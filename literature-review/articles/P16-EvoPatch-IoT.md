# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P16 |
| Başlık | EvoPatch-IoT: Evolution-Aware Cross-Architecture Vulnerability Retrieval and Patch-State Profiling for BusyBox-Based IoT Firmware |
| Yazarlar | Yinhao Xiao, Huixi Li, Yongluo Shen (kurum bilgisi makalede/özet kaynaklarında net belirtilmemiş) |
| Yıl | 2026 (hakemsiz preprint) |
| Yayın Yeri (Venue) | arXiv preprint |
| DOI / Link | arXiv:2604.19496 — https://arxiv.org/abs/2604.19496 |
| Anahtar Kelimeler | BusyBox, stripped binary analysis, cross-architecture retrieval, patch-state profiling, IoT firmware security, CVE |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Çoklu mimari (cross-architecture) — aynı BusyBox kaynak bileşeninin farklı heterojen mimarilere derlenmiş halleri karşılaştırılıyor
- **Analiz Türü:** Statik — stripped (sembolsüz) binary'ler üzerinde fonksiyon seviyesinde ikili benzerlik/retrieval analizi
- **Tespit Edilen Tehdit Türü:** Doğrudan bir istismar tespiti değil; firmware'deki BusyBox binary'lerinin hangi sürüme ait olduğunu ve bilinen bir CVE'ye karşı yamalı/yamasız (patch-state) olduğunu belirleme
- **Kullanılan Ana Teknik/Algoritma:** Anonim instruction/context özellikleri, graf seviyesinde istatistikler, ikili-bazlı geometrik öncüller (priors) ve tarihsel fonksiyon prototiplerini birleştiren "evolution-aware" (evrim-farkında) çapraz mimari retrieval çerçevesi; sembol, kaynak yolu veya sürüm string'ine ihtiyaç duymadan homolog/potansiyel zafiyetli fonksiyonları lokalize ediyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Kendi oluşturdukları büyük ölçekli BusyBox benchmark'ı — 57 tarihsel sürüm, 270 unstripped + 285 stripped binary, 130 kaynak kod sürümü; 1.550.752 fonksiyon-sembol satırı, 1.290.369 analiz-fonksiyonu satırı, 155.845 yüksek güvenilirlikli stripped-unstripped eşleşmesi
- **Veri Seti Erişilebilir mi?** Belirtilmemiş — preprint'te ayrı bir veri seti paylaşım/indirme linki bulunamadı
- **Kaynak Kod Açık mı?** Hayır — GitHub veya başka bir kod deposu linki bulunamadı

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Kısmen | Stripped ile unstripped binary'ler ve farklı sürüm/mimari çiftleri arasında homolog fonksiyon eşleştirmesi yapıyor — imaj değil fonksiyon seviyesinde bir diferansiyel yaklaşım |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir yöntem: çapraz mimari fonksiyon retrieval |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Kısmen | Hit@1 / Hit@10 gibi retrieval metrikleri var, ama birleşik bir "şüphe skoru" tasarımı sunulmuyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor, ancak BusyBox'ın firmware'lerde yeniden kullanılan bir bileşen olması nedeniyle tedarik zinciri temasına dolaylı olarak yakın |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "bilinen zafiyetli bileşen tespiti / CVE eşleştirme" katmanına doğrudan uygulanabilir bir yaklaşım sunuyor — stripped firmware binary'lerinde BusyBox sürüm ve yama durumu tespiti, adli bilişim projesinin CVE değerlendirme ihtiyacıyla doğrudan örtüşüyor.
- **Eksik bıraktığı nokta (Gap):** Adli bilişim unsurları (delil zinciri, raporlama, skorlama) yok; sadece BusyBox'a özgü, genel dosya bütünlüğü/entropi/imza tarama gibi katmanlar içermiyor; kod ve veri seti paylaşılmadığı için tekrarlanabilirlik şu an için zayıf.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** Hakemsiz preprint (Nisan 2026). Büyük ölçekli özgün bir benchmark oluşturmuşlar ancak henüz yayınlamamışlar. En güçlü baseline'a göre Hit@1'de %16.04, Hit@10'da %26.85 iyileştirme bildiriyorlar; CVE-2021-42386 patch-state tespitinde mimariler arası ortalama %82.44 doğruluk / %88.47 F1 elde etmişler.
