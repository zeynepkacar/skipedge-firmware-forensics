# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P21 |
| Başlık | A Review of IoT Firmware Vulnerabilities and Auditing Techniques |
| Yazarlar | Taimur Bakhshi (National University of Computer & Emerging Sciences, Lahore, Pakistan), Bogdan Ghita (University of Plymouth, İngiltere), Ievgeniia Kuzminykh (King's College London, İngiltere) |
| Yıl | 2024 |
| Yayın Yeri (Venue) | Sensors (MDPI), Cilt 24, Sayı 2, Makale No: 708 |
| DOI / Link | 10.3390/s24020708 — açık erişim (CC BY 4.0) |
| Anahtar Kelimeler | Internet of Things, firmware auditing, reverse engineering, security testing |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Kapsamlı bir derleme (review) makalesi olduğu için tek bir mimariye odaklanmıyor; incelenen araçlar ağırlıklı olarak ARM ve MIPS mimarilerini (kısmen x86 ve diğerlerini) destekliyor, Linux platformları literatürde baskın
- **Analiz Türü:** Sistematik literatür taraması ve taksonomi — kendi statik/dinamik analiz yapmıyor, mevcut statik (SA), dinamik (DA) ve hibrit auditing tekniklerini karşılaştırmalı olarak sınıflandırıyor
- **Tespit Edilen Tehdit Türü:** IoT firmware zafiyetlerini 8 geniş kategoriye ayırıyor: sistem özellikleri (yazılım/bellek bozulması), erişim mekanizmaları (kimlik doğrulama/backdoor), bileşen yeniden kullanımı, ağ arayüzü, imaj yönetimi, kullanıcı farkındalığı, düzenleyici uyumluluk, düşman vektörleri (yan kanal vb.)
- **Kullanılan Ana Teknik/Algoritma:** Reverse engineering süreci (edinme → unpacking → decompiling) ve auditing tekniklerinin (statik: Woodpecker, Firmalice, PIE, ANGR, Genius, Gemini, FirmUp, UFO; dinamik: FIE, Avatar, Firmadyne, P2IM, DICE, HALucinator, Laelaps, µEmu; hibrit: Mechanical Phish, IoTFuzzer, Firm-AFL, FIRMCORN) sistematik karşılaştırması; her aracı hedef zafiyet, ölçeklenebilirlik, bilinmeyen zafiyet tespiti ve platform çok yönlülüğü kriterlerine göre tablolar halinde (Tablo 2-6) haritalıyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Yok — bu bir derleme makalesi, kendi veri seti/deneyi içermiyor; incelenen ~150 kaynağın bulgularını sentezliyor
- **Veri Seti Erişilebilir mi?** Uygulanamaz (N/A)
- **Kaynak Kod Açık mı?** Hayır — derleme makalesi, kod üretmiyor; ancak incelediği araçların çoğunun (Binwalk, ANGR, Ghidra, QEMU, AFL vb.) halka açık kaynak kodlu olduğunu not ediyor

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Derleme makalesi, kendi analiz yöntemi sunmuyor |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Statik, dinamik ve hibrit yöntemleri taksonomik olarak birbirini tamamlayan katmanlar şeklinde ele alıyor, unification (birleştirme) ihtiyacını açıkça vurguluyor |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor, güvenlik denetimi (security auditing) odaklı |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Skorlama mekanizması sunmuyor, araçları çok boyutlu tablolarla karşılaştırıyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Kısmen | "Hardware and Software Re-use" (bileşen yeniden kullanımı) kategorisi ODM/OEM koordinasyon sorunlarını ve zafiyetlerin binlerce cihaza yayılmasını (tedarik zinciri riskine yakın) tartışıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin "related work" (ilgili çalışmalar) bölümü için omurga niteliğinde bir kaynak — 8 kategorili zafiyet taksonomisi ve araç-zafiyet-mimari eşleştirme tabloları (Tablo 6), projenin kapsamını ve konumlandırmasını literatür içinde netleştirmeye yardımcı oluyor. Makine öğrenmesi ve blockchain'in firmware auditing'e entegrasyonu üzerine önerilen gelecek araştırma yönleri de projenin genişleme potansiyeline ışık tutuyor.
- **Eksik bıraktığı nokta (Gap):** Kendi bir aracı/deneyi yok, tamamen ikincil literatüre dayanıyor; adli bilişim unsurları (delil zinciri, raporlama, skorlama) makalenin kapsamı dışında; unification (araçların birleştirilmesi) ihtiyacını vurguluyor ama somut bir çözüm sunmuyor.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** Hakemli (MDPI Sensors), açık erişim. Kapsamlı bir kaynakça (150+ referans) içeriyor; literatür taramasının "related work" bölümü için birincil referans olarak kullanılabilir.
