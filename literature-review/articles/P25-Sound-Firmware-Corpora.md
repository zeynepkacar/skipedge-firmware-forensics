# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P25 |
| Başlık | Mens Sana In Corpore Sano: Sound Firmware Corpora for Vulnerability Research |
| Yazarlar | René Helmke, Elmar Padilla (Fraunhofer FKIE, Almanya), Nils Aschenbruck (Osnabrück Üniversitesi, Almanya) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | NDSS 2025 (Network and Distributed System Security Symposium) |
| DOI / Link | arXiv:2404.11977 — https://arxiv.org/abs/2404.11977 |
| Anahtar Kelimeler | firmware corpus, veri seti kalitesi, örnekleme yanlılığı (sampling bias), tekrarlanabilirlik, LFwC (Linux Firmware Corpus) |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Çoklu mimari — Linux tabanlı gömülü firmware'lerin geniş bir yelpazesi (yönlendiriciler, IP kameralar, NAS cihazları vb.)
- **Analiz Türü:** Meta-analiz / metodolojik denetim — kendi bir zafiyet tespit aracı sunmak yerine, mevcut firmware veri setlerinin bilimsel sağlamlığını (soundness) sorguluyor: örnekleme yanlılığı, belgeleme eksikliği, tekrarlanabilirlik sorunları
- **Tespit Edilen Tehdit Türü:** Doğrudan bir tehdit tespiti değil — literatürdeki 44 üst düzey firmware güvenlik makalesini inceleyip kullandıkları veri setlerindeki metodolojik eksiklikleri (temsil gücü, güncellik, çeşitlilik) sistematik olarak ortaya koyuyor
- **Kullanılan Ana Teknik/Algoritma:** Sistematik literatür incelemesi (44 makale) + kendi büyük ölçekli LFwC (Linux Firmware Corpus) veri setinin (10.913 firmware imajı) oluşturulması; FACT (Firmware Analysis and Comparison Tool) tabanlı açma/paketleme (unpacking/repacking) araçlarıyla veri setinin belgelendirilmesi ve doğrulanabilirliğinin sağlanması

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** LFwC (Linux Firmware Corpus) — 10.913 firmware imajından oluşan, kapsamlı şekilde belgelenmiş büyük ölçekli veri seti
- **Veri Seti Erişilebilir mi?** Evet — halka açık, GitHub üzerinden erişilebilir
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/fkie-cad/linux-firmware-corpus) — FACT tabanlı açma/paketleme araçlarıyla birlikte, tam belgelenmiş

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Veri seti kalitesi denetimi yapıyor, imaj karşılaştırması değil |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir meta-analiz yöntemi (literatür + veri seti denetimi) |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "veri seti çaprazlama" ve deneysel tasarım fazına doğrudan uygulanabilir — hangi veri setlerinin (örneğin nRF52 SDK örnekleri, FitBit firmware'leri gibi diğer incelenen makalelerdeki setler) örnekleme yanlılığı taşıyabileceğini değerlendirmek için bir kontrol listesi işlevi görüyor. LFwC veri seti, projenin kendi test setini büyük ölçekli ve çeşitli tutmak için doğrudan kullanılabilir bir kaynak.
- **Eksik bıraktığı nokta (Gap):** Kendi bir zafiyet tespit/skorlama aracı sunmuyor; adli bilişim unsurları (delil zinciri, raporlama) kapsamı dışında; bulguları büyük ölçüde nitel (metodolojik eleştiri), nicel bir karşılaştırma çerçevesi sunmuyor.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** NDSS 2025'te kabul edilmiş, üst düzey hakemli bir konferans. Kod ve veri seti tam açık ve aktif bakımı yapılıyor. Projenin 8/8 kod teyidi hedefine katkı sağlayan güçlü bir referans.
