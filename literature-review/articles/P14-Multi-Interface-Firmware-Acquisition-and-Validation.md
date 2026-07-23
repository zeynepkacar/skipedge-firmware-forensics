# Makale İnceleme Şablonu — P14

## 1. Künye ve Meta Veri

| Alan | Bilgi |
|---|---|
| Makale ID | P14 |
| Başlık | A Multi-Interface Firmware Acquisition and Validation Methodology for Low-Cost Consumer Drones: A Case Study on Three Holy Stone Platforms |
| Yazarlar | Sandesh More, Sneha Sudhakaran, Marco Carvalho |
| Yıl | 2026 (preprint, Mayıs 2026) |
| Venue | arXiv preprint; Internet of Things (Elsevier, ISSN 2542-6605) dergisine gönderilmek üzere hazırlanan taslak |
| DOI / Link | arXiv:2605.11040 — https://arxiv.org/abs/2605.11040 |
| Anahtar Kelimeler | consumer UAV, drone firmware, embedded systems security, entropy analysis, firmware extraction, IoT security, SPI flash, SWD/JTAG, UART |

## 2. Teknik Analiz ve Metodoloji

| Alan | Bilgi |
|---|---|
| Hedef Mimari | Tüketici drone uçuş kontrolcüleri — MM32F103 (ARM Cortex-M0, HS175D); HS720/HS360S'te MCU probe edilmemiş; harici SPI NOR flash çipleri (XTX XT25F128F-W, XMC XM25QH64C, Macronix MX25L6433F) |
| Analiz Türü | Çıkarım-sonrası (post-acquisition) statik analiz — sliding-window Shannon entropi profili + binwalk yapısal imza analizi + EMBA statik analiz (SBOM, CVE korelasyonu, binary hardening değerlendirmesi) |
| Tespit Edilen Tehdit Türü | Bozuk/eksik/sahte firmware dump tespiti (araç düzeyinde "başarılı" rapor edilen ama içerik olarak boş/geçersiz görüntüler — HS360S örneği); ayrıca dump içeriğinde tespit edilen güvenlik zafiyetleri: şifrelenmemiş TEE imajı, ömrünü tamamlamış (EOL) çekirdek, binary hardening eksikliği |
| Ana Teknik / Algoritma | Üç katmanlı doğrulama çerçevesi: Tier 1 — boyut kontrolü (deklare edilen flash kapasitesiyle eşleşme), Tier 2 — SHA-256 hash tekrarlanabilirliği (tekrarlı okumalar arası bitwise tutarlılık), Tier 3 — sliding-window Shannon entropi + binwalk yapısal analiz uyumu; ayrıca çoklu arayüz çapraz doğrulama (SPI vs SWD vs UART) |

## 3. Veri Seti ve Tekrarlanabilirlik

| Alan | Bilgi |
|---|---|
| Veri Seti | 3 Holy Stone drone modelinden (HS175D, HS720, HS360S) SPI/SWD/UART üzerinden elde edilen firmware dump'ları; SHA-256 hash'leri ve offset bazlı yapısal imzalar makalede raporlanmış |
| Erişilebilir mi | Makalede açıkça belirtilmemiş — dump görüntülerinin veya veri setinin kamuya açık bir deposu için link verilmemiş |
| Kaynak Kod Açık mı | Kontrol edilmedi — makalede kendilerine ait bir GitHub/repo linki bulunmuyor; kullanılan araçlar (flashrom, OpenOCD, binwalk, EMBA) üçüncü parti açık kaynak araçlar |

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
|---|---|---|
| Diferansiyel Analiz | Yok | Tek cihazdan alınan dump'lar analiz ediliyor; iyi huylu/kötü huylu firmware karşılaştırması yapılmıyor |
| Çok Katmanlı Analiz | Var | Üç katmanlı (boyut / hash / entropi+yapısal) doğrulama çerçevesi projenin metodolojisine çok yakın |
| Delil Zinciri | Kısmen | SHA-256 hashleme ve metadata loglama (arayüz, fikstür, güç kaynağı) var; ancak formal chain-of-custody modeli yok |
| Tek Şüphe Skoru | Yok | Pass/fail (validated / incomplete) ikili karar; sürekli/olasılıksal şüphe skoru üretilmiyor |
| Tedarik Zinciri / İç Tehdit | Kısmen | Tedarik zinciri odaklı değil; fiziksel donanım erişimi ve çıkarım güvenliği bağlamında dolaylı ilişki var |

## 5. Değerlendirme

| Alan | Bilgi |
|---|---|
| Katkı | Projenin "statik bütünlük + entropi + CVE değerlendirme" katmanlarına metodolojik olarak en yakın çalışmalardan biri; flashrom'un araç-düzeyinde "başarılı" raporunun veri bütünlüğünü garanti etmediğini somut bir örnekle (HS360S) gösteriyor — projenin "tool-level success ≠ gerçek bütünlük" argümanı için güçlü destek sağlıyor |
| Gap | Tek üretici (Holy Stone) ve üç modelle sınırlı; şifreli/imzalı bootloader senaryosu test edilmemiş; runtime/dinamik bütünlük kontrolü kapsam dışı; kod/veri seti paylaşım durumu belirsiz |
| Uygunluk Skoru (1-5) | 5 |
| Ek Notlar | Üç katmanlı doğrulama çerçevesi ve entropi + binwalk + EMBA kombinasyonu projenin çekirdek metodolojisiyle doğrudan örtüşüyor; entropi eşik değerleri (yüksek: 7,0 bits/byte, düşük: 1,0 bits/byte) doğrudan referans alınabilir. EMBA'nın CVE korelasyonu ve binary hardening değerlendirmesi projenin "değerlendirme" fazına entegre edilebilir |
