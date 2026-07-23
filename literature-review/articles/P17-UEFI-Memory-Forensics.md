# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P17 |
| Başlık | UEFI Memory Forensics: A Framework for UEFI Threat Analysis |
| Yazarlar | Kalanit Suzan Segal, Hadar Cochavi Gorelik, Oleg Brodt, Yuval Elbahar, Yuval Elovici, Asaf Shabtai (Ben Gurion University of the Negev, İsrail) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | 11th IEEE European Symposium on Security and Privacy (Euro S&P) — kabul edilmiş; arXiv preprint olarak da mevcut |
| DOI / Link | arXiv:2501.16962 — https://arxiv.org/abs/2501.16962 |
| Anahtar Kelimeler | UEFI, memory forensics, bootkit, function pointer hooking, inline hooking, pre-boot güvenlik, DXE |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** x86/x64 PC-sınıfı sistemler (UEFI firmware) — Coreboot tabanlı Ubuntu laptop ve Lenovo ThinkPad (Windows 11) üzerinde fiziksel test, ayrıca QEMU/TianoCore EDK II ile sanal ortam testi
- **Analiz Türü:** Dinamik + Statik hibrit — önce UEFI önyükleme aşamasında bellek toplama (dinamik), ardından toplanan dump üzerinde disassembly tabanlı anomali tespiti (statik)
- **Tespit Edilen Tehdit Türü:** UEFI bootkit'leri — çalışma zamanı bellek/kontrol yapısı bütünlük ihlalleri: function pointer hooking, inline hooking ve kötü amaçlı image (PE/COFF) yükleme
- **Kullanılan Ana Teknik/Algoritma:** İki bileşenli çerçeve — UefiMemDump (DXE driver + UEFI shell uygulaması olarak bellek toplama) ve UEFIDumpAnalysis (Boot/Runtime/DXE Services tablolarındaki fonksiyon pointer'larının GUID tabanlı beklenen bellek aralığına göre doğrulanması; Capstone disassembler ile fonksiyon prolog'larında jmp/call talimatlarını tarayarak inline hook tespiti; b'ldri' imzalarından PE/COFF image carving)

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Kendi oluşturdukları test ortamı — QEMU sanal ortamda EDK II firmware imajı ve iki fiziksel laptop (System76 Adder WS / Coreboot, Lenovo ThinkPad T14 Gen4); gerçek bootkit tekniklerini (EfiGuard, Glupteba, CosmicStrand, MoonBounce, ThunderStrike) kendi kötü amaçlı DXE driver/OPROM implementasyonlarıyla yeniden üretmişler
- **Veri Seti Erişilebilir mi?** Hayır — halka açık, indirilebilir bir veri seti değil, kendi test senaryoları
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/UefiMemAnalysis/UefiMemAnalysis) — MIT lisans, 17 commit, aktif ve detaylı README/dokümantasyon

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | İki imaj karşılaştırması değil; GUID tabanlı beklenen bellek aralığından sapma tespiti yapıyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Üç ayrı analiz modülü (function pointer hooking, inline hooking, image carving) birlikte, tamamlayıcı şekilde kullanılıyor |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Ham bellek dump'ı alınıyor ama kriptografik doğrulama/zincir mekanizması sunulmuyor |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Her modül kendi anomalisini ayrı ayrı flag'liyor, birleşik bir skor yok |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor; ancak bootkit'lerin firmware'e kalıcı yerleşimi tedarik zinciri/implant temasına dolaylı olarak yakın |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin doğrudan bir katmanı değil (statik dosya/firmware imaj analizi odaklı projenin aksine tamamen çalışma zamanı belleği), ancak GUID tabanlı "beklenen bellek aralığından sapma" mantığı, projenin statik bütünlük kontrolü (beklenen hash/imzadan sapma) fikrine metodolojik bir analoji sunuyor. Çok modüllü, tamamlayıcı analiz yaklaşımı da projenin "çok katmanlı analiz" hedefine örnek teşkil edebilir.
- **Eksik bıraktığı nokta (Gap):** Statik firmware dosyası/imaj bütünlüğü (hash, entropi, YARA) katmanları içermiyor; UEFI'ye (PC-sınıfı firmware) özgü, gömülü MCU firmware'ine doğrudan uygulanamaz; delil zinciri ve birleşik skorlama mekanizmaları yok; tek imaj/oturum üzerinde çalışıyor, differential analiz yapmıyor.
- **Uygunluk Skoru (1–5):** 3
- **Ek Notlar:** IEEE Euro S&P'ye kabul edilmiş, hakemli. Kod açık kaynak, aktif bakımı yapılıyor (MIT lisans). Gerçek bootkit ailelerine (ThunderStrike, CosmicStrand, Glupteba, MoonBounce, EfiGuard) karşı hem sanal hem fiziksel ortamda test edilmiş, bu da makalenin pratik etkisini güçlü şekilde gösteriyor.
