# Arama Stratejisi Şablonu — 30 Makalelik Literatür Taraması

## 1. Kullanılacak Veritabanları

| Veritabanı | Neden Öncelikli | Tarandı mı? |
|---|---|---|
| IEEE Xplore | Donanım/gömülü sistem güvenliği için güçlü | ☑ (P20 FirmRCA — IEEE S&P) |
| ACM Digital Library | Sistem güvenliği, yazılım mühendisliği | ☑ (P09 PEMU, P19 MiniFS, P28 UniBOM, P29 Pack-ALM — CCS/ARES/IoT konferansları) |
| USENIX Security | Uygulamalı güvenlik araştırmaları | ☑ (P01 FFXE, P04 ChkUp) |
| DFRWS | Adli bilişim odaklı, projeye yakın | ☑ (P05 MARS, P26 SoK Timeline) |
| arXiv | Güncel / ön baskı çalışmalar | ☑ (P03, P06-P08, P10-P11, P14-P18, P20, P23-P27 — çoğunluk) |
| Google Scholar | Genel tarama ve atıf takibi | ☑ (tüm makalelerin DOI/atıf teyidi için kullanıldı) |

## 2. Anahtar Kelime Kombinasyonları

- "firmware integrity verification" + "digital forensics"
- "firmware diffing" + "backdoor detection"
- "supply chain attack" + "embedded firmware"
- "chain of custody" + "IoT forensics"
- "multi-layer firmware analysis"
- "trust score" OR "suspicion score" + "firmware"

**Kullanılan ek sorgular (taramada gerçekten kullanılanlar):**
- "firmware rehosting" + "LLM" (→ P23 FirmCure)
- "UEFI bootkit detection" / "UEFI memory forensics" (→ P17, P27)
- "SBOM" + "IoT firmware" + "CVE scanning" (→ P28 UniBOM)
- "packed executable detection" + "entropy evasion" (→ P29 Pack-ALM)
- "blockchain" + "chain of custody" + "digital evidence" (→ P30)
- "firmware corpus" + "reproducibility" / "sampling bias" (→ P25)
- "control flow graph recovery" + "embedded firmware" (→ P01 FFXE)
- "lightweight hash" + "secure boot" + "IoT" (→ P12, P13)
- "firmware extraction" + "JTAG" OR "UART" + "forensics" (→ P22)
- "vulnerability patch ranking" + "graph" (→ P18 VulRG)
- "ELF header" + "malware detection" + "machine learning" (→ P15)
- "BusyBox" + "stripped binary" + "vulnerability retrieval" (→ P16)

## 3. Filtreleme Kriterleri

- **Zaman aralığı:** Son 1–3 yıl öncelikli (çoğunluk 2024–2026); temel/klasik çalışmalar gerektiğinde dahil edildi (ör. metodoloji referansı olarak kullanılan bazı standart tanım makaleleri).
- **Dil:** İngilizce; Türkçe kaynak kullanılmadı, tüm 30 makale İngilizce.
- **Yayın kalitesi:** Hakemli konferans/dergi öncelikli (USENIX Security, IEEE S&P, ACM CCS, NDSS, DFRWS, ICSE, IFIP SEC, MDPI Sensors, Elsevier FSI dergileri — toplam ~18 makale hakemli); hakemsiz arXiv preprint'ler destekleyici/güncel kaynak olarak dahil edildi (~12 makale), her biri notlarda "hakemsiz preprint" olarak açıkça işaretlendi.

## 4. Kartopu (Snowballing) Yöntemi

- ☑ Uygunluk skoru 4–5 olan makalelerin referans listeleri tarandı (ör. P17'nin referans listesinden aynı ekibin P27/Peacock çalışmasına ulaşıldı; P21'in derleme yapısı P01–P20 arası makalelerin literatür içindeki konumunu netleştirmek için kullanıldı).
- ☑ Bu makalelere atıf yapan yeni çalışmalar Google Scholar/arama motoru üzerinden kontrol edildi (ör. P15/ELF header makalesinin sonraki adversarial malware üretimi çalışmalarında referans gösterildiği teyit edildi).

## 5. Tarama İlerleme Takibi

| Tarih | Kullanılan Sorgu | Veritabanı | Bulunan Sonuç | İncelemeye Alınan |
|---|---|---|---|---|
| Oturum 1 (P01–P06) | "firmware forensics" + "control flow graph" / "firmware update verification" | USENIX Security, arXiv, Google Scholar | ~15-20 | 6 |
| Oturum 1 (P07–P14) | "binary diff LLM" / "supply chain attack firmware" / "lightweight hash secure boot" | arXiv, ACM DL, Google Scholar | ~20-25 | 8 |
| Oturum 2 (P15–P17) | "ELF header malware ML" / "BusyBox vulnerability retrieval" / "UEFI memory forensics" | arXiv, IOP, Google Scholar | ~15 | 3 |
| Oturum 2 (P18–P20) | "vulnerability patch ranking graph" / "MiniFS reverse engineering" / "post-fuzzing root cause" | arXiv, ACM DL, IEEE Xplore | ~12 | 3 |
| Oturum 3 (P21–P24) | "IoT firmware vulnerability review" / "hardware firmware extraction forensics" / "LLM firmware rehosting" / "forensic intrusion detection XAI" | MDPI, Elsevier, arXiv | ~18 | 4 |
| Oturum 3 (P25–P27) | "firmware corpus reproducibility" / "timeline event reconstruction SoK" / "UEFI runtime observability" | NDSS, DFRWS, arXiv | ~12 | 3 |
| 24 Temmuz 2026 (P28–P30) | "SBOM IoT firmware CVE" / "packed executable entropy evasion" / "blockchain chain of custody" | ACM DL, Google Scholar | ~10 | 3 |
| Devam eden | Yeni sorgu: _______________________________________________ | — | — | — |

## 6. Durdurma Kriteri

- ☑ Art arda 2–3 farklı sorguda yeni/alakalı makale çıkmaması — özellikle P28–P30 aşamasında (SBOM, entropi-kaçınma, blockchain delil zinciri konularında) yeni sorgular aynı küçük makale havuzuna geri dönmeye başladı.
- ☑ Aynı makalelere farklı sorgularla tekrar ulaşılması (doygunluk) — ör. P17 hem "UEFI memory forensics" hem "bootkit detection" sorgularında, P22 hem "firmware extraction JTAG" hem "industrial forensics hardware" sorgularında tekrar çıktı.
- ☑ Her temel kriter için en az 3–5 referans makale bulunması — statik bütünlük/entropi (P12, P13, P14, P15, P29), delil zinciri (P22, P24, P27, P30), skorlama (P11, P12, P18, P24, P29), diferansiyel analiz (P07, kısmen P16/P22) kriterlerinin her biri için yeterli sayıda referans toplandı; **30 makalelik hedefe ulaşılarak tarama tamamlandı.**
