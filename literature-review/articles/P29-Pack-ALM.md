# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P29 |
| Başlık | Adversarially Robust Assembly Language Model for Packed Executables Detection (Pack-ALM) |
| Yazarlar | Shijia Li, Ni Zhang (China Electronics Corporation + Nankai Üniversitesi), Jiang Ming (Tulane Üniversitesi, ABD), Lanqing Liu, Longwei Yang, Chunfu Jia (Nankai Üniversitesi, Çin) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | ACM CCS 2025 (32nd ACM Conference on Computer and Communications Security, Taipei) — CCF-A/Top4 sınıflandırmalı |
| DOI / Link | 10.1145/3719027.3765157 — arXiv:2509.15499 |
| Anahtar Kelimeler | packed executable tespiti, entropi analizi, dil modeli (language model), adversarial robustness, assembly kodu |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Genel amaçlı çalıştırılabilir dosyalar (PE/ELF binary'ler) — spesifik bir gömülü mimariye bağlı değil, x86/x64 assembly kod seviyesinde çalışıyor
- **Analiz Türü:** Statik — assembly/talimat seviyesinde dil modeli (language model) tabanlı sınıflandırma
- **Tespit Edilen Tehdit Türü:** Paketlenmiş/şifrelenmiş (packed/encrypted) çalıştırılabilir dosyaların tespiti — malware'in paketleme yoluyla statik analizden kaçmasını (evasion) önlemeyi hedefliyor
- **Kullanılan Ana Teknik/Algoritma:** Önce mevcut entropi eşiği tabanlı (genellikle 7.0 civarı) paketleme tespit yöntemlerinin temel zayıflıklarını deneysel olarak kanıtlıyor — malware örneklerinin %30'undan fazlasının entropiyi bu eşiğin altına düşürerek tespitten kaçabildiğini gösteriyor; ardından buna alternatif olarak **Pack-ALM** adında, assembly talimat dizilerini bir dil modeli gibi işleyen, adversarial saldırılara karşı dirençli bir sınıflandırma modeli öneriyor

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Paketlenmiş ve paketlenmemiş çalıştırılabilir dosyalardan oluşan büyük ölçekli bir kıyaslama seti (adversarial örnekler dahil)
- **Veri Seti Erişilebilir mi?** Evet — kod ile birlikte Zenodo üzerinden paylaşılmış
- **Kaynak Kod Açık mı?** Evet — Zenodo'da açık bilim deposu olarak yayınlanmış (GitHub değil, kalıcı bir DOI'li açık bilim arşivi)

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek dosya sınıflandırması, imaj karşılaştırması değil |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir yöntem: dil modeli tabanlı assembly sınıflandırma (entropi tabanlı eski yöntemle karşılaştırmalı olarak) |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Evet | Model, her binary için paketlenmiş/paketlenmemiş olasılığı şeklinde bir sınıflandırma skoru üretiyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Projenin entropi analizi katmanına doğrudan **eleştirel bir literatür desteği** sağlıyor — sabit entropi eşiği (7.0) kullanan yaklaşımların malware'in %30'undan fazlası tarafından atlatılabildiğini kanıtlaması, projenin kendi entropi tabanlı katmanının sınırlamalarını raporlarken referans gösterilebilecek güçlü bir bulgu. Önerilen dil modeli tabanlı alternatif de, projenin gelecekte entropi analizini nasıl güçlendirebileceğine dair bir yön gösteriyor.
- **Eksik bıraktığı nokta (Gap):** Gömülü/IoT firmware'e özgü değil, genel PE/ELF binary'ler için tasarlanmış; adli bilişim unsurları (delil zinciri, raporlama) yok; dil modeli yaklaşımı hesaplama açısından entropi hesabından daha maliyetli olabilir (makalede performans/maliyet karşılaştırması ayrıca değerlendirilmeli).
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** ACM CCS 2025'te kabul edilmiş, CCF-A/Top4 sınıflandırmalı üst düzey bir konferans. Kod ve veri seti Zenodo'da açık ve kalıcı DOI ile erişilebilir — projenin 8/8 kod teyidi hedefine katkı sağlıyor.
