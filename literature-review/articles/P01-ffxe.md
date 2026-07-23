# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P01 |
| Başlık | FFXE: Dynamic Control Flow Graph Recovery for Embedded Firmware Binaries |
| Yazarlar | Ryan Tsang, Asmita, Doreen Joseph (UC Davis), Soheil Salehi (University of Arizona), Prasant Mohapatra, Houman Homayoun (UC Davis) |
| Yıl | 2024 |
| Yayın Yeri (Venue) | USENIX (33rd USENIX Security Symposium) |
| DOI / Link | 10.5555/3698900.3699212 — https://www.usenix.org/conference/usenixsecurity24/presentation/tsang |
| Anahtar Kelimeler | Control Flow Graph, dynamic forced execution, embedded firmware, volatile memory, Unicorn emulation |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** ARM Cortex-M (birincil hedef), kısmi destek ARM7TDMI ve Cortex-A/R
- **Analiz Türü:** Dinamik — "forced execution" tabanlı emülasyon (Unicorn CPU emulator + Capstone disassembly framework)
- **Tespit Edilen Tehdit Türü:** Doğrudan bir tehdit tespit aracı değil; bir **CFG (Control Flow Graph) recovery** aracı. Vaka çalışmasında (We-Be Band akıllı bileklik firmware'i) bir **buffer overflow** açığı bulunmuş — sınır kontrolü olmayan bir bellek kopyalama zafiyeti
- **Kullanılan Ana Teknik/Algoritma:** Volatile-aware dynamic forced execution — ISR (interrupt service routine) giriş noktalarından ayrı geçişler yaparak asenkron bellek yazma/okuma olaylarını izliyor, callback fonksiyonlarına giden indirect branch'leri (dolaylı dallanmaları) bu şekilde çözüyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** 36 firmware imajı — nRF52 SDK peripheral örnekleri (8 örnek × 4 optimizasyon seviyesi = 32 + blinky), artı 10 gerçek dünya firmware'i (FitBit Flex 1, FitBit Charge HR, Switchmate Bright/Light, Asus USB dongle)
- **Veri Seti Erişilebilir mi?** Kısmen — nRF52 SDK örnekleri halka açık kaynaklardan derlenebilir; gerçek dünya firmware'leri (FitBit vb.) ticari ürünlerden elde edilmiş, veri seti olarak ayrıca paylaşılmamış
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/rchtsang/ffxe) — Dil: Python

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek bir firmware imajını analiz ediyor, iki imaj arasında karşılaştırma yapmıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Kısmen | Vaka çalışmasında Ghidra'nın backward slicing özelliğiyle birlikte kullanılmış, ama kendi başına tek bir yöntem (CFG recovery) |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması yok, çıktısı bir CFG (grafik) |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin doğrudan bir katmanı değil (statik analiz odaklı projemin aksine tamamen dinamik), ancak firmware'in kontrol akışını anlamanın metodolojik bir örneği olarak referans olabilir. Vaka çalışmasındaki "backward slicing ile veri akışı izleme" yaklaşımı, projenin değerlendirme katmanında zafiyet doğrulaması için ilham verici olabilir.
- **Eksik bıraktığı nokta (Gap):** Statik bütünlük (hash), entropi, YARA imza tarama, izin/yetki analizi gibi katmanları içermiyor; adli bilişim unsurları (delil zinciri, raporlama, skorlama) tamamen yok; tek imaj üzerinde çalışıyor, differential analiz yapmıyor. Projemin bu makaleye göre farkı: çok katmanlı statik analiz + adli bilişim odaklı bir sistem sunması.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** USENIX Security 2024'te kabul edilmiş, hakemli. Kod açık kaynak, aktif bakımı yapılıyor (83 commit, MIT lisans). Vaka çalışmasında gerçek bir ticari ürün (We-Be Band) üzerinde gerçek bir zafiyet keşfedilmiş, bu makalenin pratik etkisini gösteriyor.
