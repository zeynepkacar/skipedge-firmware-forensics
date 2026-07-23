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

**Notlar / Sonraki Adımlar:**
- Skorlama katmanı tamamlandı - 6 katmanlı sistemin 5.'si bitti
- Sırada: zaman çizelgesi (timeline) oluşturma ve delil zinciri (chain of custody, SHA-256 tabanlı) belgeleme katmanı