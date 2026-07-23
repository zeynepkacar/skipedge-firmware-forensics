# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P07 |
| Başlık | Binary Diff Summarization using Large Language Models |
| Yazarlar | Meet Udeshi, Venkata Sai Charan Putrevu, Prashanth Krishnamurthy, Prashant Anantharaman, Sean Carrick, Ramesh Karri, Farshad Khorrami |
| Yıl | 2025 |
| Yayın Yeri (Venue) | arXiv preprint, arXiv:2509.23970 [cs.CR] |
| DOI / Link | 10.48550/arXiv.2509.23970 — https://arxiv.org/abs/2509.23970 |
| Anahtar Kelimeler | Binary diffing, large language models, software supply chain security, malware detection, reverse engineering, Ghidra, Ghidriff, Functional Sensitivity Score, XZ backdoor |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Genel amaçlı binary executables ve libraries. Deneylerde Ubuntu 20.04 üzerinde GCC 9.4.0 ile derlenen gzip, OpenSSL, tar, SQLite, GNU libmicrohttpd ve Eclipse Paho MQTT projeleri kullanılmıştır. Çalışma firmware'e özel değildir; ancak binary-level differential analysis yaklaşımı firmware binary'lerine metodolojik olarak uygulanabilir.
- **Analiz Türü:** Statik ve diferansiyel binary analysis + LLM tabanlı semantik özetleme/sınıflandırma. Eski ve yeni binary sürümleri karşılaştırılır; yalnızca eklenen, silinen ve değiştirilen fonksiyonlar sonraki analiz aşamalarına taşınır.
- **Tespit Edilen Tehdit Türü:** Software supply-chain sırasında binary update içerisine enjekte edilen kötü amaçlı kod. Benchmark'ta ransomware, remote-access trojan/reverse shell ve botnet/DoS davranışları incelenmektedir. Gerçek dünya vaka çalışmasında XZ Utils/liblzma supply-chain backdoor'u analiz edilmektedir.
- **Kullanılan Ana Teknik/Algoritma:** Ghidriff/Ghidra ile old-vs-new binary diffing; added/deleted/modified function extraction; Python difflib ile decompiled textual diff; yalnızca değişen fonksiyonları içeren diff callgraph; LLM tabanlı function/diff summarization; CVSS'ten esinlenen Functional Sensitivity Score (FSS) ve en yüksek FSS'li fonksiyonlardan `MALICIOUS` / `BENIGN` tahmini.

  **FSS Kategorileri:** Sensitive behaviors, sensitive resources, confidentiality impact, integrity impact ve availability impact. Her kategori none/low/medium/high olarak sınıflandırılır ve 0–10 arası tek FSS değerinde birleştirilir.

  **Kullanılan Modeller:** GPT-5 mini, GPT-5 nano, GPT OSS 20B, Qwen3 30B ve Qwen3 8B. XZ vaka çalışmasında GPT-5 de değerlendirilmiştir.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Yazarlar software supply-chain security için kendi benchmark'larını oluşturmuştur. Altı açık kaynak proje kullanılmıştır: gzip, OpenSSL, tar, SQLite, GNU libmicrohttpd ve Eclipse Paho MQTT. Toplam 104 binary version, 98 consecutive clean software-update pair ve malware injection varyantlarıyla toplam 392 binary diff oluşturulmuştur. Diff'lerde toplam 46.023 added/deleted/modified function bulunmaktadır. Her projeye üç malware uygulanmıştır: `rware` (ransomware), `rat` (remote access trojan/reverse shell) ve `botnet` (DoS bot).
- **Veri Seti Erişilebilir mi?** Hayır — makalenin arXiv kaydında veya metninde oluşturulan 104-version/392-diff benchmark için bağımsız bir açık dataset repository bağlantısı belirtilmemektedir. Kullanılan temel projelerin açık kaynak olması, araştırmacıların oluşturduğu malware-injected benchmark'ın ayrıca yayımlandığı anlamına gelmemektedir.
- **Kaynak Kod Açık mı?** Hayır — makalenin kendi binary-diff summarization framework'ü için resmi kaynak kod repository bağlantısı belirtilmemektedir. Çalışma açık kaynak Ghidriff aracını binary diffing aşamasında kullanmaktadır; ancak Ghidriff makalenin kendi framework kodu değildir.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Evet | Çalışmanın merkezinde doğrudan `old` ve `new` binary karşılaştırması vardır. Added, deleted ve modified fonksiyonlar çıkarılır ve yalnızca değişiklikler sonraki analizde değerlendirilir. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Ghidriff/Ghidra binary diffing, decompilation, textual diff, diff callgraph, LLM summarization, FSS scoring ve LLM malicious/benign prediction ardışık olarak kullanılmaktadır. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Binary'lerin acquisition bütünlüğü, hash tabanlı evidence verification, zaman damgası veya chain-of-custody kaydı ele alınmamaktadır. |
| Tek Bir Şüphe Skoru ile Özetleme | Evet | FSS, fonksiyon hassasiyetini beş güvenlik kategorisinden türeterek 0–10 arasında tek bir skor üretmektedir. En yüksek FSS'li fonksiyonlar final malicious/benign prediction için kullanılmaktadır. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Evet | Makalenin ana motivasyonu software supply-chain security'dir. Benchmark temiz software update'lerine malware injection yapılarak oluşturulmuştur ve XZ Utils supply-chain backdoor'u gerçek dünya vaka çalışmasıdır. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Bu çalışma projem açısından literatürdeki en doğrudan ilişkili çalışmalardan biridir. Temel pipeline eski/güvenilir binary ile yeni binary'nin karşılaştırılması → değişen fonksiyonların çıkarılması → değişikliklerin semantik değerlendirilmesi → sensitivity score ile önceliklendirme → malicious/benign kararı şeklindedir. Bu yapı güvenilir ve şüpheli firmware imajlarını diferansiyel analiz etme yaklaşımıyla önemli ölçüde örtüşmektedir.

  Özellikle Functional Sensitivity Score (FSS) projemdeki birleşik şüphe skoru açısından güçlü bir akademik referanstır. FSS, CVSS yaklaşımından esinlenerek sensitive behavior/resource ve confidentiality/integrity/availability impact kategorilerini sınıflandırmakta ve bunları 0–10 arasında tek bir değerde birleştirmektedir. Bu, projemde farklı analiz katmanlarından elde edilen hash, dosya, entropi, YARA ve permission gibi bulguların tek bir suspicion score altında toplanması fikriyle metodolojik benzerlik taşımaktadır.

  Diff callgraph yaklaşımı da önemlidir. Yalnızca değişen fonksiyonların daha derin analize aktarılması hem işlem maliyetini azaltmakta hem de analizi kritik farklılıklara odaklamaktadır. Benzer prensip firmware analizinde yalnızca değişen dosya/binary/component'lerin ileri analiz katmanlarına gönderilmesinde kullanılabilir. Gerçek XZ Utils backdoor vakasının incelenmesi de supply-chain manipülasyonu açısından güçlü bir gerçek dünya örneğidir.
- **Eksik bıraktığı nokta (Gap):** Makale firmware'e özel değildir ve karşılaştırmayı ağırlıklı olarak executable/library içerisindeki fonksiyon seviyesinde binary diff olarak gerçekleştirir. Firmware filesystem extraction, eklenen/silinen/değiştirilen dosyaların bütüncül karşılaştırılması, firmware entropy analizi, YARA scanning, permission/ownership değişiklikleri, configuration artefact'ları ve firmware-specific metadata analizi kapsam dışındadır.

  İkinci önemli eksiklik adli bilişim boyutudur. Binary'lerin SHA-256 gibi hash'lerle acquisition öncesi/sonrası doğrulanması, evidence ID, timestamp, examiner/action logging ve chain-of-custody gibi adli bütünlük mekanizmaları sunulmamaktadır.

  Ayrıca FSS büyük ölçüde LLM değerlendirmesine dayanır. Makalede FSS için insan tarafından etiketlenmiş function-level ground truth bulunmadığı belirtilmekte; injected malware functions ile benign functions arasındaki skor dağılımı karşılaştırılmaktadır. Final malware detection recall'ının en iyi durumda 0.64 olması da bazı malicious update'lerin kaçırılabildiğini göstermektedir.

  **Projemin bu makaleye göre temel farkı:** Bu çalışma binary/function seviyesinde LLM destekli differential analysis ve FSS sunarken benim projem firmware imajı seviyesinde çok katmanlı diferansiyel adli analiz hedeflemektedir. Projem dosya sistemi ve firmware artefact'larını farklı statik analiz yöntemleriyle incelemeyi, sonuçları kriptografik delil bütünlüğü altında saklamayı ve tüm katmanların bulgularını birleşik bir firmware suspicion score'da değerlendirmeyi amaçlamaktadır.
- **Uygunluk Skoru (1–5):** 5
- **Ek Notlar:** Benchmark toplam 104 binary version, 392 binary diff ve 46.023 değişen fonksiyon içermektedir. En iyi sonuç GPT-5 mini ile 0.98 precision ve 0.64 recall olarak raporlanmıştır. GPT-5 mini için malicious ve benign fonksiyonların median FSS değerleri arasında 3.0 puanlık ayrım bulunmuştur. XZ Utils vaka çalışmasında compromised v5.6.0 ile önceki v5.4.7 sürümü karşılaştırılmış; 79 diff fonksiyonu arasındaki gerçek backdoor fonksiyonları top-5 FSS listesine girmiştir. Yazarlar gelecekte vulnerability detection, patch analysis ve daha geniş mimari desteğini olası genişleme alanları olarak belirtmektedir.
