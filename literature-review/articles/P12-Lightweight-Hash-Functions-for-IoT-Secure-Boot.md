# Makale İnceleme Şablonu — P12

## 1. Künye ve Meta Veri

| Alan | Bilgi |
|---|---|
| Makale ID | P12 |
| Başlık | The method for verifying firmware integrity in IoT devices for secure boot using lightweight hash functions |
| Yazarlar | Inna Rozlomii, Emil Faure, Andrii Yarmilko, Serhii Naumenko |
| Yıl | 2025 |
| Venue | CSDP'2025 (Cyber Security and Data Protection), CEUR-WS Vol-4042, 31 Temmuz 2025, Lviv, Ukrayna |
| DOI / Link | CEUR-WS Vol-4042 (açık erişim, CC BY 4.0) — https://ceur-ws.org/Vol-4042/ |
| Anahtar Kelimeler | limited resources, IoT, lightweight hashing, session tokens, weighted aggregation, STM32F072, ESP8266, ATmega328P |

## 2. Teknik Analiz ve Metodoloji

| Alan | Bilgi |
|---|---|
| Hedef Mimari | STM32F072 (32-bit Cortex-M0), ESP8266 (Tensilica L106), ATmega328P (8-bit AVR) — düşük kaynaklı IoT mikrodenetleyicileri |
| Analiz Türü | Statik bütünlük doğrulama (secure boot / firmware hash karşılaştırma); dinamik/runtime analiz değil |
| Tespit Edilen Tehdit Türü | Firmware değişikliği/manipülasyonu (modification), replay saldırıları (önceki geçerli hash değerinin tekrar kullanımı) |
| Ana Teknik / Algoritma | Çok seviyeli ağırlıklı hash agregasyonu (Hagg = Σ wi·Hi); SPONGENT/PHOTON/QUARK/LESAMNTA-LW hafif hash fonksiyonları; session/context token ile replay koruması; cihaz durumuna (batarya, CPU yükü) göre adaptif kısmi doğrulama derinliği |

## 3. Veri Seti ve Tekrarlanabilirlik

| Alan | Bilgi |
|---|---|
| Veri Seti | Kendi oluşturdukları segmentlenmiş firmware imajları (STM32F072: 32 KB, ESP8266: 48 KB, ATmega328P: 28 KB); standart/paylaşılan bir veri seti değil |
| Erişilebilir mi | Hayır — makalede veri seti/imaj paylaşım linki yok |
| Kaynak Kod Açık mı | Hayır — kaynak kod paylaşımı bulunamadı |

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
|---|---|---|
| Diferansiyel Analiz | Kısmen | Tek referans hash ile karşılaştırma; segment bazlı kısmi/ağırlıklı yaklaşım var ama iyi/kötü örnek karşılaştırması yok |
| Çok Katmanlı Analiz | Var | Segment ağırlıklandırma + adaptif (batarya/CPU durumuna göre) kademeli doğrulama derinliği |
| Delil Zinciri | Yok | Uyuşmazlık durumunda loglama/uyarı bahsediliyor ama formal chain-of-custody modeli yok |
| Tek Şüphe Skoru | Kısmen | Ağırlıklı aggregate hash tek bir D(Hagg) kararına indirgeniyor; ancak sürekli/olasılıksal skor değil, ikili (eşleşti/eşleşmedi) karar |
| Tedarik Zinciri / İç Tehdit | Yok | Tedarik zinciri odaklı değil; cihaz-üstü secure boot senaryosuna odaklanıyor |

## 5. Değerlendirme

| Alan | Bilgi |
|---|---|
| Katkı | Kaynak kısıtlı IoT cihazlarında SHA-256'ya kıyasla %30-60 kaynak (süre/RAM/güç) tasarrufu sağlayan ağırlıklı ve kısmi hafif-hash doğrulama yöntemi; üç farklı mimaride (STM32F072, ESP8266, ATmega328P) somut donanım ölçümleri sunuyor |
| Gap | Sadece statik firmware segmentleri kontrol ediliyor, dinamik yüklenen modüller kapsam dışı bırakılmış; kod ve veri seti paylaşılmadığı için tekrarlanabilirlik zayıf; adli bilişim/delil zinciri perspektifi yok, secure boot odaklı |
| Uygunluk Skoru (1-5) | 3 |
| Ek Notlar | SPONGENT/PHOTON/QUARK/LESAMNTA-LW karşılaştırma tabloları (süre, RAM, güç tüketimi) "hangi hafif hash fonksiyonu kullanılmalı" kararı için P13 ile birlikte referans olarak kullanılabilir |
