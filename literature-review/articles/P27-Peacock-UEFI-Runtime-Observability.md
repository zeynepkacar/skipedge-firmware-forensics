# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P27 |
| Başlık | Peacock: UEFI Firmware Runtime Observability Layer for Detection and Response |
| Yazarlar | Hadar Cochavi Gorelik, Orel Fadlon, Denis Klimov, Oleg Brodt, Asaf Shabtai, Yuval Elovici (Ben Gurion University of the Negev, İsrail) |
| Yıl | 2026 (hakemsiz preprint) |
| Yayın Yeri (Venue) | arXiv preprint |
| DOI / Link | arXiv:2601.07402 — https://arxiv.org/abs/2601.07402 |
| Anahtar Kelimeler | UEFI, runtime observability, bootkit tespiti, TPM, PCR extension, SIEM entegrasyonu |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** x86/x64 PC-sınıfı sistemler (UEFI firmware) — [[P17-UEFI-Memory-Forensics|P17]] ile aynı Ben Gurion Üniversitesi ekibinden tamamlayıcı bir çalışma
- **Analiz Türü:** Dinamik, gerçek zamanlı (real-time) — P17'nin post-mortem (olay sonrası bellek dump analizi) yaklaşımının aksine, UEFI çalışma zamanında sürekli izleme (continuous runtime observability) sağlıyor
- **Tespit Edilen Tehdit Türü:** UEFI bootkit'leri — gerçek zamanlı olarak function pointer hooking, inline hooking ve kötü amaçlı image yükleme girişimlerini tespit ediyor
- **Kullanılan Ana Teknik/Algoritma:** Sürekli çalışan bir UEFI runtime gözlemleme katmanı; TPM (Trusted Platform Module) tabanlı PCR (Platform Configuration Register) extension mekanizmasıyla log kayıtlarının kriptografik bütünlüğünü sağlama; tespit edilen olayların SIEM (Security Information and Event Management — Splunk entegrasyonu) sistemine gerçek zamanlı aktarımı, böylece kurumsal güvenlik operasyon merkezlerinin (SOC) UEFI seviyesi tehditleri görebilmesi

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** 4 gerçek bootkit ailesi (Glupteba, BlackLotus, LoJax, MosaicRegressor) kullanılarak test edilmiş — P17'dekine benzer bir test metodolojisi
- **Veri Seti Erişilebilir mi?** Hayır — kendi test senaryoları, halka açık bir veri seti değil
- **Kaynak Kod Açık mı?** Bulunamadı — GitHub veya başka bir kod deposu linki tespit edilemedi

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | İki imaj karşılaştırması değil, gerçek zamanlı anomali/hook tespiti |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Kısmen | Gözlemleme katmanı + TPM tabanlı bütünlük doğrulama + SIEM entegrasyonu olmak üzere birbirini tamamlayan bileşenler var |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Evet | TPM PCR extension mekanizması, log kayıtlarının değiştirilemezliğini kriptografik olarak garanti ediyor — bu, delil zincirine doğrudan uygulanabilir güçlü bir teknik |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok, olay bazlı tespit/alarm üretiyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor, ama bootkit kalıcılığı tedarik zinciri/implant temasına dolaylı yakın |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** TPM tabanlı PCR extension ile log bütünlüğü sağlama tekniği, projenin delil zinciri katmanı için doğrudan uygulanabilir kriptografik bir mekanizma sunuyor — statik dosya hash'i yerine, çalışma zamanı olaylarının değiştirilemez şekilde kaydedilmesi fikri projeye entegre edilebilir. Gerçek zamanlı SIEM entegrasyonu da, projenin çıktısının kurumsal güvenlik operasyonlarına nasıl bağlanabileceğine dair bir örnek teşkil ediyor.
- **Eksik bıraktığı nokta (Gap):** UEFI'ye (PC-sınıfı firmware) özgü, gömülü MCU firmware'ine doğrudan uygulanamaz; statik dosya/firmware imaj bütünlüğü (hash, entropi) katmanları içermiyor; kod paylaşılmadığı için tekrarlanabilirlik zayıf.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** Hakemsiz preprint (Ocak 2026). P17 ile aynı ekip ve tema (UEFI güvenliği) üzerine çalışıyor; post-mortem (P17) ve gerçek-zamanlı (bu makale) yaklaşımların birlikte değerlendirilmesi projenin "hem statik hem dinamik" katmanlı yaklaşımına ilham verebilir.
