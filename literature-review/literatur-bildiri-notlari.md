# Literatür Taraması — Bildiri Taslağı için Referans Notları

**Proje bağlamı:** Gömülü sistem firmware bütünlük ihlali tespiti ve adli bilişim analiz aracı. Katmanlar: statik bütünlük karşılaştırma, entropi analizi, YARA kural taraması, izin/yetki analizi, zaman çizelgesi + delil zinciri, PDF/HTML rapor çıktısı. Yaklaşım: iki firmware imajını (orijinal vs şüpheli) karşılaştırarak tahrifat kanıtı üretmek.

Bu belge, incelenen 10 makalenin her biri için: (1) ne yaptığı, (2) projeyle örtüşen yönler, (3) projeden eksik/farklı olan yönler, (4) reproduction sırasında elde edilen somut bulgu özetleniyor.

---

## P01 — FFXE
**Ne yapıyor:** Cortex-M gömülü firmware ikililerinden dinamik zorlamalı yürütme (forced execution) ile kontrol akış grafiği (CFG) çıkarıyor; özellikle asenkron kayıtlı kesme işleyicilerine (interrupt handler) dolaylı çağrıları çözüyor.

**Projeyle örtüşen yön:** Her ikisi de gömülü/embedded firmware ikilileriyle çalışıyor, ikisi de statik+dinamik analiz sınırında.

**Projeden eksik/farklı yön:** FFXE bütünlük/tahrifat tespiti yapmıyor — amacı analiz/keşif (CFG haritası çıkarmak), karşılaştırma değil. Projede olmayan bir yetenek: kontrol akışı düzeyinde firmware iç yapısını haritalama. Bildiriye eklenebilir: "gelecek çalışma olarak CFG farkı, iki firmware sürümü arasında sadece byte-seviyesi değil, kontrol-akışı seviyesinde de tahrifat tespiti sağlayabilir."

**Test bulgusu:** 9/9 real-world örnek (ChargeHR, Flex, Switchmate) hatasız çalıştı, ortalama ~23sn/firmware. Makale iddiası tam doğrulandı, sorunsuz reproduction.

---

## P02 — ROSA
**Ne yapıyor:** AFL++ tabanlı fuzzing + metamorfik oracle ile ikili programlarda arka kapı (backdoor) tespiti.

**Projeyle örtüşen yön:** İkisi de "kötü niyetli/beklenmeyen davranış" tespiti hedefliyor, ikisi de ikili program analizi.

**Projeden eksik/farklı yön:** ROSA çalışma-zamanı davranışsal tespit (fuzzing ile runtime anomali), proje ise statik/karşılaştırmalı tespit. ROSA'nın hedefi "arka kapı" (spesifik gizli fonksiyonellik), proje ise "genel tahrifat/bütünlük ihlali" — daha geniş bir tehdit sınıfı. Bildiride fark: "ROSA'nın dinamik/fuzzing yaklaşımı, projenin statik yaklaşımına kıyasla daha derin ama çok daha yavaş/pahalı bir tespit sağlıyor."

**Test bulgusu (kısmi):** Rust çekirdeği (cargo build --release) AFL++ olmadan başarıyla derlendi. Ancak kod incelemesiyle doğrulandı ki gerçek tespit kampanyası zorunlu olarak AFL++ fuzzer'ına bağımlı (src/fuzzer/ altında tek backend). Tam çalıştırma denenemedi — derleme başarısı ile sınırlı doğrulama.

---

## P03 — AutoFirm
**Ne yapıyor:** IoT firmware'lerinde büyük ölçekte yeniden kullanılan kütüphaneleri ve versiyonlarını binwalk+QEMU emülasyonu ile otomatik tespit ediyor.

**Projeyle örtüşen yön:** İkisi de firmware içeriğini (dosya sistemi, binary'ler) analiz ediyor, ikisi de binwalk kullanıyor/kullanabiliyor.

**Projeden eksik/farklı yön:** AutoFirm kütüphane/versiyon envanteri çıkarıyor (bir çeşit SBOM), proje bunu yapmıyor — bu doğrudan bir **eksik/genişletme fırsatı**: projeye "bilinen kütüphane versiyonu tespiti" katmanı eklenebilir (bkz. P28 UniBOM ile de örtüşüyor).

**Test bulgusu (önemli sınırlama):** OpenWrt (modern Linux) firmware'inde qemu emülasyonu çalıştı ama regex tabanlı versiyon çıkarma mantığı eşleşme bulamadı — araç klasik vendor firmware (TP-Link, Netgear tarzı) regex'lerine göre tasarlanmış, modern/minimal Linux dağıtımlarında genelleşmiyor. **Bildiride kullanılabilir bulgu:** "mevcut kütüphane-tespit araçları modern firmware ekosistemlerinde genelleşme sorunu yaşıyor" — projenin YARA kural tabanlı yaklaşımı da benzer bir genelleşme riskiyle karşı karşıya, bu bir ortak kısıt.

---

## P04 — ChkUp
**Ne yapıyor:** Firmware güncelleme prosedürlerindeki doğrulama adımlarını (authenticity, integrity, freshness, compatibility) tespit edip eksik/hatalı doğrulama zafiyetlerini buluyor.

**Projeyle EN GÜÇLÜ örtüşen makale:** İkisi de "firmware bütünlüğü" temalı. Ama açı tamamen farklı:
- **ChkUp** = tasarım-zamanı analiz — "bu firmware'in güncelleme mekanizması güvenli mi tasarlanmış?" (üretici tarafının ürettiği güncelleme sürecini denetliyor)
- **Proje** = post-hoc adli analiz — "bu firmware imajı elimdeki referanstan tahrif edilmiş mi?" (bir analistin elindeki iki dosyayı karşılaştırması)

**Bildiride kullanılabilir çerçeve:** "ChkUp önleyici (preventive) bir yaklaşım sunarken, bu proje tespit edici (detective/forensic) bir yaklaşım sunuyor — ikisi birlikte firmware bütünlüğü sorununun farklı aşamalarını (tasarım vs. olay-sonrası adli analiz) kapsıyor."

**Test durumu:** Ghidra 10.1.2 + Java 11 + Python 3.6 zorunluluğu nedeniyle reproduction denenemedi (uyumluluk riski yüksek görüldü).

---

## P10 — PEMU
**Ne yapıyor:** Rehosting platformlarına (SEmu, Fuzzware, Hoedur) eklenti olarak çalışan, protokol-farkındalıklı paket üretimiyle gömülü ağ yığınlarını fuzzlayan bir araç.

**Projeyle örtüşen yön:** Sınırlı — ikisi de gömülü sistem güvenliği alanında ama PEMU ağ protokolü fuzzing'i, proje statik dosya analizi.

**Projeden eksik/farklı yön:** Proje ağ trafiği/protokol analizi yapmıyor. PEMU'nun kapsamı (network-facing firmware güvenliği) projenin kapsamı dışında — bildiride "kapsam dışı ama ilişkili alan" olarak kısaca değinilebilir.

**Test bulgusu:** Çekirdek `Packer` sınıfı izole test edildi, gerçek Ethernet+ARP paketi (42 byte, doğru ethertype) üretildi — protokol farkındalıklı paket üretme motoru doğrulandı.

---

## P17 — UEFI Memory Forensics
**Ne yapıyor:** UEFI bellek döküntülerinden (memory dump) yüklü imajları "carving" ile çıkarıp inline/trampoline hook, pointer hooking gibi tehditleri tespit eden bir adli bilişim çerçevesi.

**Projeyle EN YAKIN ikinci makale (adli bilişim ortak temeli):** İkisi de "forensics" kelimesini taşıyor, ikisi de imza/yapı tabanlı tespit (signature-based carving vs. YARA kuralları) kullanıyor.

**Fark:** UEFI Memory Forensics **çalışma zamanı bellek** üzerinde çalışıyor (canlı sistem ya da bellek dökümü), proje ise **statik firmware dosyası** üzerinde. Bildiride: "bu proje disk/flash düzeyinde statik adli analiz sağlarken, UEFI Memory Forensics çalışma zamanı bellek düzeyinde tamamlayıcı bir adli analiz sağlıyor — ileride ikisinin birleştirilmesi (statik + runtime forensics) daha kapsamlı bir tespit hattı oluşturabilir."

**Test bulgusu:** Gerçek QEMU dump'ı yerine, kaynak koddaki gerçek imza/offset ile sentetik dump inşa edildi — imza tarama + doğrulama mantığı (1/1 doğru tespit, 0 red) doğrulandı.

---

## P20 — FirmRCA
**Ne yapıyor:** Fuzzing sonrası (post-fuzzing) ARM gömülü firmware'lerde olay-tabanlı hata lokalizasyonu — bir crash'in kök nedenini tersine yürütme (reverse execution) ile buluyor.

**Projeyle örtüşen yön:** İkisi de gömülü ARM firmware analiz ediyor, ikisi de "bir olayın nedenini bulma" (kök neden vs. tahrifat kanıtı) motivasyonuna sahip.

**Projeden eksik/farklı yön:** FirmRCA bir **crash'in** kök nedenini buluyor (yazılım hatası/güvenlik açığı bağlamı), proje bir **dosyanın tahrif edilip edilmediğini** buluyor (bütünlük bağlamı) — farklı problem sınıfları, teknik olarak ilişkisiz ama ikisi de "kanıta dayalı, adım adım izlenebilir sonuç" üretme felsefesini paylaşıyor (proje: zaman çizelgesi + delil zinciri; FirmRCA: taintli komut listesi + adres/assembly çıktısı).

**Test bulgusu:** 168.542 komutluk tersine yürütme tamamlandı (~25dk), 53 taintli komut + 69 taint çifti tespit edildi — kök neden analizi tam çalışır durumda doğrulandı.

---

## P25 — LFwC (Linux Firmware Corpus)
**Ne yapıyor:** Araç değil, büyük ölçekli (354GB, 10.913 firmware imajı) bir Linux firmware veri seti/benchmark kaynağı.

**Projeyle ilişkisi:** Projenin değerlendirme/test aşamasında kullanılabilecek potansiyel bir kaynak — büyük ölçekte gerçek dünya firmware'leriyle projenin doğruluğunu (false positive/negative oranı) test etmek için ideal olurdu.

**Durum:** Erişim akademik başvuru + 354GB indirme gerektiriyor, bu çalışmada kullanılamadı. Yerine AutoFirm testinde OpenWrt'nin resmi sitesinden küçük gerçek bir firmware kullanıldı. **Bildiride not:** "gelecek çalışma olarak, projenin LFwC gibi büyük ölçekli bir korpus üzerinde değerlendirilmesi doğruluk iddialarını güçlendirecektir."

---

## P28 — UniBOM
**Ne yapıyor:** SBOM (Software Bill of Materials) üretimi + bilinen zafiyet (CVE) taraması — syft ile bileşen envanteri, grype ile zafiyet eşleştirme.

**Projeyle örtüşen yön (genişletme fırsatı, P03 ile birlikte):** Proje şu an "bu dosya değişmiş mi" sorusuna cevap veriyor ama "bu dosyada bilinen bir CVE var mı" sorusuna cevap vermiyor. UniBOM'un pipeline'ı (SBOM + CVE) doğrudan projeye eklenebilecek bir katman.

**Bildiride kullanılabilir çerçeve:** Projenin mevcut katmanları (statik bütünlük, entropi, YARA, izin) + potansiyel yeni katman (SBOM/CVE, UniBOM'dan esinlenerek) = daha kapsamlı bir tehdit modeli. Bu, "gelecek çalışma" bölümü için somut ve teknik olarak temellendirilmiş bir öneri olur.

**Test bulgusu:** OpenWrt dosya sisteminde 338 bileşen (SBOM) tespit edildi, 8 gerçek zafiyet bulundu (1 kritik) — pipeline uçtan uca doğrulandı.

---

## P29 — Pack-ALM
**Ne yapıyor:** RoBERTa tabanlı bir dil modeli ile ikili dosya bölümlerinin paketlenmiş (packed/obfuscated) olup olmadığını sınıflandırıyor.

**Projeyle örtüşen yön (doğrudan tamamlayıcı):** Projenin **entropi katmanı**, paketleme/şifrelemeyi yüksek entropi ile *dolaylı* tespit ediyor (entropi bir vekil/proxy metrik). Pack-ALM ise öğrenilmiş bir model ile *doğrudan* sınıflandırma yapıyor.

**Bildiride kullanılabilir çerçeve:** "Projenin entropi tabanlı paketleme tespiti, Pack-ALM gibi öğrenilmiş modellerle karşılaştırıldığında daha basit ama daha az hassas (yanlış pozitif/negatife açık) olabilir — gelecekte entropi katmanının yanına ML tabanlı bir sınıflandırıcı eklenmesi doğruluğu artırabilir." Bu, entropi katımının sınırlarını tartışırken doğrudan literatürle temellendirme sağlıyor.

**Test bulgusu:** Checkpoint (RoBERTa-base, 12 katman) gerçek eğitilmiş ağırlıklarla yüklendi (0 eksik/0 beklenmeyen), forward pass ile gerçek [1,20,768] çıktı üretildi — modelin çalışır durumda olduğu doğrulandı.

---

## Genel Sentez (Bildiri Giriş/İlgili Çalışmalar bölümü için taslak)

Literatürdeki 10 çalışma dört gruba ayrılabilir:

1. **Analiz/keşif araçları** (FFXE, PEMU) — firmware'in iç yapısını/davranışını haritalıyor, bütünlük tespiti yapmıyor
2. **Doğrudan ilişkili bütünlük/güvenlik araçları** (ChkUp, ROSA) — ChkUp tasarım-zamanı, proje olay-sonrası; ROSA davranışsal, proje statik
3. **Adli bilişim araçları** (FirmRCA, UEFI Memory Forensics) — farklı substrat (crash kök nedeni / çalışma zamanı bellek) ama ortak "kanıta dayalı iz sürme" felsefesi
4. **Genişletme/tamamlama fırsatı sunan araçlar** (AutoFirm, UniBOM, Pack-ALM) — bu üçü projeye doğrudan eklenebilecek yeni katmanlar öneriyor: kütüphane/versiyon tespiti, SBOM+CVE taraması, öğrenilmiş paketleme sınıflandırması

**Projenin literatürdeki konumu:** Mevcut araçların çoğu ya saldırı/zafiyet keşfine (ROSA, PEMU, FirmRCA) ya da geliştirici-tarafı doğrulamaya (ChkUp) odaklanmışken, bu proje **analist-tarafı, post-hoc, karşılaştırmalı bir adli bilişim aracı** sunarak farklı ve daha az doldurulmuş bir boşluğu hedefliyor — özellikle iki firmware imajı arasında delil zincirini koruyarak fark analizi yapma yaklaşımı, incelenen 10 makale arasında doğrudan bir emsali olmayan bir katkı.
