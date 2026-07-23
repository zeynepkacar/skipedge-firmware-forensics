# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P28 |
| Başlık | UniBOM – A Unified SBOM Analysis and Visualisation Tool for IoT Systems and Beyond |
| Yazarlar | Vadim Safronov, Andrew Martin (Oxford Üniversitesi, İngiltere), Ionut Bostan, Nicholas Allott (NquiringMinds, Southampton, İngiltere) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | ACM IoT 2025 (15. Uluslararası Internet of Things Konferansı, Viyana) |
| DOI / Link | 10.1145/3770501.3770512 — arXiv:2511.22359 |
| Anahtar Kelimeler | SBOM (Software Bill of Materials), IoT firmware, CVE tarama, binwalk, Syft, Grype |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Gerçek dünya router firmware'leri — OpenWrt tabanlı ve TRENDnet cihazları dahil çoklu mimari
- **Analiz Türü:** Statik — firmware imajından bileşen envanteri (SBOM) çıkarma ve bilinen zafiyet (CVE) taraması
- **Tespit Edilen Tehdit Türü:** Firmware içindeki üçüncü taraf bileşenlerdeki bilinen zafiyetler (CVE) — tedarik zinciri şeffaflığı odaklı
- **Kullanılan Ana Teknik/Algoritma:** Boru hattı (pipeline) yaklaşımı — binwalk ile firmware açma/çıkarma, Syft ile SBOM (yazılım malzeme listesi) üretimi, CCScanner ile bileşen/kütüphane tespiti, Grype ile SBOM üzerinden CVE eşleştirme; sonuçların birleşik bir görselleştirme arayüzünde sunulması

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** 258 gerçek router firmware imajı (OpenWrt ve TRENDnet cihazları dahil)
- **Veri Seti Erişilebilir mi?** Kısmen — OpenWrt firmware'leri halka açık kaynaklardan derlenebilir; TRENDnet gibi ticari ürünler ayrıca veri seti olarak paylaşılmamış
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/nqminds/UniBOM) — Docker paketli, açık kaynak CLI aracı

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek firmware imajından SBOM/CVE çıkarımı yapıyor, imaj karşılaştırması değil |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | binwalk (açma) + Syft (SBOM üretimi) + CCScanner (bileşen tespiti) + Grype (CVE eşleştirme) olmak üzere 4 farklı aracın birleştirildiği bir boru hattı |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok, çıktısı SBOM + eşleştirilen CVE listesi (görselleştirilmiş) |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Evet | Makalenin ana odağı — SBOM üretimi doğrudan tedarik zinciri şeffaflığı ve üçüncü taraf bileşen risklerini hedefliyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "değerlendirme (CVE testi)" katmanına doğrudan uygulanabilir hazır bir araç zinciri sunuyor — binwalk+Syft+CCScanner+Grype pipeline'ı, projenin kendi CVE eşleştirme mekanizmasını tasarlarken referans/karşılaştırma noktası olarak kullanılabilir. 258 firmware imajı üzerindeki büyük ölçekli değerlendirmesi de, projenin kendi veri setini genişletmek için bir kaynak olabilir.
- **Eksik bıraktığı nokta (Gap):** Statik bütünlük (hash), entropi, YARA imza tarama gibi katmanları içermiyor; delil zinciri/skorlama gibi adli bilişim unsurları yok; sadece bilinen (CVE veritabanında kayıtlı) zafiyetleri tespit ediyor, sıfırıncı gün (zero-day) veya özel/proprietary bütünlük ihlallerini kapsamıyor.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** ACM IoT 2025'te kabul edilmiş, hakemli. Kod açık kaynak, Docker ile paketlenmiş, kullanıma hazır. Projenin 8/8 kod teyidi hedefine katkı sağlıyor.
