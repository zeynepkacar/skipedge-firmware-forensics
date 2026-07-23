# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P19 |
| Başlık | Reverse Engineered MiniFS File System |
| Yazarlar | Dmitrii Belimov, Evgenii Vinogradov (Technology Innovation Institute, Abu Dhabi, BAE) |
| Yıl | 2024 |
| Yayın Yeri (Venue) | ACM ARES 2024 (19th International Conference on Availability, Reliability and Security) |
| DOI / Link | 10.1145/3664476.3664511 — arXiv:2407.05064 (açık erişim, CC BY 4.0) — https://arxiv.org/abs/2407.05064 |
| Anahtar Kelimeler | reverse engineering, MiniFS, binary analiz, veri çıkarma (data extraction), dosya sistemi, firmware güvenlik testi |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** TP-Link AC1900 WiFi router'ının gömülü firmware'i (spesifik CPU mimarisi makalede öne çıkarılmamış, router SoC'si)
- **Analiz Türü:** Statik — manuel/yarı-otomatik ters mühendislik; hex editör ile binary yapı incelemesi
- **Tespit Edilen Tehdit Türü:** Doğrudan bir tehdit tespit aracı değil; MiniFS proprietary dosya sistemi formatının ters mühendisliği. Vaka çalışmasında hardcoded private key'ler ve kriptografik koruma eksikliği tespit edilmiş
- **Kullanılan Ana Teknik/Algoritma:** 6 adımlı genel firmware güvenlik test metodolojisi (edinme/çıkarma → analiz → test, entropi analizi dahil); MiniFS'in "chunk tablosu" yapısını (byte offset'i, chunk boyutu, sıkıştırma sonrası boyut alanları) manuel olarak decode etme ve bu bilgiyle dosya sistemini yeniden inşa etme

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** TP-Link AC1900 router firmware imajı — tek bir ticari ürün üzerinde vaka çalışması
- **Veri Seti Erişilebilir mi?** Hayır — ticari router firmware'i, ayrıca veri seti olarak paylaşılmamış
- **Kaynak Kod Açık mı?** Hayır — kendi geliştirdikleri Python decoder'ları paylaşılmamış; sadece MiniFS için eski, sınırlı yeteneklere sahip üçüncü parti bir decompression aracına (VxWorks MiniFS aracı) referans veriliyor

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek firmware imajı üzerinde çalışıyor, iki imaj arasında karşılaştırma yapmıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Kısmen | 6 adımlı genel firmware güvenlik test metodolojisi (entropi analizi dahil) izleniyor, ama asıl katkı tek bir dosya sistemi formatının çözümlenmesi |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok; bulgular niteliksel (hardcoded key tespiti gibi) |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin dosya sistemi/format analizi katmanına referans olabilir; izlenen 6 adımlı firmware güvenlik test metodolojisi (entropi analizi dahil) projenin genel akışına metodolojik olarak yakın. Proprietary dosya sistemlerinde "security-by-obscurity" riskine dikkat çekmesi, projenin motivasyonunu destekleyen bir bulgu.
- **Eksik bıraktığı nokta (Gap):** Kod paylaşılmadığı için tekrarlanabilirlik zayıf; skorlama/delil zinciri gibi adli bilişim unsurları yok; tek vaka çalışması olduğu için genelleştirilebilirlik sınırlı; differential analiz yapılmıyor.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** ACM ARES 2024'te kabul edilmiş, hakemli. arXiv'de açık erişim tam metin mevcut (CC BY 4.0). Gerçek bir ticari üründe (TP-Link AC1900) hardcoded private key bulunması, makalenin pratik güvenlik etkisini gösteriyor.
