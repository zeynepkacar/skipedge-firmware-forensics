# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P23 |
| Başlık | FirmCure: Towards Autonomous and Adaptive Rehosting of Linux-Based Firmware |
| Yazarlar | Chuan Hong, Zheng Zhang, Lei Zhou, Laisong Li, Chenyifan Liu, Ze Huang, Xu Zhou, Peihong Lin (National University of Defense Technology, Çin) |
| Yıl | 2026 (hakemsiz preprint) |
| Yayın Yeri (Venue) | arXiv preprint |
| DOI / Link | arXiv:2606.24549 — https://arxiv.org/abs/2606.24549 |
| Anahtar Kelimeler | full-system rehosting, Linux tabanlı firmware, LLM (büyük dil modeli), adaptive/autonomous rehosting, dinamik analiz |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Çoklu mimari — değerlendirmede 5 farklı mimari kullanılmış (ARM, MIPS vb. dahil olası — makalede "5 architectures" olarak belirtiliyor), 10 farklı üreticiden 21 IoT firmware imajı
- **Analiz Türü:** Dinamik — tam sistem (full-system) rehosting/emülasyon; firmware'i gerçek donanımdan bağımsız sanal ortamda çalıştırıp servis etkileşimini test ediyor
- **Tespit Edilen Tehdit Türü:** Doğrudan bir tehdit tespiti değil — rehosting sürecindeki başlatma (initialization) ve çalışma zamanı (runtime) engellerini otomatik gidermeyi hedefleyen bir altyapı; başarılı rehosting sonrası bilinen CVE'ler yeniden üretilmiş ve yeni zafiyetler bulunmuş
- **Kullanılan Ana Teknik/Algoritma:** İlk LLM-güdümlü tam-sistem rehosting çerçevesi — (1) Adaptive Perception Inference: statik analiz ile firmware yapısal bağımlılıklarını çıkarma, (2) Reflective Synthesis: yinelemeli konfigürasyon optimizasyonu, (3) Autonomous Runtime Intervention: çalışma zamanı hata teşhisi ve izleme yoluyla gerçek zamanlı hata giderme (crash, eksik dosya, sonsuz döngü gibi engellere otomatik müdahale)

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** 10 vendörden, 5 mimariden toplanan 21 IoT firmware imajı ile değerlendirilmiş
- **Veri Seti Erişilebilir mi?** Belirtilmemiş net bir paylaşım linki bulunamadı
- **Kaynak Kod Açık mı?** Kısmen — anonim bir depoda ~16.000 satır Python kodu (CrewAI framework tabanlı) paylaşıldığı önceki araştırma notlarında belirtilmiş, ancak kalıcı/isimli bir GitHub linki şu an için mevcut değil (muhtemelen hakem değerlendirmesi sonrası yayınlanacak)

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek firmware imajının rehosting sürecini otomatikleştiriyor, imaj karşılaştırması yapmıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Statik analiz (yapısal bağımlılık çıkarma) + dinamik rehosting + çalışma zamanı hata teşhisi olmak üzere üç aşamalı, tamamlayıcı bir boru hattı |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Kısmen | Her müdahale adımının loglanıp izlenebilir (audit trail) olduğu belirtiliyor, ama formal bir delil zinciri/kriptografik doğrulama mekanizması değil |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok; çıktı, başarılı rehosting ve tespit edilen CVE/zafiyet listesi |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Rehosting, projenin statik bütünlük odaklı yaklaşımının tamamlayıcısı olarak dinamik doğrulama katmanına örnek teşkil edebilir; LLM tabanlı otomatik hata giderme yaklaşımı, projenin "değerlendirme" aşamasında zafiyet doğrulamasını hızlandırma fikri için ilham verici olabilir.
- **Eksik bıraktığı nokta (Gap):** Statik bütünlük (hash), entropi, delil zinciri gibi adli bilişim unsurları yok; kod henüz kalıcı olarak yayınlanmadığı için tekrarlanabilirlik şu an sınırlı; özel donanım bağımlı (custom device) senaryolar için tasarlanmış, genel amaçlı statik analiz aracı değil.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** Hakemsiz preprint (Haziran 2026). 21 firmware imajında %100 ağ portu açma oranı ve %90.5 servis etkileşimi elde etmiş; 10 bilinen CVE yeniden üretilmiş ve 5 yeni zafiyet bulunmuş — pratik etkisi güçlü ama henüz hakem değerlendirmesinden geçmemiş.
