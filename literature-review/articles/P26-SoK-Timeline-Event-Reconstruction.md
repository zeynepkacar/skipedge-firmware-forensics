# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P26 |
| Başlık | SoK: Timeline based event reconstruction for digital forensics: Terminology, methodology, and current challenges |
| Yazarlar | Frank Breitinger (Augsburg Üniversitesi, Almanya), Hudan Studiawan (Institut Teknologi Sepuluh Nopember, Endonezya), Chris Hargreaves (Oxford Üniversitesi, İngiltere) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | DFRWS USA 2025 (25. Digital Forensics Research Conference USA) — Forensic Science International: Digital Investigation, Cilt 53, Makale No: 301932 |
| DOI / Link | 10.1016/j.fsidi.2025.301932 — açık erişim (CC BY-NC-ND) |
| Anahtar Kelimeler | event reconstruction, timeline, digital investigation, terminology, framework, challenges |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Mimari bağımsız — genel dijital adli bilişim (herhangi bir sistem/ortam: bilgisayar, akıllı telefon, IoT, bulut)
- **Analiz Türü:** Teorik/kavramsal — sistematik literatür taraması (SoK — Systematization of Knowledge) yoluyla zaman çizelgesi tabanlı olay rekonstrüksiyonu için birleşik bir terminoloji ve model (**TER-Model**) öneriyor
- **Tespit Edilen Tehdit Türü:** Belirli bir tehdit değil — genel olay rekonstrüksiyon sürecini ele alıyor; hem kasıtsız zorluklar (yanlış sistem saati, günlük eksikliği, ortam anomalileri) hem de kasıtlı müdahale (zaman manipülasyonu, anti-forensics araçları, zaman damgası sahteciliği, log silme) kategorize ediliyor
- **Kullanılan Ana Teknik/Algoritma:** TER-Model — Gerçeklik (Reality) ve Rekonstrüksiyon (Reconstruction) uzayları olmak üzere iki ana bölüme, bunlar da 4 çeyreğe (Q1: İlgi Zaman Aralığı, Q2: Olay-Sonrası Dönem, Q3: Zaman Çizelgesi, Q4: Karar Verme/Hipotez Testi) ayrılan görsel bir model; ~200 makalelik sistematik literatür taraması (Google Scholar üzerinden) ile zorlukların sınıflandırılması; her zaman çizelgesi girdisi (t, S, C) — normalize edilmiş zaman damgası, kaynak, bağlam — 3'lüsü olarak formalize ediliyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Yok — teorik/SoK makalesi, kendi deneysel veri seti içermiyor; ~200 makalelik bir literatür taraması sentezleniyor (Tablo 1'de sistematik olarak haritalanmış)
- **Veri Seti Erişilebilir mi?** Uygulanamaz (N/A)
- **Kaynak Kod Açık mı?** Kısmen — modelin pratik bir gösterimi için küçük bir örnek depo paylaşılmış (Link: https://github.com/chrishargreaves/TER-model-example), ancak bu tam bir araştırma kodu değil, sadece modelin kullanımını gösteren bir örnek

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Zaman çizelgesi rekonstrüksiyon teorisi, imaj karşılaştırması değil |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | TER-Model'in 4 çeyreği (Q1-Q4), olay oluşumu → zaman çizelgesi üretimi → analiz → hipotez testi olmak üzere birbirini besleyen, sistematik katmanlar sunuyor |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Kısmen | Delil kontaminasyonu, saklama süresi (aging), zaman damgası sahteciliği/manipülasyonu gibi delil bütünlüğü zorluklarını derinlemesine tartışıyor, ama kendi bir çözüm/mekanizma sunmuyor — bir zorluk kategorisi olarak ele alıyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması sunmuyor; ancak Casey'nin "C-Scale" (kanıt gücü skalası) gibi mevcut yaklaşımlara atıfta bulunuyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "skorlama ve zaman çizelgesi" katmanına güçlü bir akademik/teorik iskelet sağlıyor — "event" ve "artifact" terimlerinin tutarlı tanımları, zaman damgası normalizasyonu gerekliliği, ve özellikle **tamper detection** (zaman damgası sahteciliği tespiti) üzerine Bölüm 7 ve 9.3'teki tartışma, projenin bütünlük ihlali tespit katmanına doğrudan uygulanabilir. 7 araştırma boşluğu (Research Gap) listesi de projenin gelecekteki genişleme yönlerini şekillendirebilir.
- **Eksik bıraktığı nokta (Gap):** Firmware'e özgü değil — genel dijital adli bilişim (çoğunlukla OS-seviyesi zaman çizelgeleri) odaklı; kendi bir aracı/deneyi yok, tamamen teorik; adli bilişim projesi için doğrudan uygulanabilir bir yazılım/algoritma sunmuyor.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** DFRWS USA 2025'te seçilmiş bildiri (Selected Paper), hakemli, açık erişim (CC BY-NC-ND). Yazarların ChatGPT-4'ü metin düzenleme/kısaltma için kullandıklarını açıkça belirtmeleri de dikkat çekici bir şeffaflık örneği.
