# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P30 |
| Başlık | A Blockchain-Based Chain of Custody for Digital Evidence: Design and Evaluation |
| Yazarlar | Truong Xuan Hung, Luong The Dung, Tran Anh Tu (Academy of Cryptography Techniques, Vietnam Government Information Security Commission, Vietnam) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | Journal of Science and Technology on Information Security, Sayı 3.CS(26) |
| DOI / Link | 10.54654/isj.v3i26.1167 |
| Anahtar Kelimeler | digital evidence, chain of custody, blockchain, permissioned ledger, smart contracts, auditability, forensic readiness |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Firmware'e özgü değil — genel dijital delil (device image, log, URL, araç çıktısı, adli rapor) yönetimi için tasarlanmış bir blockchain sistemi
- **Analiz Türü:** Sistem tasarımı + prototip implementasyon + ampirik performans değerlendirmesi (firmware analizi değil, delil yönetim altyapısı)
- **Tespit Edilen Tehdit Türü:** Doğrudan bir zafiyet tespiti değil — delil bütünlüğünü tehdit eden senaryolara (içeriden tehdit, kurumlar arası gizli anlaşma/collusion, anahtar ele geçirme, off-chain veri kurcalama) karşı bir delil zinciri (chain of custody) sistemi
- **Kullanılan Ana Teknik/Algoritma:** Hyperledger Fabric tabanlı izinli (permissioned) blockchain — on-chain'de sadece imzalı, zaman damgalı metadata ve içerik özet (digest) değerleri; off-chain'de WORM (Write-Once-Read-Many) uyumlu güvenli delil kilitleri (evidence lockers); delil yaşam döngüsü bir durum makinesi olarak modellenmiş: **Acquire → Seal → Transfer → (Unseal → Analyze → Reseal)* → Disclose → Return/Dispose**; her olay bir önceki olaya (PrevEvtId) hash ile bağlanarak değiştirilemez bir zincir oluşturuyor; hassas geçişler için çok taraflı onay (M-of-N multi-role endorsement) zorunlu kılınıyor; periyodik bütünlük denetimleriyle (fixity check) off-chain artefaktların SHA-256 özetleri ledger'daki kayıtla karşılaştırılıyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Kendi prototip test ortamı — 3 kurumlu konsorsiyum (polis birimi, adli bilişim laboratuvarı, savcılık ofisi), commodity donanımda (4 vCPU, 8GB RAM) sentetik iş yükleri (vaka başına 30-60 olay, 5-10 kurum arası, 1000'e kadar eşzamanlı vaka)
- **Veri Seti Erişilebilir mi?** Hayır — kendi sentetik test senaryoları, halka açık bir veri seti değil
- **Kaynak Kod Açık mı?** Hayır — GitHub veya başka bir kod deposu linki makalede bulunamadı

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Delil yönetim sistemi, imaj/dosya karşılaştırması yapmıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Kısmen | Kimlik (Identity), Veri (Data) ve Kontrol (Control) düzlemleri olmak üzere formal 3 katmanlı bir güvenlik modeli sunuyor, ama tek bir blockchain mimarisi altında |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Evet | Makalenin ana konusu — hash-linked olay zinciri, çok taraflı onay, TPM/HSM tabanlı anahtar yönetimi, periyodik fixity denetimi ile uçtan uca formal bir delil zinciri modeli sunuyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok, delil durumu (acquired/sealed/transferred/disclosed vb.) durum makinesi ile izleniyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Kısmen | İçeriden tehdit (insider threat) ve kurumlar arası gizli anlaşma (collusion) senaryoları tehdit modelinde açıkça ele alınıyor, ama yazılım tedarik zinciri değil, kurumsal/insan kaynaklı tehdit odaklı |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "delil zinciri" katmanına doğrudan uygulanabilir, formal ve test edilmiş bir mimari sunuyor — hash-linked olay zinciri (PrevEvtId), çok taraflı onay (multi-party endorsement) ve periyodik fixity denetimi tasarımları, projenin kendi delil bütünlüğü mekanizmasını tasarlarken doğrudan referans alınabilir. Durum makinesi (Acquire→Seal→Transfer→Analyze→Disclose) modeli de, projenin firmware analiz sürecini adli olarak izlenebilir adımlara bölmek için bir şablon olabilir.
- **Eksik bıraktığı nokta (Gap):** Firmware'e özgü değil — genel dijital delil yönetimi; statik/dinamik firmware analizi (bütünlük, entropi, CVE tarama) içermiyor; kod paylaşılmadığı için performans sonuçları (p50/p95 gecikme, TPS) bağımsız olarak doğrulanamıyor.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** Vietnam Kriptografi Teknikleri Akademisi'nin hakemli dergisinde yayınlanmış, İngilizce/Vietnamca çift dilli özet içeriyor. Hyperledger Fabric 2.5 üzerinde prototip test edilmiş; medyan gecikme <1 saniye, 160-220 TPS gibi somut performans rakamları raporlanmış.
