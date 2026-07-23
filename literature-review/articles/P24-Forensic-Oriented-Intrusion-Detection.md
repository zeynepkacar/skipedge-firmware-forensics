# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P24 |
| Başlık | Forensic-Oriented Intrusion Detection Using Synthetic Network Traffic Data and Explainable Artificial Intelligence |
| Yazarlar | José Luis Vela, Carmen Pellicer (CESTE University Center, Zaragoza, İspanya) |
| Yıl | 2026 (hakemsiz preprint) |
| Yayın Yeri (Venue) | arXiv preprint |
| DOI / Link | arXiv:2607.00763 — https://arxiv.org/abs/2607.00763 |
| Anahtar Kelimeler | adli bilişim odaklı sızma tespiti, sentetik veri (SDV/CTGAN), açıklanabilir yapay zeka (XAI), SHAP, delil bütünlüğü |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Firmware/gömülü sistem değil — genel ağ trafiği (network traffic) verisi üzerinde çalışan bir sızma tespit sistemi
- **Analiz Türü:** Statik/çevrimdışı makine öğrenmesi analizi — ağ trafiği kayıtları üzerinde XGBoost tabanlı sınıflandırma + SHAP ile açıklanabilirlik
- **Tespit Edilen Tehdit Türü:** Ağ tabanlı sızma/saldırı tespiti (intrusion detection); doğrudan firmware zafiyeti değil, ancak adli bilişim standartlarının bir ML pipeline'ına nasıl entegre edileceği metodolojik olarak projeyle örtüşüyor
- **Kullanılan Ana Teknik/Algoritma:** ISO/IEC 27037, 27041, 27042 ve NIST SP 800-86 adli bilişim standartlarının makine öğrenmesi işlem hattına (pipeline) uygulanması; orijinal delil verisinin hash ile doğrulanmış, değiştirilemez (immutable) bir artefakt olarak korunması; eğitim verisi olarak gerçek veriler yerine sentetik veri üretim araçları (SDV ve CTGAN — Conditional Tabular GAN) kullanılması; XGBoost sınıflandırıcı + SHAP (SHapley Additive exPlanations) ile her tahmin için açıklanabilir, izlenebilir skorlama

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Sentetik olarak üretilmiş ağ trafiği verisi (SDV/CTGAN ile), orijinal delilin hash ile doğrulanmış kopyasından türetilmiş
- **Veri Seti Erişilebilir mi?** Belirtilmemiş net bir paylaşım linki bulunamadı
- **Kaynak Kod Açık mı?** Hayır — GitHub veya başka bir kod deposu linki bulunamadı

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Firmware imajı değil, ağ trafiği akışı üzerinde sınıflandırma yapıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir ML pipeline'ı (XGBoost + SHAP), ama adli bilişim standartlarının (3 ISO standardı + NIST) ML sürecine entegrasyonu metodolojik olarak çok katmanlı |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Evet | Makalenin güçlü yönü — orijinal delilin hash ile doğrulanması, değiştirilemez artefakt olarak saklanması, ISO/IEC 27037/27041/27042 standartlarına uyum açıkça tasarlanmış |
| Tek Bir Şüphe Skoru ile Özetleme | Evet | XGBoost+SHAP ile her örnek için açıklanabilir bir sınıflandırma skoru üretiyor (F1-macro = 0.96) |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Firmware alanında olmasa da, adli bilişim standartlarını (ISO/IEC 27037/27041/27042, NIST SP 800-86) bir ML tabanlı tespit/skorlama sistemine nasıl entegre edeceğine dair güçlü bir metodolojik şablon sunuyor; delil hash doğrulaması + açıklanabilir skorlama (SHAP) kombinasyonu, projenin "delil zinciri + skorlama" katmanlarının birlikte nasıl tasarlanabileceğine dair doğrudan bir örnek teşkil ediyor. Sentetik veri kullanımı da, gerçek/hassas veri paylaşımı olmadan model eğitimi için ilham verici bir yaklaşım.
- **Eksik bıraktığı nokta (Gap):** Firmware'e özgü değil (ağ trafiği odaklı); kod paylaşılmadığı için tekrarlanabilirlik zayıf; statik dosya bütünlüğü, entropi, YARA gibi firmware-spesifik teknikleri içermiyor.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** Hakemsiz preprint (Temmuz 2026). Yüksek F1-macro skoru (0.96) rapor ediliyor, ancak sentetik veri üzerinde eğitildiği için gerçek dünya genellenebilirliği ayrıca doğrulanmalı.
