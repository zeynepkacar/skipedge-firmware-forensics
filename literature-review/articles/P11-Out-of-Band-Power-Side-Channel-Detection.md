# Makale İnceleme Şablonu — P11

## 1. Künye ve Meta Veri

| Alan | Bilgi |
|---|---|
| Makale ID | P10 |
| Başlık | Out-of-Band Power Side-Channel Detection for Semiconductor Supply Chain Integrity at Scale |
| Yazarlar | Rajiv Thummala, Katherine Winton, Luke Flores, Elizabeth Redmond, Gregory Falco |
| Yıl | 2026 (preprint, 3 Ocak 2026) |
| Venue | arXiv preprint (SPIE formatında); Cornell University / Brooks Tech Policy Institute, DoD fonlu (Award No. HQ00342520002) |
| DOI / Link | arXiv:2601.01054 — https://arxiv.org/abs/2601.01054 |
| Anahtar Kelimeler | power side-channel, semiconductor supply chain, hardware Trojan, GAN, anomaly detection, ChipWhisperer, firmware tampering |

## 2. Teknik Analiz ve Metodoloji

| Alan | Bilgi |
|---|---|
| Hedef Mimari | Atmel XMEGA128D4 (8/32-bit AVR mikrodenetleyici), ChipWhisperer-Lite (CW1173) + CW308 UFO baseboard üzerinde; COTS drone/UAS avionik yığınındaki tersiyer/çevresel mikrodenetleyicileri (peripheral safety controller) temsilen seçilmiş |
| Analiz Türü | Fiziksel güç yan-kanal (power side-channel) ölçümüne dayalı dinamik/donanımsal anomali tespiti — statik dosya/firmware analizi DEĞİL |
| Tespit Edilen Tehdit Türü | Koşullu tetiklenen donanım Truva atı, gizli backdoor komutu, kriptografik bütünlük ihlali (ciphertext bit-flip), gecikme/exfiltrasyon döngüsü — dört farklı sabotaj sınıfı, composite (birleşik) ve tekil senaryolar halinde test edilmiş |
| Ana Teknik / Algoritma | Sadece iyi huylu (benign) güç izlerinde eğitilen tek sınıflı (one-class) WGAN-GP; discriminator çıktısı anomali skoru olarak kullanılıyor (s(x*) = −D(x*)); %1/%5 hedef yanlış pozitif oranına (FPR) göre eşik kalibrasyonu |

## 3. Veri Seti ve Tekrarlanabilirlik

| Alan | Bilgi |
|---|---|
| Veri Seti | Kendi topladıkları 2.000 benign + 2.000 composite tampered + 4×1.000 tekil-sabotaj güç izi (ChipWhisperer-Lite ile, tek cihaz/tek oturum, 3.000 örnek/iz) |
| Erişilebilir mi | Belirtilmemiş — makalede veri seti için paylaşım linki yok |
| Kaynak Kod Açık mı | Hayır — kaynak kod paylaşımı bulunamadı |

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
|---|---|---|
| Diferansiyel Analiz | Var | Benign vs composite tampered ve 4 tekil-sabotaj senaryosu ayrı ayrı karşılaştırılıyor (Tablo 2/3), AUC/TPR@FPR metrikleriyle raporlanmış |
| Çok Katmanlı Analiz | Kısmen | Tek bir discriminator skoru üretiliyor; ancak üç kademeli tedarik zinciri konuşlandırma noktası (üretim sonu, kabul muayenesi, depo/bakım) öneriliyor |
| Delil Zinciri | Yok | Anomali tespiti sonrası "karantina/forensic eskalasyon" öneriliyor ama formal chain-of-custody modeli yok |
| Tek Şüphe Skoru | Var | s(x*) = −D(x*) tek bir sürekli anomali skoru üretiyor — projenin "tek şüphe skoru" fikrine doğrudan paralel |
| Tedarik Zinciri / İç Tehdit | Var | Makalenin ana odağı doğrudan yarı iletken tedarik zinciri bütünlüğü; iç tehdit değil ama tedarik zinciri boyutu güçlü ve merkezi |

## 5. Değerlendirme

| Alan | Bilgi |
|---|---|
| Katkı | Statik dosya/firmware analizinden tamamen farklı bir modalite (fiziksel güç tüketimi) sunuyor; %93,2 tespit oranı (%1 FPR'de, AUC 0,995), tek sınıf GAN ile saldırı örneği gerektirmeden eğitim, tedarik zinciri konuşlandırma noktaları için somut politika tartışması |
| Gap | Tek cihaz/tek oturumda toplanmış veri (dış geçerlilik sınırlı); backdoor komutu gibi workload dışında tetiklenen sabotajları tespit edemiyor (negative control ile gösterilmiş, AUC=0); kod/veri paylaşılmamış |
| Uygunluk Skoru (1-5) | 4 |
| Ek Notlar | "Tool-level success bütünlüğü garanti etmez" temasına paralel olarak, bu makale de standart fonksiyonel testlerin bazı sabotaj türlerini (backdoor negative control) kaçırdığını gösteriyor — P14 (Holy Stone drone firmware) ile birlikte okunabilir; farklı modalite olduğu için related work/gap analizi bölümünde değerli |
