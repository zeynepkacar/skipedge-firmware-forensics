# Makale İnceleme Şablonu — P13

## 1. Künye ve Meta Veri

| Alan | Bilgi |
|---|---|
| Makale ID | P13 |
| Başlık | Implementation of a Data-Parallel Approach on a Lightweight Hash Function for IoT Devices |
| Yazarlar | Abdullah Sevin |
| Yıl | 2025 |
| Venue | Mathematics (MDPI), Cilt 13, Sayı 5, Makale No. 734 (24 Şubat 2025) |
| DOI / Link | 10.3390/math13050734 (açık erişim, CC BY 4.0) — https://doi.org/10.3390/math13050734 |
| Anahtar Kelimeler | IoT, lightweight cryptography, parallel computing, hash function |

## 2. Teknik Analiz ve Metodoloji

| Alan | Bilgi |
|---|---|
| Hedef Mimari | Genel amaçlı çok çekirdekli platformlar (Intel i7-7700HQ) ve Raspberry Pi 4 (ARM Cortex-A72 dört çekirdek) — IoT senaryosunu temsilen |
| Analiz Türü | Kriptografik hash fonksiyonu tasarımı ve performans/güvenlik (istatistiksel) analizi; doğrudan tehdit/anomali tespiti değil, bütünlük doğrulaması için temel primitif |
| Tespit Edilen Tehdit Türü | Doğrudan bir tehdit tespiti yapılmıyor; çalışma bir hash fonksiyonu önerisi olup çarpışma direnci (collision resistance) ve hassasiyet (avalanche effect) üzerinden veri bütünlüğü garantisi sağlıyor |
| Ana Teknik / Algoritma | SIMON hafif blok şifresi tabanlı, CTR modunda çalışan, ağaç yapısına benzer veri-paralel (data-parallel) hash fonksiyonu (PLWHF); OpenMP ile çoklu iş parçacığı paralelleştirmesi (şifreleme/XOR paralel, birleştirme adımı sıralı) |

## 3. Veri Seti ve Tekrarlanabilirlik

| Alan | Bilgi |
|---|---|
| Veri Seti | 1000 rastgele üretilmiş mesaj (Mersenne Twister — MT19937 ile), çarpışma/hassasiyet/dağılım testleri için; standart bir kamu veri seti kullanılmamış |
| Erişilebilir mi | Hayır — "Data Availability Statement: veriler talep üzerine yazardan temin edilebilir, gizlilik/etik kısıtlama nedeniyle genel erişime kapalı" |
| Kaynak Kod Açık mı | Hayır — makalede kaynak kod (GitHub vb.) linki bulunamadı |

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
|---|---|---|
| Diferansiyel Analiz | Yok | İyi huylu/kötü huylu karşılaştırması yok; saf bir hash fonksiyonu çalışması |
| Çok Katmanlı Analiz | Kısmen | Tek geçişli hash hesaplama; ancak paralel/sıralı hibrit mimari var (şifreleme+XOR paralel, toplama sıralı) |
| Delil Zinciri | Yok | Kapsam dışı |
| Tek Şüphe Skoru | Yok | Bir hash fonksiyonu; anomali/şüphe skoru üretmiyor |
| Tedarik Zinciri / İç Tehdit | Yok | Kapsam dışı |

## 5. Değerlendirme

| Alan | Bilgi |
|---|---|
| Katkı | Diğer hafif hash fonksiyonlarından (SPONGENT, Quark, Photon, Lesamnta, SipHash) en az %20 daha hızlı, BLAKE ile karşılaştırılabilir performans; 2 iş parçacığıyla ~%40, 3 iş parçacığıyla ~%50-55 hızlanma; Raspberry Pi 4 üzerinde somut IoT performans verileri |
| Gap | Saf bir hash fonksiyonu önerisi — bütünlük doğrulama sistemi, tehdit modeli, adli bilişim veya tedarik zinciri bağlamı içermiyor; kaynak kod paylaşılmamış, tekrarlanabilirlik sınırlı |
| Uygunluk Skoru (1-5) | 2 |
| Ek Notlar | Performans ölçüm metodolojisi (mesaj boyutuna göre çalışma süresi, thread sayısına göre hızlanma) "hafif kriptografi performans karşılaştırması" alt bölümünde P12 ile birlikte referans olarak kullanılabilir; projeye doğrudan uygulanabilirlik düşük |
