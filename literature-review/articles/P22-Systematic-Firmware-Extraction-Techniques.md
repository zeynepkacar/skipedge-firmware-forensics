# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P22 |
| Başlık | Systematic firmware extraction techniques for forensic analysis of industrial embedded devices |
| Yazarlar | Erwin Karincic, Lauren Linkous, Alexander Will, Carl Elks, Milos Manic, Erdem Topsakal (Virginia Commonwealth University, ABD) |
| Yıl | 2026 |
| Yayın Yeri (Venue) | Forensic Science International: Reports (Elsevier), Cilt 14, Makale No: 100492 |
| DOI / Link | 10.1016/j.fsir.2026.100492 — açık erişim (CC BY-NC 4.0) |
| Anahtar Kelimeler | Device disassembly, digital forensics, embedded device forensics, firmware extraction, hardware analysis, reverse engineering |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Çoklu mimari — ARM (STM32 Cortex-M4 örneği dahil), x86, MIPS ve PowerPC üzerinde test edilmiş; endüstriyel gömülü cihazlar (ağ router'ları, IoT sensörleri, PLC benzeri sistemler) hedefleniyor
- **Analiz Türü:** Donanım-odaklı adli bilişim metodolojisi — statik/dinamik kod analizinden önceki aşama olan fiziksel firmware **edinme (acquisition)** sürecine odaklanıyor; UART, JTAG, SWD, SPI, I2C arayüzleri üzerinden hem yıkıcı olmayan hem de yıkıcı (destructive) çıkarma teknikleri sunuyor
- **Tespit Edilen Tehdit Türü:** Doğrudan bir zafiyet/tehdit tespiti değil — cihaz söküm (disassembly), arayüz tanımlama ve firmware çıkarma sürecinin adli olarak sağlam (forensically sound) şekilde nasıl yürütüleceğini standartlaştırıyor; Stuxnet, Industroyer, Triton gibi endüstriyel malware örnekleriyle motivasyonu gerekçelendiriyor
- **Kullanılan Ana Teknik/Algoritma:** 4 aşamalı metodoloji — (1) kritik bileşen tanımlama ve cihaz söküm, (2) arayüz tanımlama (board etiketleri, pin gruplamaları, debug port'lara yakınlık), (3) enstrümantasyon taksonomisi (JTAG enumerator'lar, lojik/protokol analizörleri, debug board'lar — Bus Pirate/Tigard/Glasgow, genel amaçlı SBC'ler, yazılım arayüz araçları — OpenOCD/UrJTAG/flashrom/i2c-tools), (4) protokole özgü çıkarma teknikleri (UART konsol dump, JTAG/EJTAG ile flash dump, SWD ile DAP tabanlı okuma, SPI flashrom, I2C i2cdump); ayrıca modern anti-forensics (RDP/CRP bypass, voltage/EM fault injection, encrypted firmware) karşı önlemleri ve NIST SP 800-86 uyumlu delil zinciri/raporlama kriterlerini tartışıyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Kendi test cihazları — tüketici sınıfı ağ router'ları/IoT sensörleri ile temsili endüstriyel gömülü cihazlar; üretici kimlikleri gizlilik sözleşmeleri (NDA) nedeniyle açıklanmamış
- **Veri Seti Erişilebilir mi?** Hayır — cihaz kimlikleri ve ham firmware imajları paylaşılmamış
- **Kaynak Kod Açık mı?** Hayır (kendi özgün bir kodu yok) — ancak makale, kullanılan tüm araçların (JTAGulator, JTAGenum, blueTag, OpenOCD, UrJTAG, flashrom, i2c-tools, Binwalk) halka açık/açık kaynaklı olduğunu belirtiyor ve komut örnekleri veriyor

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tekil cihazdan firmware çıkarma metodolojisi, imaj karşılaştırması içermiyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Kısmen | Birden fazla fiziksel arayüz/araç kategorisini (JTAG, UART, SPI, I2C, SWD) tamamlayıcı şekilde birleştiriyor, ama tek bir katman olan "edinme" aşamasında |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Evet | Makalenin güçlü yönlerinden biri — NIST SP 800-86 uyumlu belgeleme, cihaz kimlik kaydı, her komut/yanıtın kaydedilmesi, anlık hashleme, sızdırmaz referans kopya saklama, kısmi dump'ların birleştirme prosedürü ayrıntılı şekilde tanımlanmış |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok, çıktısı ham firmware imajı |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Kısmen | Endüstriyel kontrol sistemlerine yönelik tedarik zinciri saldırıları (Stuxnet'in PLC'lere bulaşması, üçüncü taraf kütüphane kullanımı istatistikleri — Linux kernel kodunun %22.3'ünün önceki implementasyonlardan geldiği) motivasyon bölümünde tartışılıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "firmware edinme" ön ucuna doğrudan uygulanabilir bir fiziksel çıkarma metodolojisi sunuyor; özellikle NIST SP 800-86 uyumlu delil zinciri ve adli raporlama bölümü (6.7-6.8), projenin adli bilişim (delil zinciri) katmanı için doğrudan bir çerçeve teşkil edebilir. Enstrümantasyon taksonomisi tablosu (Tablo 1) da hangi aracın hangi arayüz için kullanılacağına dair pratik bir referans sağlıyor.
- **Eksik bıraktığı nokta (Gap):** Yazılım zafiyet tespiti (statik/dinamik kod analizi) içermiyor — sadece firmware'in fiziksel olarak nasıl elde edileceğine odaklanıyor; skorlama mekanizması yok; fiziksel cihaz erişimi gerektiriyor (uzaktan/sadece-binary senaryolara uygulanamaz).
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** Hakemli (Elsevier, Forensic Science International: Reports), 2026'da yayınlanmış, açık erişim (CC BY-NC). NIST SP 800-86, 800-82, 800-101, NISTIR 8428 gibi standartlarla uyumlu; anti-forensics (fault injection, encrypted storage) karşı yöntemleri de kapsamlı şekilde ele alıyor.
