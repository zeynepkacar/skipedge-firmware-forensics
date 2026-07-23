# Özet Karşılaştırma Tablosu — 30 Makale

## 1. Makale Karşılaştırma

| ID | Yıl | Makale Başlığı | Hedef Mimari | Analiz Türü | Veri Seti / Kod | A vs B? | Çok Katmanlı? | Delil Zinciri? | Skorlama? | Temel Eksiklik (Gap) | Uygunluk (1–5) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P01 | 2024 | FFXE: Dynamic Control Flow Graph Recovery for Embedded Firmware Binaries | ARM Cortex-M (+ARM7TDMI, Cortex-A/R kısmi) | Dinamik (forced execution / emülasyon) | Kod açık (GitHub); veri seti kısmen açık | Hayır | Kısmen | Hayır | Hayır | Statik bütünlük/entropi/skorlama yok, tek imaj | 3 |
| P02 | 2025 | ROSA (fuzzing oracle sentezi, BINSEC tabanlı) | Genel/embedded (BINSEC mimarileri) | Dinamik (fuzzing/oracle sentezi) | Kod açık (binsec/rosa + rosarum) | Hayır | Kısmen | Hayır | Kısmen | Adli bilişim unsurları yok | 3 |
| P03 | 2024 | AutoFirm | IoT firmware (çoklu) | Dinamik/otomatik test | Kod açık (sure17/AutoFirm), 6.900+ firmware veri seti | Hayır | Evet | Hayır | Kısmen | Adli bilişim unsurları yok | 3 |
| P04 | 2024 | ChkUp / "Your Firmware Has Arrived" | Genel firmware güncelleme | Statik + dinamik güncelleme kontrolü | Kod açık (WUSTL-CSPL/ChkUp) | Hayır | Kısmen | Hayır | Hayır | Adli bilişim unsurları yok | 3 |
| P05 | 2024 | MARS | Bellek adli bilişimi (mimari belirtilmemiş) | Dinamik | Kod paylaşılmamış | Hayır | Kısmen | Kısmen | Kısmen | Kod yok, tekrarlanabilirlik zayıf | 3 |
| P06 | 2026 | TELEMETRY projesi (IoT ekosistem test) | Çoklu (IoT ekosistemi) | Karma (fuzzing + izleme) | Kod paylaşılmamış (açık araçlara referans) | Hayır | Evet | Hayır | Hayır | Kendi kodu yok, sadece mevcut araçlara referans | 3 |
| P07 | 2025 | Binary Diff Summarization using LLMs | Genel binary (mimari-bağımsız) | Statik (LLM tabanlı diffing) | Kod paylaşılmamış | **Evet** | Hayır | Hayır | Hayır | Firmware'e özgü değil, kod yok | 4 |
| P08 | 2026 | SynthChain | Paket ekosistemi (PyPI/npm/C++) — firmware değil | Statik (tedarik zinciri saldırı zinciri rekonstrüksiyonu) | Kod/veri henüz yayınlanmamış | Hayır | Evet | Kısmen | Hayır | Konu firmware değil, düşük öncelik | 2 |
| P09 | 2025 | PEMU (Protocol-Aware Firmware Rehosting) | Embedded ağ yığınları (network stacks) | Dinamik (protokol-farkında rehosting/fuzzing) | Kod açık (MPI-SysSec/pemu) | Hayır | Evet | Hayır | Hayır | Adli bilişim unsurları yok | 3 |
| P10 | 2026 | Out-of-Band Power Side-Channel Detection | Fiziksel donanım (yarı iletken) | Dinamik (güç tüketimi + GAN) | Kod paylaşılmamış | Hayır | Hayır | Hayır | Kısmen | Statik dosya analizi değil, farklı modalite | 2 |
| P11 | 2025 | Energy-Efficient Multi-LLM Reasoning for Zero-Day Detection | IoT firmware (binary-free) | Simülasyon / LLM muhakeme | Kod paylaşılmamış | Hayır | Evet | Hayır | Evet | Gerçek firmware'de test edilmemiş, simülasyon tabanlı | 3 |
| P12 | 2025 | Lightweight hash functions for secure boot | STM32F072 / ESP8266 / ATmega328P | Statik (hash performans testi) | Kod paylaşılmamış | Hayır | Kısmen | Kısmen | Evet | Adli bilişim unsurları yok | 3 |
| P13 | 2025 | PLWHF (Data-Parallel Lightweight Hash) | Raspberry Pi 4 (SIMON cipher) | Statik (paralel hash) | Kod paylaşılmamış | Hayır | Hayır | Hayır | Hayır | Adli bilişim unsurları yok | 3 |
| P14 | 2026 | Multi-Interface Firmware Acquisition (Holy Stone drone) | Drone (mimari belirtilmemiş) | Statik (3 katmanlı: boyut/hash/entropi + EMBA) | Kod/veri kontrol edilmedi | Hayır | Evet | Kısmen | Hayır | Kod/veri paylaşımı doğrulanmadı | 4 |
| P15 | 2025 | Lightweight ELF header analysis for IoT malware (ML) | ARM | Statik (sadece ELF header, 64-1024 byte) | Kod yok | Hayır | Hayır | Hayır | Kısmen | Sadece header'a bakıyor, dosyanın geri kalanı yok | 2 |
| P16 | 2026 | EvoPatch-IoT (BusyBox) | Çoklu (cross-architecture) | Statik (fonksiyon retrieval) | Kod yok | Kısmen | Hayır | Hayır | Kısmen | BusyBox'a özgü, adli bilişim yok | 4 |
| P17 | 2025 | UEFI Memory Forensics | x86/x64 (UEFI) | Dinamik + statik hibrit | Kod açık (UefiMemAnalysis) | Hayır | Evet | Hayır | Hayır | UEFI'ye özgü, PC-sınıfı, gömülü MCU'ya uygulanamaz | 3 |
| P18 | 2025 | VulRG (graf tabanlı yama önceliklendirme) | Sistem-agnostik | Statik (graf tabanlı) | Kod yok | Hayır | Evet | Hayır | Evet | Firmware'e özgü değil | 3 |
| P19 | 2024 | Reverse Engineered MiniFS File System | TP-Link router (MIPS/ARM) | Statik (manuel RE) | Kod yok | Hayır | Kısmen | Hayır | Hayır | Kod paylaşılmamış, tek vaka çalışması | 3 |
| P20 | 2025 | FirmRCA (post-fuzzing kök neden analizi) | ARM | Dinamik (event-based footprint) | Kod + veri seti açık (GitHub + Zenodo) | Hayır | Hayır | Hayır | Kısmen | Statik bütünlük/entropi yok | 3 |
| P21 | 2024 | A Review of IoT Firmware Vulnerabilities and Auditing Techniques | Mimari-bağımsız (derleme) | Sistematik literatür taraması | Kod yok (derleme) | Hayır | Evet | Hayır | Hayır | Kendi aracı/deneyi yok | 4 |
| P22 | 2026 | Systematic Firmware Extraction Techniques (endüstriyel) | Çoklu (ARM/x86/MIPS/PowerPC) | Donanım-odaklı edinme (acquisition) | Kod yok (kullanılan araçlar açık) | Hayır | Kısmen | **Evet** | Hayır | Yazılım zafiyet tespiti içermiyor | 4 |
| P23 | 2026 | FirmCure (LLM tabanlı rehosting) | Çoklu (5 mimari) | Dinamik (tam sistem rehosting) | Kod anonim depoda, kalıcı link yok | Hayır | Evet | Kısmen | Hayır | Kod henüz kalıcı olarak yayınlanmadı | 3 |
| P24 | 2026 | Forensic-Oriented Intrusion Detection (XAI) | Ağ trafiği (firmware değil) | Statik ML (XGBoost+SHAP) | Kod yok, veri sentetik (SDV/CTGAN) | Hayır | Hayır | **Evet** | **Evet** | Firmware'e özgü değil | 3 |
| P25 | 2025 | Sound Firmware Corpora for Vulnerability Research | Çoklu | Meta-analiz (literatür + veri seti denetimi) | Kod + veri açık (LFwC, 10.913 imaj) | Hayır | Hayır | Hayır | Hayır | Kendi tespit aracı yok | 4 |
| P26 | 2025 | SoK: Timeline based event reconstruction | Mimari-bağımsız | Teorik (TER-Model) | Kısmen (örnek repo) | Hayır | Evet | Kısmen | Hayır | Teorik, firmware'e özgü değil | 4 |
| P27 | 2026 | Peacock (UEFI runtime observability) | x86/x64 (UEFI) | Dinamik, gerçek zamanlı | Kod yok | Hayır | Kısmen | **Evet** | Hayır | UEFI'ye özgü | 3 |
| P28 | 2025 | UniBOM (SBOM analiz aracı) | Router firmware (OpenWrt/TRENDnet) | Statik (SBOM + CVE) | Kod açık (nqminds/UniBOM) | Hayır | Evet | Hayır | Hayır | Sadece bilinen (CVE) zafiyetler | 4 |
| P29 | 2025 | Pack-ALM (Adversarially Robust Assembly LM) | PE/ELF (genel) | Statik (dil modeli) | Kod + veri açık (Zenodo) | Hayır | Hayır | Hayır | **Evet** | Firmware'e özgü değil | 4 |
| P30 | 2025 | A Blockchain-Based Chain of Custody | Firmware'e özgü değil | Sistem tasarımı + prototip | Kod yok | Hayır | Kısmen | **Evet** | Hayır | Firmware analizi içermiyor | 4 |

## 2. Gap Analizi / Problem Tanımı

**Ortak Eksiklik 1 — Diferansiyel Analiz (A vs B imaj karşılaştırması):**
30 makalenin yalnızca 1'i (P07 — Binary Diff Summarization) doğrudan diferansiyel/karşılaştırmalı analiz sunuyor, o da firmware'e özgü değil, genel binary diff'e odaklanıyor. İncelenen literatürün ezici çoğunluğu tek bir firmware imajı/dosyası üzerinde çalışıyor; iki sürüm veya iki cihaz arasında sistematik karşılaştırma yapan bir çalışmaya rastlanmadı.

**Ortak Eksiklik 2 — Delil Zinciri (Chain of Custody) ve Kriptografik Doğrulama:**
Sadece 4 makalede (P22, P24, P27, P30) güçlü şekilde ele alınmış — ancak bunların hiçbiri firmware'e özgü statik bütünlük/entropi analiziyle birleştirilmemiş (sırasıyla donanım edinme, ağ IDS, UEFI runtime izleme ve genel blockchain delil yönetimi bağlamlarında). Firmware analiz araçlarının büyük çoğunluğu, ürettikleri bulguları adli olarak izlenebilir/doğrulanabilir bir formatta raporlamıyor.

**Ortak Eksiklik 3 — Tek Bir Birleşik Şüphe/Güven Skoru:**
Sadece 5 makalede (P11, P12, P18, P24, P29) kısmen veya tam olarak mevcut. Literatürün geneli ham çıktı üretiyor (CFG, SBOM listesi, sınıflandırma etiketi, retrieval skoru) ve nihai yorumu insan analiste bırakıyor; çok boyutlu bulguları (hash uyuşmazlığı + entropi anomalisi + CVE eşleşmesi + imza taraması) tek bir açıklanabilir skorda birleştiren bir yaklaşım bulunamadı.

**Projenin Konumlandığı Boşluk (Positioning Statement):**
Gömülü sistem firmware güvenliği literatürü ağırlıklı olarak tek katmanlı (yalnızca statik *veya* yalnızca dinamik) ve tek-imaj odaklıdır; adli bilişim gerekliliklerini (delil zinciri, standartlara uyumlu raporlama) firmware analiz katmanıyla birleştiren çalışmalar nadirdir (30 makalenin sadece %13'ü). Projemiz, çok katmanlı statik analiz (hash bütünlüğü + entropi + CVE/SBOM taraması + imza tarama) ile A/B diferansiyel karşılaştırmayı bir araya getirip bunları tek bir açıklanabilir şüphe skoruna ve NIST SP 800-86 / ISO 27037 uyumlu delil zinciri raporlamasına bağlayarak, literatürde tespit edilen bu üç boşluğu (diferansiyel analiz + skorlama + delil zinciri kombinasyonu) aynı anda dolduran nadir çalışmalardan biri olarak konumlanıyor.

## 3. İstatistikler

| Gösterge | Sayı | Oran |
|---|---|---|
| Toplam incelenen makale | 30 | — |
| Diferansiyel analiz (A vs B) — Evet | 1 | %3,3 |
| Çok katmanlı analiz — Evet | 12 | %40,0 |
| Delil zinciri — Evet | 4 | %13,3 |
| Skorlama — Evet | 5 | %16,7 |

*Not: "Kısmen" olarak işaretlenen satırlar yukarıdaki "Evet" sayımına dahil edilmemiştir; sadece net "Evet" durumları sayılmıştır.*
