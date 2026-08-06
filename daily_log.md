# Günlük Çalışma Kaydı (Daily Log)

Bu dosya, staj süresince her gün yapılan çalışmaları tarih bazında kayıt altına almak için kullanılmaktadır.

---

## 17.07.2026

**Yapılanlar:**
- Proje konusu ve kapsamı netleştirildi: "Gömülü Sistem Firmware'lerinde Çok Katmanlı Bütünlük İhlali Tespiti ve Adli Bilişim Analizi"
- Proje önerisi dokümanı (amaç, kapsam, analiz katmanları, yöntem/araçlar, 20 iş günlük plan) hazırlandı
- Arayüz tasarımı planlandı (özet kartları, katman bazlı sekmeler, olay zaman çizelgesi, delil zinciri paneli, rapor dışa aktarma)
- Arayüz fonksiyonel gereksinimleri (FR-1 – FR-8) belirlendi
- GitHub reposu oluşturuldu, README.md ve daily_log.md eklendi

**Notlar / Sonraki Adımlar:**
- Açık kaynak firmware imajlarının (OpenWrt / Yocto örnek build) toplanmasına başlanacak
- Statik bütünlük (hash karşılaştırma) katmanının geliştirilmesine geçilecek

---

## 20.07.2026

**Yapılanlar:**

1. Proje klasör yapısı kuruldu: data, layers, scoring, ui, reports klasörleri oluşturuldu - her klasör projenin farklı bir bileşenini karşılayacak (veri, analiz katmanları, skorlama mantığı, arayüz, çıktı raporları)

2. Statik bütünlük katmanı yazıldı (layers/static_integrity.py)
   - Amaç: iki firmware arasında dosya seviyesinde SHA-256 hash karşılaştırması yaparak eklenen, silinen ve içeriği değiştirilen dosyaları tespit etmek
   - Üç ana fonksiyon yazıldı: dosya hash hesaplama, dizin tarama, iki dizini karşılaştırma

3. Entropi analizi katmanı yazıldı (layers/entropy_analysis.py)
   - Amaç: şifrelenmiş/gizlenmiş kod izlerini, dosyaları küçük bloklara bölüp her bloğun Shannon entropi değerini (rastgelelik ölçüsü) hesaplayarak yakalamak
   - Yüksek entropi genelde şifrelenmiş veya sıkıştırılmış içeriğe işaret eder

4. Test verisi olarak gerçek bir OpenWrt firmware imajı kullanılmasına karar verildi
   - OpenWrt 25.12.5 (x86-64, generic, squashfs-rootfs) resmi firmware selector aracından indirildi
   - İmaj açılıp (.gz -> .img) içindeki gerçek Linux dosya sistemi çıkarıldı: toplam 940 dosya, data/original klasörüne yerleştirildi
   - Bu adımda binwalk aracı Windows'ta çalışmadığı için (ModuleNotFoundError), alternatif olarak PySquashfsImage Python kütüphanesi kullanıldı

5. Gerçekçi bir saldırı senaryosu simüle edildi (data/tamper_firmware.py)
   - data/original klasörü kopyalanarak data/suspicious oluşturuldu
   - Üç farklı manipülasyon türü uygulandı: yeni bir backdoor dosyası eklendi (usr/bin/update_service - içinde reverse shell kodu barındırıyor), mevcut bir konfigürasyon dosyası değiştirildi (etc/dnsmasq.conf), ve backdoor dosyasına şüpheli bir SUID izni verildi

6. Statik bütünlük katmanı gerçek veriyle test edildi
   - Sonuç: eklenen dosya (update_service) ve değiştirilen dosya (dnsmasq.conf) başarıyla ve doğru şekilde tespit edildi

7. Entropi analizi katmanında önemli bir metodolojik sorun tespit edildi ve çözüldü
   - İlk yaklaşım (sabit bir entropi eşiğiyle "şüpheli" işaretleme) gerçek firmware'de çok fazla yanlış alarm üretti, çünkü derlenmiş kütüphane dosyaları (.so) ve kernel modülleri (.ko) doğal olarak yüksek entropili çıkıyor
   - Çözüm: yöntem "karşılaştırmalı entropi analizine" çevrildi - artık tek bir dosyanın entropisinin yüksek olup olmadığına değil, iki firmware arasında AYNI dosyanın entropi profilinin değişip değişmediğine bakılıyor
   - Ek gözlem: entropi katmanı, düz metin olarak yazılmış backdoor'u yakalayamadı - bu beklenen bir durumdu çünkü şifrelenmemiş kod entropiyi yükseltmiyor. Bu bulgu, tek bir analiz yöntemine güvenilemeyeceğini, bu yüzden projenin çok katmanlı tasarlandığını somut olarak doğruladı

8. .gitignore dosyası eklendi
   - Büyük ham firmware dosyaları (.img, .img.gz - GitHub'ın 100MB dosya boyutu sınırını aşıyor) ve çıkarılmış dosya sistemleri (940+ dosya, gereksiz repo şişkinliği) hariç tutuldu
   - Bu dosyalar zaten script'lerle (decompress_firmware.py, extract_squashfs.py) yeniden üretilebildiği için versiyon kontrolüne dahil edilmesine gerek yok

9. Tüm değişiklikler GitHub'a commit ve push edildi

**Karşılaşılan Sorunlar ve Çözümleri:**
- binwalk Windows'ta kurulamadı/çalışmadı (ModuleNotFoundError: No module named 'binwalk.core') -> PySquashfsImage kütüphanesine geçildi
- Entropi katmanının ham eşik değeri gerçek firmware'de yanlış alarm üretti -> karşılaştırmalı (comparative) analiz yaklaşımına geçildi

**Notlar / Sonraki Adımlar:**
- YARA imza/pattern tarama katmanına (3. katman) geçilecek
- İzin/yetki (SUID/SGID) analiz katmanına geçilecek

## 21.07.2026

**Yapılanlar:**

1. YARA imza/pattern tarama katmanı tasarlandı ve yazıldı
   - Amaç: firmware dosyalarını bilinen backdoor/zararlı kod imzalarına karşı taramak
   - rules/backdoor_rules.yar dosyasında 3 YARA kuralı yazıldı: Suspicious_Backdoor_Keyword (backdoor, reverse_shell gibi anahtar kelimeler, yüksek risk), Hardcoded_Credentials (kod içine gömülü şifre/kullanıcı adı şüphesi, orta risk), Suspicious_Network_Command (uzaktan erişim komutları, yüksek risk)
   - layers/yara_scan.py modülü yazıldı: dosyaları bu kurallara karşı tarayıp eşleşmeleri (kural adı, açıklama, risk seviyesi, eşleşen metin) raporluyor

2. YARA katmanı gerçek veriyle test edildi
   - Sonuç: data/suspicious/usr/bin/update_service dosyasındaki backdoor, "Suspicious_Backdoor_Keyword" kuralı ile başarıyla tespit edildi (eşleşen kelimeler: backdoor, reverse_shell, nc -e)
   - Önemli bulgu: entropi katmanının bir önceki gün kaçırdığı bu backdoor'u YARA katmanı yakaladı - bu, projenin çok katmanlı tasarım felsefesinin (tek katmana güvenmemek) somut kanıtı oldu

3. Yanlış pozitif gözlemi yapıldı
   - data/original'da (yani hiçbir manipülasyon içermeyen orijinal firmware'de) bile 12 dosyada "Hardcoded_Credentials" kuralı eşleşti (örneğin pppd, birkaç .js dosyası) - bunlar "password=" gibi normal konfigürasyon ifadeleri içerdiği için tetiklenmiş, gerçek bir tehdit değil
   - Bu gözlem not edildi: ileride skorlama katmanında bu kurala düşük ağırlık verilmesi, ya da sadece suspicious'a özgü (original'da olmayan) eşleşmelerin sayılması gerektiği belirlendi

4. Kod kalitesi iyileştirmesi: tüm kod dosyaları İngilizceye çevrildi
   - static_integrity.py, entropy_analysis.py, yara_scan.py, tamper_firmware.py, decompress_firmware.py, extract_squashfs.py, generate_test_data.py dosyalarındaki Türkçe yorum satırları ve değişken isimleri İngilizceye çevrildi
   - Bu değişiklik sonrası tüm katmanlar tekrar çalıştırılıp sonuçların değişmediği (sadece dilin değiştiği) doğrulandı

**Literatür Taraması (paralel görev):**
- Literatür taraması görevine başlandı: proje konusu (firmware bütünlük tespiti / adli bilişim) etrafında Google Scholar üzerinden arama yapıldı
- İlk 5 makale bulunup DOI ve GitHub kod durumu teyit edildi: P01 FFXE (USENIX Security 2024, kod var), P02 ROSA (ICSE 2025, kod var), P03 AutoFirm (arXiv 2024, kod var), P04 ChkUp (USENIX Security 2024, kod var), P05 MARS (DFRWS 2024, kod paylaşımı yok)

**Notlar / Sonraki Adımlar:**
- İzin/yetki (SUID/SGID) analiz katmanına geçilecek

## 22.07.2026

**Yapılanlar:**

1. İzin/yetki (SUID/SGID) analiz katmanı tasarlandı
   - Amaç: iki firmware arasında dosya izinlerindeki şüpheli değişiklikleri (özellikle SUID/SGID biti eklenmesi) tespit etmek - saldırganlar genelde kalıcı erişim sağlamak için masum görünen bir dosyaya bu tür izinler ekler

2. Önemli bir teknik engelle karşılaşıldı ve çözüldü
   - İlk denemede canlı dosya sistemi (data/original, data/suspicious klasörleri) üzerinden izin okumaya çalışıldı, ancak sonuç her zaman "0 değişiklik" çıktı
   - Kök neden araştırıldı: Windows/NTFS dosya sistemi, Linux'a özgü SUID/SGID izin bitlerini desteklemiyor - tamper_firmware.py içinde chmod ile eklenen SUID izni Windows'ta sessizce yok sayılıyordu
   - Çözüm: PySquashfsImage kütüphanesinin dosya nesnelerinin gerçek Unix izin bilgisini (mode, uid, gid) sakladığı fark edildi. Yaklaşım değiştirildi: izinler artık canlı dosya sisteminden değil, squashfs imajının kendi orijinal meta verisinden okunuyor

3. extract_squashfs.py güncellendi
   - Artık dosya içeriğini çıkarmanın yanı sıra, her dosyanın gerçek Unix izin bilgisini de data/original_permissions.json adlı bir manifest dosyasına kaydediyor

4. tamper_firmware.py güncellendi
   - SUID izni simülasyonu artık gerçek (ve Windows'ta işe yaramayan) chmod çağrısı yerine, JSON manifest üzerinde (data/suspicious_permissions.json) yapılıyor

5. layers/permission_analysis.py yazıldı
   - İki manifest dosyasını karşılaştırıp yeni SUID/SGID kazanan dosyaları ve izin değişikliklerini tespit ediyor

6. Katman gerçek veriyle test edildi
   - Sonuç: usr/bin/update_service dosyasına eklenen SUID izni (rws------ olarak) başarıyla ve doğru şekilde tespit edildi

**Karşılaşılan Sorun ve Çözümü (özet):**
Windows/NTFS dosya sistemi Unix izin bitlerini (SUID/SGID) desteklemediği için canlı dosya sistemi üzerinden izin analizi yapılamadı. Çözüm olarak izin bilgisi, dosya çıkarma anında squashfs imajının kendi meta verisinden okunup ayrı JSON manifest dosyalarında saklanacak şekilde mimari değiştirildi. Bu, adli bilişim açısından da daha doğru bir yöntem oldu çünkü orijinal imaj verisine dayanıyor.

**Literatür Taraması (paralel görev):**
- Aramaya devam edildi, 5 makale daha bulunup teyit edildi: P06 TELEMETRY/IoT Ecosystems (SN Computer Science 2026, kod yok), P07 Binary Diff Summarization LLM (arXiv 2025, kod yok), P08 SynthChain (arXiv 2026, düşük öncelik), P09 PEMU (ACM CCS 2025, kod var), P10 Out-of-Band Power Side-Channel Detection (arXiv 2026, kod yok)
- Toplam 10 makale (P01-P10) için aday listesi tamamlandı

**Notlar / Sonraki Adımlar:**
- 4 analiz katmanı tamamlandı (statik bütünlük, entropi, YARA, izin/yetki)
- Sırada: skorlama ve zaman çizelgesi katmanı

## 23.07.2026

**Yapılanlar:**

1. Skorlama katmanı tasarlandı ve yazıldı (layers/scoring.py)
   - Bu katmanın amacı: önceki 4 analiz katmanından (statik bütünlük, entropi, YARA, izin/yetki) gelen ham bulguları tek başlarına değil, birlikte değerlendirip tek bir "şüphe skoru" (0-100 arası) üretmek
   - Her bulgu türü için bir ağırlık (puan) belirlendi. Örneğin: yeni eklenen bir dosya +15 puan, değiştirilen bir dosya +10 puan, YARA'nın yüksek riskli bir kural eşleşmesi +25 puan, yeni bir SUID/SGID izin değişikliği +25 puan gibi
   - Ağırlıkların belirlenme mantığı: katman ne kadar "kesin/güvenilir" kanıt sunuyorsa o kadar yüksek puan verildi (örneğin izin değişikliği ve YARA yüksek risk eşleşmesi, entropi değişiminden daha güçlü birer kanıt sayıldı)

2. İlk testte beklenmeyen bir sonuç çıktı: skor doğrudan 100/100'e (üst sınıra) ulaştı
   - Sebebi araştırıldı: YARA katmanının "Hardcoded_Credentials" kuralı, hem orijinal hem şüpheli firmware'de aynı şekilde bulunan normal dosyalarda (örneğin pppd, birkaç .js dosyası) tekrar tekrar eşleşiyordu
   - Bu eşleşmeler gerçek bir saldırı belirtisi değil, firmware'in doğal/normal içeriğiydi - yani skorlama, "iki firmware arasındaki farkı" değil, "şüpheli firmware'deki her şeyi" sayıyordu, bu da yanlış

3. Skorlama mantığı düzeltildi
   - YARA bulguları artık sadece şüpheli firmware'e ÖZGÜ olan (yani orijinalde bulunmayan, yeni ortaya çıkan) eşleşmeleri sayacak şekilde güncellendi
   - Bu düzeltme, statik bütünlük ve entropi katmanlarında zaten kullanılan "karşılaştırmalı" mantıkla tutarlı hale getirildi

4. Düzeltme sonrası test edildi, sonuç doğrulandı
   - Yeni skor: 75/100
   - Toplam 4 anlamlı bulgu tespit edildi, hepsi daha önce bilinçli olarak eklediğim test senaryosuyla (backdoor dosyası eklenmesi, bir konfigürasyon dosyasının değiştirilmesi, şüpheli SUID izni verilmesi) birebir örtüşüyor
   - Bu, sistemin artık gerçek bir tehdidi doğru tespit edip yanlış alarm vermediğini kanıtlıyor


**Karşılaşılan Sorun ve Çözümü (özet):**
İlk skorlama denemesi ham veriyi doğrudan topladığı için yanlış pozitiflerden etkilendi (skor 100/100 çıktı). Kök neden analiziyle sorunun YARA katmanının normal firmware içeriğini de saydığı tespit edildi. Çözüm olarak YARA katmanına da diğer katmanlarda kullanılan "karşılaştırmalı" (sadece fark olanı say) mantığı uygulandı, skor gerçekçi bir değere (75/100) düştü.

**Literatür Taraması (paralel görev):**
- P02 (ROSA) için makale inceleme şablonu dolduruldu (5 bölümlü: künye, teknik analiz, veri seti/tekrarlanabilirlik, proje kriterleriyle karşılaştırma, değerlendirme) — uygunluk skoru: 3
- P10, P12, P13, P14 makaleleri için şablonlar dolduruldu
- Dosya isimlendirme kuralı belirlendi: PXX dosya adları makale başlığına göre olacak (örn. P14-Multi-Interface-Firmware-Acquisition-and-Validation.md)

**Notlar / Sonraki Adımlar:**
- Skorlama katmanı tamamlandı - 6 katmanlı sistemin 5.'si bitti
- Sırada: zaman çizelgesi (timeline) oluşturma ve delil zinciri (chain of custody, SHA-256 tabanlı) belgeleme katmanı


 ## 24.07.2026

**Yapılanlar:**

1. Zaman çizelgesi (timeline) ve delil zinciri (chain of custody) katmanının tasarımı yapıldı
   - Bu katman, projenin 6. ve son analiz aşamasının bir parçası ("Skorlama ve zaman çizelgesi" - proje önerisindeki 5. katman)
   - İki ayrı ama birbirine bağlı hedefi var: (a) tüm bulguları okunabilir, kronolojik bir olay listesine dönüştürmek, (b) bu bulguların adli bilişim standartlarına uygun şekilde "delil" olarak korunmasını sağlamak

2. layers/timeline.py modülü yazıldı, 4 ana fonksiyon içeriyor:
   - `hash_finding()`: bir bulgu kaydını JSON formatına çevirip SHA-256 ile hash'liyor. JSON'ın anahtarları sıralı (sort_keys=True) tutuluyor ki aynı veri her zaman aynı hash'i üretsin, tutarlılık sağlansın
   - `build_timeline()`: skorlama katmanından gelen ham bulgu listesini alıp her birine bir olay numarası (event_id), zaman damgası (UTC formatında ISO 8601), ve kendi SHA-256 hash'ini ekliyor
   - `save_timeline()`: oluşturulan timeline'ı reports/timeline.json dosyasına JSON formatında kaydediyor, böylece hem insan tarafından okunabilir hem de ileride raporlama/arayüz katmanında kullanılabilir hale geliyor
   - `verify_timeline_integrity()`: delil zincirinin bütünlüğünü doğrulayan fonksiyon - her kayıt için hash'i saklanan değerden ayırıp yeniden hesaplıyor, eğer yeniden hesaplanan hash saklanan hash ile eşleşmiyorsa o kaydın sonradan değiştirildiği anlaşılıyor

3. Neden hash tabanlı delil zinciri gerekli - kısaca açıklama:
   - Adli bilişim çalışmalarında, bir bulgunun mahkemede veya resmi bir incelemede kabul edilebilir olması için "değiştirilmediğinin" kanıtlanabilir olması gerekiyor
   - SHA-256 hash, bir verinin "parmak izi" gibi çalışıyor - veride tek bir karakter bile değişse, hash tamamen farklı çıkıyor
   - Bu sayede, ileride biri "bu bulgu sonradan eklendi/değiştirildi" iddiasında bulunursa, hash karşılaştırmasıyla bunun doğru olup olmadığı kesin olarak kanıtlanabiliyor

4. Katman, önceki günlerde tamamlanan skorlama katmanıyla (layers/scoring.py) entegre edilerek uçtan uca test edildi
   - Script çalıştırıldığında önce tüm 4 analiz katmanı (statik bütünlük, entropi, YARA, izin/yetki) otomatik olarak çalışıyor, skorlama yapılıyor, sonra bu bulgular timeline'a dönüştürülüyor
   - Test sonucunda önceki günden bilinen 4 bulgu (backdoor dosyası eklenmesi +15, dnsmasq.conf değişikliği +10, YARA backdoor imza eşleşmesi +25, SUID izin değişikliği +25) doğru şekilde timeline'a işlendi, toplam şüphe skoru yine 75/100 olarak doğrulandı
   - Her olayın kendine özgü, 64 karakterlik bir SHA-256 hash değeri üretildiği gözlemlendi (örnek: usr/bin/update_service dosyasındaki backdoor bulgusu için 8ddf37559ef339e5... ile başlayan hash)

5. Bütünlük doğrulama testi çalıştırıldı
   - Sonuç: "Integrity check: PASSED" - yani oluşturulan 4 kaydın hiçbiri bozulmamış, tutarlı
   - Bu, sistemin kendi ürettiği delilleri kendi kendine doğrulayabildiğini gösteren önemli bir kanıt oldu
   
6. - requirements.txt oluşturuldu, README.md Kullanım bölümü gerçek/güncel komutlarla düzeltildi
**Karşılaşılan zorluk:** Bu aşamada teknik bir sorunla karşılaşılmadı - önceki günlerde (binwalk sorunu, entropi eşiği kalibrasyonu, Windows/NTFS SUID kısıtlaması) kurulan sağlam altyapı sayesinde bu katman sorunsuz şekilde entegre oldu. Bu da önceki günlerde yapılan hata ayıklama ve mimari düzeltmelerin (örneğin manifest tabanlı izin sistemine geçiş) ne kadar isabetli olduğunu gösterdi.

**Sonuç:** 6 katmanlı sistemin 5'i tamamlandı: statik bütünlük, entropi analizi, YARA imza tarama, izin/yetki analizi, skorlama + zaman çizelgesi/delil zinciri. Geriye sadece "değerlendirme" (bilinen CVE örnekleriyle doğrulama) ve arayüz (Streamlit) aşamaları kaldı - bunlar sırasıyla 4. haftanın ilk ve ikinci yarısında planlanmıştı.

**Literatür Taraması (paralel görev):**
- P11-P15 arası makalelerin araştırması ve teyidi tamamlandı: P12 (hafif hash fonksiyonları ile IoT secure boot), P13 (SIMON tabanlı paralel hash fonksiyonu), P14 (drone firmware çok arayüzlü doğrulama), P15 (ELF header tabanlı IoT malware tespiti)

**Notlar / Sonraki Adımlar:**
- Zaman çizelgesi ve delil zinciri katmanı tamamlandı ve test edildi
- Bilinen bir CVE örneğiyle sistemin doğrulanması (değerlendirme aşaması)
- Ardından Streamlit tabanlı web arayüzüne geçilecek 
 
## 27.07.2026

**Yapılanlar:**

1. Değerlendirme aşamasına başlandı: gerçek bir CVE ile sistemin doğrulanması hedeflendi
   - Proje önerisindeki "geliştirilen yöntemin bilinen gerçek CVE örnekleriyle test edilerek doğrulanması" maddesi kapsamında, önce hangi CVE'nin projeyle en uyumlu olduğu araştırıldı
   - Araştırma sonucu CVE-2024-54143 (OpenWrt Attended Sysupgrade sunucusu, CVSS 9.3, Aralık 2024) seçildi - projenin doğrudan konusuyla (firmware bütünlük doğrulaması) birebir örtüşen, güncel ve kritik seviyeli bir zafiyet olması tercih sebebi oldu

2. CVE'nin teknik mekanizması analiz edildi ve belgelendi (reports/cve_evaluation.md)
   - Zafiyet iki parçadan oluşuyor: imagebuilder sürecinde komut enjeksiyonu, ve build isteklerini doğrulamak için kullanılan SHA-256 hash'in sadece 12 karaktere kısaltılmış olması
   - Kısaltılmış hash, hash çakışması (collision) üretmeyi hesaplama açısından mümkün kılıyor - bu da bir saldırganın kötü amaçlı bir firmware imajını meşru imajın yerine geçirip bütünlük kontrolünü atlatmasına izin veriyor
   - Belgede CVE'nin özeti, projeyle ilgisi, ve bu projenin yöntemiyle ilişkisi ayrı başlıklar altında yazıldı

3. Bu projenin yöntemiyle CVE arasındaki ilişki ortaya konuldu
   - layers/static_integrity.py katmanının tam uzunlukta (64 karakter, kısaltılmamış) SHA-256 kullandığı doğrulandı
   - Bu tasarım tercihinin, CVE-2024-54143'ün istismar ettiği zafiyet sınıfına (kısaltılmış hash zayıflığı) karşı doğal bir direnç sağladığı sonucuna varıldı
   - Yani projenin daha önceden yapılmış bir mimari kararının (tam hash kullanımı), gerçek dünyada yaşanmış kritik bir güvenlik açığına karşı koruma sağladığı gösterilmiş oldu

4. Sayısal kanıt üretildi: data/hash_truncation_demo.py yazıldı ve çalıştırıldı
   - Script, aynı veri için hem tam SHA-256 hash'i (256 bit, 64 karakter) hem de CVE'deki gibi kısaltılmış hash'i (48 bit, 12 karakter) üretip olası değer sayılarını karşılaştırıyor
   - Sonuç: tam hash arama uzayı, kısaltılmıştan yaklaşık 4.1 x 10^62 kat daha büyük
   - Bu sayısal fark, "neden tam hash kullanmak önemli" savını soyut bir iddia olmaktan çıkarıp somut bir sayıyla kanıtladı

5. Bulgular commit edilip GitHub'a gönderildi
   - Commit mesajında CVE analizi, mekanizma açıklaması ve sayısal sonuç ayrı ayrı belgelendi

**Sonuç:**
"Değerlendirme" aşamasının ilk ve en kapsamlı parçası (CVE-2024-54143 analizi) tamamlandı. Bu, proje önerisindeki "geliştirilen yöntemin bilinen gerçek CVE örnekleriyle test edilerek doğrulanması" maddesinin somut bir kanıtı oldu.

**Notlar / Sonraki Adımlar:**
- İkinci bir CVE değerlendirmesi (backdoor/kimlik doğrulama temalı) yapılacak
- Silinen dosya test senaryosu eklenip test edilecek
- Ardından Streamlit arayüzüne geçilecek

## 28.07.2026

**Yapılanlar:**

1. İkinci CVE değerlendirmesi yapıldı: CVE-2024-9643 (Four-Faith F3x36 endüstriyel router)
   - Bu CVE, firmware'e gömülü, sabit (değiştirilemeyen) admin kullanıcı adı/şifre çiftinden kaynaklanıyor - CWE-798 (Hard-coded Credentials) sınıfının gerçek dünyadan bir örneği
   - reports/cve_evaluation_2.md dosyasında zafiyetin mekanizması ve bu projenin YARA katmanıyla (Hardcoded_Credentials kuralı) ilişkisi belgelendi
   - Önceki testlerde (2. gün) bu kuralın normal OpenWrt dosyalarında da yanlış pozitif ürettiği dürüstçe not edildi, bunun skorlama katmanındaki karşılaştırmalı mantıkla (sadece yeni eşleşmeleri sayma) kısmen çözüldüğü açıklandı

2. CVE-2024-9643 için pratik bir test yazıldı (data/hardcoded_credential_test.py)
   - CVE'nin deseniyle uyumlu bir kimlik bilgisi (admin:admin, password=support123) data/suspicious içine eklendi
   - YARA katmanı çalıştırıldı, test dosyasının Hardcoded_Credentials kuralıyla başarıyla tespit edildiği doğrulandı
   - Küçük bir script hatası (Windows'ta dosya yolu ayracı farkı nedeniyle "Not detected" yanlış çıktısı) fark edilip düzeltildi

3. Silinen dosya test senaryosu eklendi
   - tamper_firmware.py güncellendi: mevcut bir dosyanın (etc/shells) silinmesi simüle edildi - bu, bir saldırganın kanıt/iz silmesi senaryosunu temsil ediyor
   - Bu, statik bütünlük katmanının "silinen dosya" tespit yeteneğinin ilk kez gerçek veriyle test edilmesini sağladı

4. Skorlama katmanı güncellendi (layers/scoring.py)
   - Silinen dosyalar için yeni bir ağırlık eklendi (static_deleted_file: +20 puan)
   - Bu ağırlık, ilgili bulgu türü için puanlama mantığına entegre edildi

5. Tüm sistem uçtan uca yeniden test edildi
   - Final sonuç: 100/100 şüphe skoru, 7 anlamlı bulgu
   - Bulgular: 2 eklenen dosya (backdoor + hardcoded credential dosyası), 1 değiştirilen dosya, 1 silinen dosya, 2 YARA eşleşmesi, 1 SUID izin değişikliği
   - Tüm bulgular, bilinçli olarak oluşturulan test senaryosuyla birebir örtüşüyor - yanlış pozitif veya kaçırılan bulgu yok

**Sonuç:**
"Değerlendirme" aşaması artık tam anlamıyla tamamlandı: proje artık 2 farklı, gerçek ve güncel CVE ile doğrulanmış durumda (CVE-2024-54143: hash kısaltma zafiyeti, CVE-2024-9643: hardcoded credentials), ayrıca tüm manipülasyon türlerini (ekleme, değiştirme, silme, izin değişikliği) kapsayan eksiksiz bir test senaryosu oluşturuldu.

**Literatür Taraması (paralel görev):**
- P15-P20 arası 6 makale için inceleme şablonları dolduruldu
- P21-P30 arası 10 makale için inceleme şablonları dolduruldu — toplam 30 makalelik hedef tamamlandı
- Özet Karşılaştırma Tablosu (30 makale) ve Arama Stratejisi belgesi dolduruldu
- Gap analizi çıkarıldı: diferansiyel analiz (A/B) sadece 1/30 makalede, delil zinciri sadece 4/30 makalede, tek şüphe skoru sadece 5/30 makalede mevcut
- Kod teyidi tamamlanan 10 makale netleşti: FFXE, ROSA, AutoFirm, ChkUp, PEMU, FirmRCA, UEFI Memory Forensics, UniBOM, LFwC, Pack-ALM
- GitHub reposu içinde /literature-review/ klasörü oluşturuldu (articles/ alt klasörü + özet tablo + arama stratejisi), README'ye literatür taraması bölümü eklendi
- P01-P30 dosyaları ile özet tablodaki uygunluk skorları karşılaştırılıp 11 makaledeki uyuşmazlık tespit edilip düzeltildi

**Notlar / Sonraki Adımlar:**
- Değerlendirme aşaması tamamlandı (2/2 CVE + tam test senaryosu)
- Sırada: Streamlit arayüzüne başlama - dosya yükleme, analiz başlatma, özet kartları

## 29.07.2026

**Yapılanlar:**

1. Streamlit arayüzüne başlandı: dosya yükleme ve analiz başlatma (FR-1, FR-6'nın skor kısmı)
   - app.py oluşturuldu: iki dosya yükleme alanı (orijinal/şüpheli firmware), "Analizi Başlat" butonu
   - Yüklenen dosyalar geçici bir dizine kaydedilip gerektiğinde açılıyor (.gz ise), squashfs içeriği çıkarılıyor, tüm analiz katmanları otomatik çalıştırılıyor

2. Mevcut kod, arayüzle uyumlu hale getirmek için yeniden düzenlendi
   - layers/scoring.py: run_all_layers fonksiyonu artık izin manifest yollarını parametre olarak alabiliyor (öncesinde sabit kodlanmıştı, arayüz farklı geçici dizinler kullandığı için bu değişiklik gerekliydi)
   - data/extract_squashfs.py: çıkarma mantığı extract_and_save_permissions adında yeniden kullanılabilir bir fonksiyona dönüştürüldü

3. İki teknik sorun tespit edilip çözüldü
   - Windows'a özgü bir PermissionError oluştu: Streamlit'in geçici dizini temizlerken squashfs imaj dosyasının hâlâ açık tutulması nedeniyle silinemiyordu. Çözüm: SquashFsImage nesnesi işi bitince image.close() ile açıkça kapatılıyor
   - Bir girinti (indentation) hatası oluştu, dosya tamamen yeniden yazılarak düzeltildi

4. Uçtan uca test yapıldı
   - Aynı firmware dosyası hem "orijinal" hem "şüpheli" olarak yüklendi
   - Sonuç: 0/100 şüphe skoru, 0 bulgu, "Düşük Risk" etiketi - iki özdeş dosya arasında fark olmaması beklenen ve doğru bir sonuç
   - Bu, temel yükleme → analiz → sonuç gösterme akışının uçtan uca çalıştığını doğruladı

**Sonuç:**
Streamlit arayüzünün ilk parçası (dosya yükleme, analiz tetikleme, özet kartları) tamamlandı ve test edildi. Katman bazlı detaylı görünüm ve zaman çizelgesi için bir bilgilendirme notu arayüze eklendi (henüz geliştirilmedi).

**Notlar / Sonraki Adımlar:**
- Katman bazlı sekmeler (FR-8) eklenecek - her analiz katmanının kendi bulgu tablosu
- Zaman çizelgesi ve delil zinciri görünümü eklenecek

## 30.07.2026

**Yapılanlar:**

1. Streamlit arayüzüne katman bazlı sekmeler eklendi (FR-8)
   - Özet kartlarının altına 4 ayrı sekme eklendi: Statik Bütünlük, Entropi Analizi, YARA Tarama, İzin/Yetki Analizi
   - Her sekme, kendi katmanının ham bulgularını (dosya listeleri, tablolar) ayrı ayrı gösteriyor

2. YARA sekmesi için özel bir mantık gerekti
   - get_new_yara_matches adında bir yardımcı fonksiyon yazıldı - bu, scoring.py'de daha önce kurduğumuz "sadece suspicious'a özgü yeni eşleşmeleri say" mantığını arayüzde de uyguluyor
   - Bu sayede sekme, normal firmware içeriğinden kaynaklanan eski YARA eşleşmelerini değil, sadece gerçekten yeni/şüpheli olanları gösteriyor

3. Test edildi
   - Aynı dosya hem orijinal hem şüpheli olarak yüklendi
   - Sonuç: 4 sekmenin de doğru şekilde "Bulgu yok" gösterdiği doğrulandı, arayüz hatasız çalıştı

**Sonuç:**
Arayüzün katman bazlı detaylı görünüm kısmı (FR-8) tamamlandı. Artık özet kartları ve katman detayları bir arada çalışıyor.

**Literatür Taraması (paralel görev):**
- 2. hafta Colab çalışması için ortam kararı verildi: donanım kısıtı nedeniyle yerel kurulum yerine Google Colab kullanılacak
- 10 kodlu makaleye hakim olmak için çalışma stratejisi belirlendi (Study Guide + Audio Overview kombinasyonu)
- 10 kodlu makale için karşılaştırmalı bir özet doküman hazırlandı (çözdüğü problem, girdi formatı, bağımlılıklar, sınırlamalar, metodolojik fark başlıklarıyla)

**Notlar / Sonraki Adımlar:**
- Zaman çizelgesi (timeline) ve delil zinciri (chain of custody) görünümü eklenecek (FR-6 tamamlanması)

## 31.07.2026

**Yapılanlar:**

1. Streamlit arayüzüne zaman çizelgesi ve delil zinciri (chain of custody) görünümü eklendi - bu, FR-6 gereksiniminin son parçasıydı (bulguların kronolojik zaman çizelgesi ve şüphe skoru olarak gösterilmesi)

2. layers/timeline.py'deki iki fonksiyon arayüze bağlandı:
   - build_timeline(findings): scoring katmanından gelen ham bulgu listesini, her biri sıra numarası, zaman damgası ve kendi SHA-256 hash'i taşıyan olay kayıtlarına dönüştürüyor
   - verify_timeline_integrity(timeline): her kaydın hash'ini yeniden hesaplayıp saklanan hash ile karşılaştırıyor, tüm kayıtlar tutarlıysa True dönüyor

3. Zaman çizelgesi tablosu tasarlandı ve eklendi
   - Sütunlar: Sıra, Katman, Dosya, Bulgu Türü, Puan, Delil Hash (SHA-256, ilk 16 karakter + "..." şeklinde kısaltılmış)
   - Bulgu yoksa "Zaman çizelgesinde gösterilecek bulgu yok" mesajı gösteriliyor

4. Delil bütünlüğü doğrulama sonucu görsel olarak arayüze yansıtıldı
   - Doğrulama başarılıysa yeşil kutuda "Delil bütünlüğü doğrulandı" mesajı, başarısızsa kırmızı kutuda uyarı

5. Arayüze katman açıklamaları eklendi
   - Her sekmenin (Statik Bütünlük, Entropi, YARA, İzin/Yetki) en üstüne, o katmanın ne yaptığını ve neden önemli olduğunu açıklayan bir bilgi kutusu eklendi
   - Amaç: arayüzü kullanan birinin teknik detaya girmeden her sekmenin işlevini anlayabilmesi

6. Test edildi
   - Aynı firmware dosyası hem orijinal hem şüpheli olarak yüklendi
   - Sonuç: "Delil bütünlüğü doğrulandı" mesajı doğru çıktı, tüm sekmelerde açıklama kutuları görüntülendi, arayüz hatasız çalıştı

**Sonuç:**
FR-6 gereksinimi tamamen tamamlandı. Arayüzün üç ana parçası (yükleme, katman sekmeleri, zaman çizelgesi/delil zinciri) birlikte çalışıyor ve her katman kendini açıklıyor.

**Literatür Taraması (paralel görev):**

1. 2. hafta Colab çalışmasına başlandı, Colab temelleri (cell, runtime, Drive bağlama) öğrenildi

2. İlk kodlu makale FFXE Colab'a kuruldu: GitHub'dan klonlandı, bağımlılıklar pip ile kuruldu (conda'ya gerek kalmadan), geliştirici modunda (`pip install -e .`) kuruldu
   - FFXE'nin kendi veri setiyle (9 gerçek örnek: ChargeHR, Flex, Switchmate cihazları) baseline testi yapıldı: `tests/test-real.py` ile 9/9 örnek hatasız çalıştı, sonuçlar (blocks/edges/elapsed süre) JSON olarak üretildi ve Google Drive'a kaydedildi (/content/drive/MyDrive/literatur-colab/FFXE/)

3. Reproduction sırası belirlendi: P01 (FFXE) tamamlandı → P02 (ROSA) şimdilik atlandı → P03 (AutoFirm) → P04 (ChkUp) → P10 (PEMU) → P17 (UEFI Memory Forensics) → P20 (FirmRCA) → P25 (LFwC) → P28 (UniBOM) → P29 (Pack-ALM)

4. P03 (AutoFirm, github.com/sure17/AutoFirm) test edildi
   - Makalenin kullandığı LFwC veri setine gerçek erişim mümkün olmadı (354GB, akademik başvuru gerekiyor) — bunun yerine OpenWrt'nin resmi sitesinden küçük bir MIPS router firmware'i (TP-Link Archer A6 v3, OpenWrt 23.05.5) indirilip kullanıldı
   - binwalk (imp modülü + --run-as=root düzeltmeleri sonrası) ve qemu-mipsel ile 53 ELF binary bulundu, emülasyon gerçekten çalıştı (loglarda gerçek help/versiyon çıktıları görüldü)
   - Ancak AutoFirm'in regex tabanlı versiyon çıkarma mantığı OpenWrt binary'lerinin çoğunda eşleşme bulamadı (çoğu --version bayrağını desteklemiyor, opkg git-hash formatında versiyon veriyor)
   - Bulgu olarak not edildi: araç klasik vendor firmware regex'lerine göre tasarlanmış, modern/minimal Linux dağıtımlarında genelleşmiyor

5. P04 (ChkUp, github.com/WUSTL-CSPL/ChkUp) denendi
   - Ghidra 10.1.2 + Java 11 + Python 3.6 zorunluluğu Colab'ın güncel Python'uyla uyumsuz olduğundan (eski paket derleme riski yüksek), P02 (ROSA) gibi sona bırakılıp P10'a (PEMU) geçildi

6. P10 (PEMU, github.com/MPI-SysSec/pemu) test edildi
   - Tam fuzzing kampanyası (Docker/SEmu/Fuzzware/Hoedur) kurmadan, `src/packer.py` içindeki çekirdek `Packer` sınıfı izole edilip doğrudan çağrıldı
   - `eval/01-coverage-experiments/stm32_f429/LwIP_TCP_Echo_Client/hoedur_config.yml` dosyasından gerçek config/apriori/protocols formatı örnek alındı, Ethernet+ARP protokol zinciriyle `packer.get_packet(['Ethernet','ARP'])` çağrıldı
   - Sonuç: başarılı — 42 byte'lık, yapısal olarak doğru bir Ethernet+ARP çerçevesi üretildi (broadcast MAC ff:ff:ff:ff:ff:ff + doğru ethertype 0x0806), PEMU'nun protokol farkındalıklı paket üretme motoru doğrulandı

7. Takip tablosu oluşturuldu: literatur-arac-sonuc-tablosu.xlsx (sütunlar: P#, Araç, Veri Seti, Durum, Çalıştı mı, Ana Metrik, Süre, Not) — her araç bitince güncellenecek, sonunda grafik için kaynak olacak

**Notlar / Sonraki Adımlar:**
- PDF/HTML rapor çıktısı eklenecek (FR-7)
- Literatür tarafında sırada: P02 (ROSA) ve P04 (ChkUp) için tekrar deneme ya da alternatif yaklaşım, ardından P17, P20, P25, P28, P29

## 03.08.2026

**Yapılanlar:**

1. Delil zinciri bütünlük mesajlarının netleştirilmesi
   - Önceki günlerde eklenen "Delil Zinciri Bütünlüğü: Doğrulandı" mesajı, yüksek şüphe skoruyla (örneğin 100/100, Yüksek Risk) aynı ekranda göründüğünde yanlış anlaşılmaya açık bir ifadeydi - "doğrulandı" kelimesi, firmware'in güvenli olduğu izlenimini verebiliyordu
   - Ayrım netleştirildi: Şüphe Skoru ve Risk Seviyesi firmware'in kendisiyle ilgili bir değerlendirme; Delil Zinciri Bütünlüğü ise aracın ürettiği bulgu kayıtlarının sonradan değiştirilip değiştirilmediğiyle ilgili, tamamen ayrı bir kontrol
   - app.py'deki başarı mesajına şu netleştirici not eklendi: "(Not: bu, firmware'in güvenli olduğu anlamına gelmez — sadece bu rapordaki kayıtların tahrif edilmediğini gösterir.)"
   - reports/report_generator.py'deki HTML rapor metni aynı mantıkla güncellendi
   - Hem arayüzdeki hem HTML rapordaki başlık "Delil Zinciri Bütünlüğü"nden "Rapor Kayıtlarının Bütünlüğü (Delil Zinciri)"ne çevrildi

2. Değişiklik sırasında oluşan teknik sorunun giderilmesi
   - Metin güncellemesi yapılırken app.py dosyasında bir IndentationError oluştu (satır 218, "unindent does not match any outer indentation level")
   - Dosyanın tamamı yeniden yazılarak (mevcut tüm fonksiyonlar, sekmeler, rapor bölümü korunarak) hata giderildi

3. Arayüzün ilk kez gerçek ölçekte, dolu bir senaryoyla test edilmesi
   - Şimdiye kadar yapılan tüm arayüz testleri "aynı dosyayı hem orijinal hem şüpheli olarak yükle" şeklindeydi, bu da her zaman 0 bulgu ve düşük risk sonucu veriyordu - yani arayüzün yoğun/gerçek bir bulgu listesini nasıl işlediği hiç görülmemişti
   - Bugün iki farklı gerçek OpenWrt sürümü (daha eski bir sürüm ve elimizdeki mevcut 25.12.5 sürümü) sırasıyla "Orijinal" ve "Şüpheli" alanlarına yüklendi
   - Sonuç: 100/100 şüphe skoru, 1337 bulgu, "Yüksek Risk" etiketi - iki farklı OpenWrt sürümü arasında beklenen, gerçek ve yoğun bir dosya farkı
   - Bu test, hem katman sekmelerinin hem zaman çizelgesi tablosunun hem de HTML rapor çıktısının yüzlerce/binlerce satırlık gerçek bir bulgu listesini hatasız şekilde işleyip görüntüleyebildiğini doğruladı - önceki testlerde bu ölçek hiç denenmemişti

4. Güncellenmiş mesajlarla birlikte sistemin tamamı tekrar test edildi, hatasız çalıştığı doğrulandı

**Sonuç:**
Delil zinciri kavramı artık hem arayüzde hem rapor çıktısında yanlış anlaşılmaya daha az açık şekilde ifade ediliyor. Proje, kuruluşundan bu yana ilk kez gerçek ölçekte (binlerce dosyalık fark) uçtan uca test edilmiş oldu; bu, önceki testlerin sadece "boş senaryo"yu doğruladığı, bugünün testinin ise "dolu senaryo"yu doğruladığı anlamına geliyor.


 **Literatür Taraması (paralel görev):**
 1. P17 (UEFI Memory Forensics, github.com/UefiMemAnalysis/UefiMemAnalysis) test edildi
Kurulum sorunsuz geçti (pip install -e .)
Gerçek QEMU+OVMF+Windows guest dump'ı bugün için gerçekçi olmadığından, aracın kaynak kodundaki gerçek imza/offset değerleri (SIGNATURE=b'ldri' ve ilgili offsetler) kullanılarak elle minimal, yapısal olarak geçerli sentetik bir UEFI bellek dökümü inşa edildi
uefi_image_carving modülü bu sentetik dump üzerinde çalıştırıldı: sonuç başarılı — 1/1 sinyal doğru tespit edildi, tüm doğrulama adımları (revizyon, sistem tablosu, boyut kontrolleri) geçti, 0 red — aracın imza tarama + doğrulama mantığı doğrulandı
2. P20 (FirmRCA, github.com/NESA-Lab/FirmRCA) test edildi
capstone (belirtilen commit) + uv ortamı + C projesi (autogen/configure/make) sorunsuz derlendi
Hazır demo veri seti (testsuites-demo.zip: p2im-12, p2im-22, zephyr-54) kullanıldı
p2im-12 test case'i çalıştırıldı: ~25 dakika (1501.9 saniye) süren bir analizin ardından başarıyla tamamlandı — 168.542 komutluk tersine yürütme yapıldı, 53 taintli komut + 8 dallanma + 69 taint çifti tespit edildi, gerçek adres/assembly çıktısıyla kök neden analizi üretildi
3. P28 (UniBOM, github.com/nqminds/UniBOM) test edildi
Aracın gerektirdiği tam Docker Compose kurulumu (5 container) yerine, arkasında kullandığı çekirdek motorlar (syft + grype) Docker'sız, bağımsız binary olarak kuruldu
OpenWrt dosya sistemi üzerinde syft çalıştırıldı — 338 bileşen (SBOM) tespit edildi
Aynı SBOM üzerinde grype ile CVE taraması yapıldı — 8 zafiyet bulundu (1 kritik, 5 orta, 2 düşük) — SBOM üretme + zafiyet tarama pipeline'ı uçtan uca doğrulandı
4. 2.hafta reproduction durumu: 10 araçtan 7'si tamamlandı (FFXE, AutoFirm, PEMU, UEFI Memory Forensics, FirmRCA, UniBOM), 2'si ertelendi (ROSA: Docker/AFL++ derleme yükü; ChkUp: Ghidra+Python 3.6 uyumsuzluğu), 1'i (Pack-ALM) kaldı
Takip tablosu (literatur-arac-sonuc-tablosu.xlsx) ve tüm Colab not defterleri GitHub'a yüklendi

Sonuç:
Literatür taraması paralel görevinde 2. hafta reproduction çalışması büyük ölçüde tamamlandı — 7/10 araç gerçek çalıştırmayla doğrulandı, kalan 1 araç (Pack-ALM) ve ertelenen 2 araç için (ROSA, ChkUp) sonraki adım netleşti.

**Notlar / Sonraki Adımlar:**
- Arayüz görsel iyileştirme ve hata yönetimi (12. gün)
- Uçtan uca entegrasyon testi (13. gün) 

## 04.08.2026

**Yapılanlar:**

1. Analiz akışına hata yönetimi eklendi
   - app.py'deki analiz bloğu try/except yapısıyla sarıldı
   - Hata durumunda (örneğin geçersiz/bozuk bir dosya yüklendiğinde) uygulama çökmek yerine kırmızı bir hata kutusunda anlaşılır bir mesaj gösteriyor: "Analiz sırasında bir hata oluştu. Yüklenen dosyaların geçerli bir squashfs imajı olduğundan emin olun."
   - Teknik hata detayı (exception ve traceback) st.exception ile katlanabilir şekilde sunuluyor, isteyen inceleyebiliyor
   - Hata durumunda önceki analiz sonuçları (varsa) session state'ten temizleniyor, eski/yanıltıcı sonuçların ekranda kalması önleniyor
   - Başarılı analiz sonrası küçük bir bildirim balonu (toast) eklendi

2. Arayüze sol panel (sidebar) eklendi
   - Proje başlığı, kısa açıklama, 6 analiz katmanının listesi ve GitHub repo linkini içeriyor
   - Amaç: arayüzü ilk kez gören birinin projeyi tanıması için ek bağlam sağlamak

3. Boş durum mesajı eklendi
   - Hiç dosya yüklenmemiş durumda, kullanıcıyı yönlendiren bir bilgi kutusu gösteriliyor

4. Hata yönetimi kasıtlı olarak test edildi
   - Bir .txt dosyasının uzantısı .img olarak değiştirilip "Şüpheli Firmware" alanına yüklendi
   - Sonuç: uygulama çökmedi, beklenen hata mesajı doğru şekilde gösterildi, teknik detay (PermissionError, squashfs açma hatası zincirinden kaynaklanan) traceback içinde görüntülendi

5. Normal senaryo tekrar test edildi
   - Geçerli firmware dosyalarıyla analiz akışının, hata yönetimi eklendikten sonra da sorunsuz çalıştığı doğrulandı

**Sonuç:**
Arayüz artık geçersiz girdilere karşı dayanıklı ve kullanıcıyı daha iyi yönlendiren bir yapıya kavuştu. Görsel/bağlamsal iyileştirmelerle (sidebar, boş durum mesajı) birlikte arayüz daha profesyonel bir görünüme ulaştı. 


 **Literatür Taraması (paralel görev):**
**Yapılanlar:**

1. P02 (ROSA, github.com/binsec/rosa) ikinci kez ele alındı. Rust toolchain (rustup) kuruldu. cargo build --release, AFL++ olmadan başarıyla derlendi (yaklaşık 2 dakika 29 saniye), 7 yardımcı binary üretildi (rosa, rosa-simulate, rosa-generate-config, rosa-showmap, rosa-trace-dist, rosa-evaluate, rosa-explain). 
2. Kod incelemesiyle doğrulandı: src/fuzzer/ klasöründe sadece aflpp.rs var, alternatif/hafif bir backend yok - yani gerçek bir tespit kampanyası zorunlu olarak AFL++ fuzzer'ına bağımlı. AFL++'ın derlenmesi (patch'ler, saatler sürebilecek fuzzing kampanyası) bugün için kapsam dışı bırakıldı. Sonuç: derleme başarısı doğrulandı, tam çalıştırma AFL++ bağımlılığı nedeniyle ertelendi.
3. 3.hafta reproduction çalışmasının nihai durumu netleşti: 10 araçtan 8'i tam sonuçla doğrulandı (FFXE, AutoFirm, PEMU, UEFI Memory Forensics, FirmRCA, UniBOM, Pack-ALM ve önceki günden FFXE), 1'i (ROSA) kısmi doğrulandı (derleme başarılı, çalıştırma AFL++ bağımlılığından ertelendi), 1'i (ChkUp) Python 3.6/Ghidra uyumluluk riski nedeniyle hiç denenmedi.
Takip tablosu (literatur-arac-sonuc-tablosu.xlsx) ROSA'nın kısmi sonucuyla güncellendi.

**Notlar / Sonraki Adımlar:**
- Uçtan uca entegrasyon testi (13. gün) - tüm sistemin sıfırdan, temiz bir ortamda baştan sona test edilmesi

## 05.08.2026

**Yapılanlar:**

1. Tüm sistemin uçtan uca entegrasyon testi yapıldı - kod değişikliği içermeyen, tamamen doğrulama amaçlı bir gündü

2. Komut satırı katmanları sıfırdan doğrulandı
   - static_integrity.py, entropy_analysis.py, yara_scan.py, permission_analysis.py, scoring.py, timeline.py sırayla çalıştırıldı
   - Sonuç: hepsi hatasız çalıştı, scoring.py ve timeline.py beklenen 100/100 skorunu ve 7 bulguyu doğru şekilde verdi

3. CVE testleri doğrulandı
   - hash_truncation_demo.py: tam hash ile kısaltılmış hash arasındaki ~4.1x10^62 kat fark tekrar doğrulandı
   - hardcoded_credential_test.py: admin:admin ve password= eşleşmeleri doğru şekilde tespit edildi

4. Streamlit arayüzü 3 farklı senaryoyla test edildi
   - Senaryo A (özdeş dosya, sıfır bulgu): doğru çalıştı
   - Senaryo B (iki farklı gerçek OpenWrt sürümü, yoğun bulgu): doğru çalıştı, 100/100 skor ve 1335 bulgu üretildi
   - Senaryo C (bilinçli olarak bozuk dosya): uygulama çökmedi, düzgün hata mesajı gösterildi

5. Senaryo B'den indirilen HTML rapor incelendi
   - Başlık, oluşturulma zamanı, özet kartları, "Rapor Kayıtlarının Bütünlüğü" mesajı, bulgular tablosu ve zaman çizelgesi/delil hash'leri tablosu tek tek kontrol edildi
   - Tüm bölümlerin doğru ve eksiksiz göründüğü doğrulandı

**Sonuç:**
Sistem, komut satırından arayüze kadar tüm bileşenleriyle uçtan uca test edildi. Hem normal hem uç durumlar (özdeş dosya, yoğun fark, bozuk dosya) başarıyla doğrulandı. Temiz bir klasöre yeniden klonlayarak sıfırdan deneme adımı, kapsamlı olduğu için 19. güne (son regresyon testi) ertelendi.


**Literatür Taraması (paralel görev):**
**Yapılanlar:**

1. P04 (ChkUp) ikinci kez denendi. angr==9.2.6 dahil tüm bağımlılıklar başarıyla kuruldu — Python 3.6 zorunluluğunun göründüğü kadar katı olmadığı ortaya çıktı. numpy 2.0'ın angr ile uyumsuzluğu tespit edilip çözümü bulundu (numpy<2.0 + runtime restart). Ancak Colab bağlantısı gün boyunca defalarca koptuğu için tam çalıştırmaya geçilemedi. Ghidra 10.1.2 indirildi, Java 11 kuruldu. Sonuç: teknik engel yok, sadece ortam kararsızlığı nedeniyle tamamlanamadı.
2. 10 makalenin tamamı için bildiri taslağına referans olacak bir belge (literatur-bildiri-notlari.md) hazırlandı — her makalenin projeyle örtüşen/eksik/tamamlayıcı yönleri ve test bulguları özetlendi, genel sentez (İlgili Çalışmalar bölümü taslağı) eklendi.
3. ROSA ve Pack-ALM'in güncel Colab not defterleri GitHub'a yüklendi.

Sonuç:
Literatür taraması paralel görevinde bildiri taslağı için gerekli sentez malzemesi hazırlandı. ChkUp'ın tam çalıştırılması hâlâ eksik ama teknik değil ortamsal bir engelden kaynaklanıyor, ileride hızlıca tamamlanabilir durumda.
**Notlar / Sonraki Adımlar:**
- README'nin son hâli ve LICENSE dosyası (14. gün)

## 06.08.2026

**Yapılanlar:**

1. README.md tamamen güncellendi
   - Tüm analiz katmanları ve FR (fonksiyonel gereksinim) tablolarına Durum sütunu eklendi, hepsi ✅ olarak işaretlendi
   - Kullanım bölümü, gerçek ve çalışan komutlarla güncellendi (streamlit run app.py dahil)
   - Değerlendirme bölümü eklendi: iki gerçek CVE değerlendirmesine (CVE-2024-54143, CVE-2024-9643) referans veriliyor
   - Literatür Taraması bölümü, doğru terminolojiyle güncellendi (10 kodlu makale, 1 tanesi veri seti olduğu için ayrı değerlendirildi, kalan 9 araçtan 8 tam 1 kısmi doğrulandı)

2. LICENSE dosyası eklendi
   - Projenin eğitim/staj amaçlı geliştirildiğini, ticari kullanım için izin gerektiğini belirten bir lisans metni oluşturuldu

3. Test paketine başlandı (pytest)
   - tests/ klasörü oluşturuldu
   - tests/test_static_integrity.py yazıldı: 5 test - hash hesaplamasının deterministik olduğu, eklenen/değiştirilen/silinen dosyaların doğru tespit edildiği, değişiklik olmayan senaryoda hiç bulgu çıkmadığı
   - Testler tamamen izole, geçici (temporary) dizinler kullanıyor - gerçek firmware verisine ihtiyaç duymadan çalışıyor

4. Testler çalıştırıldı: pytest tests/ -v → 5/5 PASSED

**Sonuç:**
Proje dokümantasyonu (README, LICENSE) tamamlandı. Otomatik test paketine başlandı - statik bütünlük katmanının tüm senaryoları artık otomatik doğrulanabiliyor.

**Literatür Taraması (paralel görev):**
**Yapılanlar:**

1. P04 (ChkUp) son kez ele alındı. Colab'ın sistem genelindeki numpy sürümünü düşürmenin diğer önceden derlenmiş paketlerle (scipy vb.) ikili uyumsuzluk yarattığı görüldü — bunun yerine izole bir Python venv (/content/chkup_venv) kuruldu. Venv içinde sırasıyla pycparser==2.21, güncel setuptools, js2py'de küçük bir bytecode uyumluluk yaması, np.bool/np.float_ sürüm çakışmaları düzeltildi. Sonuç: angr 9.2.6 sorunsuz import edildi — ChkUp'ın Python 3.6 zorunluluğu efsanesi tamamen çürütüldü.
2. Gerçek çalıştırma denemesinde script'in sessizce hiçbir iş yapmadan bittiği görüldü. Kod incelemesiyle kök neden bulundu: ChkUp'ın kendi Utils.getRoot() fonksiyonu, verilen path zaten "-root" ile bitince onu bir liste yerine düz string olarak döndürüyor — bu da ana döngünün stringi karakter karakter gezip hiçbir şey bulamamasına yol açıyor. Bu, ChkUp'ın kendi kodunda tespit edilmiş orijinal bir bulgu.
3. ChkUp'ın nihai durumu "Tamamlandı (kısmi bulgu)" olarak işaretlendi — Python bağımlılık zincirinin tamamen çözülmesi ve kod incelemesiyle gerçek bir bug tespiti, ROSA/AutoFirm ile tutarlı bir kısmi doğrulama sağladı.
Takip tablosu (literatur-arac-sonuc-tablosu.xlsx) ChkUp'ın nihai durumuyla güncellendi. İki özet grafik üretildi: durum dağılımı (6 tam / 3 kısmi bulgu / 1 veri seti) ve araç başına çalışma süresi karşılaştırması (log ölçek). Bunlarla birlikte 3. hafta reproduction çalışması ve planlanan tüm adımlar (çaprazlama, tablo, grafikleştirme) tamamlandı.

**Notlar / Sonraki Adımlar:**
- Kalan katmanların testleri (entropi, YARA, izin/yetki, skorlama) ve bir uçtan uca entegrasyon testi yazılacak (15. gün)