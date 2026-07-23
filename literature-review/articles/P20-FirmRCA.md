# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P20 |
| Başlık | FirmRCA: Towards Post-Fuzzing Analysis on ARM Embedded Firmware with Efficient Event-based Fault Localization |
| Yazarlar | Boyu Chang, Peiyu Liu, Qiao Zhang, Shouling Ji (Zhejiang Üniversitesi), Binbin Zhao, Raheem Beyah (Georgia Institute of Technology), Yuan Tian (UCLA) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | IEEE Symposium on Security and Privacy (S&P) 2025 |
| DOI / Link | arXiv:2410.18483 — https://arxiv.org/abs/2410.18483 — IEEE Xplore: https://ieeexplore.ieee.org/document/11023509/ |
| Anahtar Kelimeler | fuzzing sonrası analiz (post-fuzzing analysis), ARM gömülü firmware, kök neden analizi (root cause analysis), olay tabanlı (event-based) hata lokalizasyonu |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** ARM gömülü firmware
- **Analiz Türü:** Dinamik — fuzzing sonrası çökme (crash) senaryolarının yeniden üretilmesi sırasında çalışma zamanı olaylarının (event) kaydedilmesi ve analizi
- **Tespit Edilen Tehdit Türü:** Doğrudan bir zafiyet tespiti değil; fuzzing sırasında bulunan çökmelerin kök nedeninin (root cause) otomatik olarak lokalize edilmesi — fuzzing'in "ilk adım" olduğu, kök neden analizinin zaman alıcı "sonraki adım" olduğu vurgulanıyor
- **Kullanılan Ana Teknik/Algoritma:** Olay tabanlı (event-based) footprint toplama yöntemi — çökme senaryosu yeniden üretilirken veri olayları (data events) ve eylem olayları (action events) kaydediliyor; bu yaklaşım, gömülü firmware'in yetersiz debugging mekanizmalarını telafi ediyor ve bellek takma adlarının (memory alias) doğru çözümlenmesini sağlayarak gürültülü/aşırı-kirlenmiş şüpheli talimat listesini daraltıyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Ayrı bir Zenodo deposunda yayınlanmış (DOI: 10.5281/zenodo.15623400) — fuzzing kampanyalarından elde edilen çökme örnekleri ve değerlendirme verileri
- **Veri Seti Erişilebilir mi?** Evet — Zenodo üzerinden halka açık
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/NESA-Lab/FirmRCA) — Zhejiang Üniversitesi NESA Lab'ın resmi deposu, detaylı README, aktif bakım

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | İki firmware imajı karşılaştırması değil, tek bir çökme senaryosunun kök nedenini lokalize ediyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir yöntem: olay tabanlı footprint toplama + kök neden analizi |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Kısmen | Şüpheli talimatları daraltıp sıralıyor (ranking), ama tek bir birleşik "şüphe skoru" değil |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin doğrudan bir katmanı değil (fuzzing sonrası kök neden analizi, statik bütünlük/entropi odaklı projeden farklı), ancak "gürültülü şüpheli talimat listesini daraltma" yaklaşımı, projenin zafiyet doğrulama/önceliklendirme adımına metodolojik bir örnek olarak referans olabilir.
- **Eksik bıraktığı nokta (Gap):** Statik bütünlük (hash), entropi, YARA imza tarama gibi katmanları içermiyor; adli bilişim unsurları (delil zinciri, raporlama, skorlama) yok; fuzzing altyapısına bağımlı, tek başına bir statik analiz aracı değil.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** IEEE S&P 2025'te kabul edilmiş, hakemli. Kod ve veri seti açık ve aktif olarak paylaşılmış (GitHub + Zenodo), tekrarlanabilirlik güçlü. **Not:** Bu makale, önceki bir literatür taraması oturumunda P22 olarak da kaydedilmiş görünüyor — GitHub reponuzdaki articles klasörünü kontrol edip P22 ile çakışma olup olmadığını doğrulamanızı öneririm.
