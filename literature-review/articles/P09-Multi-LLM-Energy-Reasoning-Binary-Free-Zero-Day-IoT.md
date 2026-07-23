# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P09 |
| Başlık | Multi-LLM Energy Reasoning for Binary-Free Zero-Day IoT Detection |
| Yazarlar | Saeid Jamshidi, Foutse Khomh, Kawser Wazed Nafi, Omar Abdul-Wahab, Martine Bellaïche |
| Yıl | 2025 (ilk arXiv sürümü; güncel v2: 12 Haziran 2026) |
| Yayın Yeri (Venue) | arXiv preprint, arXiv:2512.19945 [cs.CR] |
| DOI / Link | 10.48550/arXiv.2512.19945 — https://arxiv.org/abs/2512.19945 |
| Anahtar Kelimeler | IoT firmware, zero-day risk estimation, binary-free analysis, architecture-agnostic analysis, multi-LLM reasoning, LLaMA 3-8B, DeepSeek v3, GPT-4o, energy-aware reasoning, firmware descriptors |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Mimari-bağımsız (architecture-agnostic) IoT firmware. Yöntem firmware binary'sinin açılmasını, disassembly/decompilation yapılmasını veya emülasyon kurulmasını gerektirmemektedir.
- **Analiz Türü:** Binary-free, descriptor-level, LLM tabanlı risk tahmini. Sistem gerçek bir exploit'i doğrulamaktan ziyade yüksek seviyeli firmware descriptor'larından conceptual zero-day likelihood tahmini yapmaktadır.
- **Tespit Edilen Tehdit Türü:** Bilinen CVE veya imzaya bağlı olmayan; misconfiguration, privilege misallocation, unsafe default credentials, zayıf service isolation, structural irregularity ve kırılgan service interaction gibi koşullardan kaynaklanabilecek latent/conceptual zero-day riskleri.
- **Kullanılan Ana Teknik/Algoritma:** Üç aşamalı LLM reasoning pipeline:
  1. **LLaMA 3-8B Configuration Interpreter:** service activation, privilege allocation, credential/policy ve exposure özelliklerini yorumlar.
  2. **DeepSeek v3 Structural Abstraction Analyzer:** call-graph eğilimleri, control-flow göstergeleri ve opcode-shape gibi non-executable structural proxy'leri değerlendirir.
  3. **GPT-4o Semantic Fusion:** İlk iki aşamanın schema-constrained textual summary'lerini birleştirerek conceptual zero-day likelihood üretir.

  **Ek Sinyaller:** Cross-layer divergence, Euclidean misalignment, entropy/uncertainty, latency, CPU/GPU index, token-flow ve symbolic energy/load surrogate.

  **Risk Çıktısı:** Sistem descriptor-level kanıttan bounded/probabilistic bir conceptual zero-day likelihood üretmektedir. Enerji/load göstergeleri primary security evidence değil, deployment/resource-aware yardımcı sinyaller olarak kullanılmaktadır.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Çalışmanın ana değerlendirmesi kontrollü synthetic firmware descriptors üzerinde simulation-based olarak yapılmıştır. Descriptor tasarımı ve gerçek-dünya uygulanabilirlik değerlendirmesi Firmadyne, OpenWrt ve Firmware Analysis Toolkit gibi kamuya açık firmware kaynaklarından esinlenmektedir. Ayrıca OpenWrt, RouterOS ve vendor-provided encrypted firmware örneklerinden metadata, configuration entries ve structural statistics düzeyinde descriptor'lar değerlendirilmiştir. Önemli not: Makale gerçek firmware dağılımını temsil ettiğini iddia eden klasik bir benchmark veri seti sunmamaktadır; sentetik descriptor'lar kontrollü sensitivity analysis için oluşturulmuştur. Yazarlar gerçek zero-day ground-truth etiketlerinin bulunmadığını açıkça belirtmektedir.
- **Veri Seti Erişilebilir mi?** Hayır / Ayrı veri seti yayımlanmamış — makalenin kendi synthetic descriptor evaluation dataset'i için ayrı ve doğrulanabilir bir dataset repository bağlantısı arXiv kaydında verilmemektedir. Firmadyne/OpenWrt/Firmware Analysis Toolkit çalışmanın kendi veri seti değildir.
- **Kaynak Kod Açık mı?** Hayır / Belirtilmemiş — arXiv makale sayfasında çalışmanın tri-LLM implementation'ına ait doğrulanabilir resmi GitHub/kod repository bağlantısı belirtilmemektedir.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Orijinal/güvenilir firmware ile şüpheli firmware imajı karşılaştırılmamaktadır. Descriptor perturbation ve farklı risk koşulları karşılaştırılsa da bu A-vs-B firmware differential analysis değildir. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Configuration reasoning, structural abstraction, semantic fusion, cross-layer divergence/uncertainty ve resource-aware auxiliary signals birlikte kullanılmaktadır. Ancak katmanlar klasik bağımsız firmware-forensics araçlarından ziyade aynı tri-LLM reasoning mimarisinin bileşenleridir. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Evidence acquisition hash'i, chain-of-custody log'u, examiner/action history veya kriptografik delil doğrulaması bulunmamaktadır. |
| Tek Bir Şüphe Skoru ile Özetleme | Evet | Sistem configuration ve structural evidence'i fusion katmanında birleştirerek bounded/probabilistic conceptual zero-day likelihood/risk score üretmektedir. Bu yönü projenin birleşik şüphe skoru fikriyle doğrudan ilişkilidir. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Makale firmware opacity ve latent zero-day riskine odaklanmaktadır. Software supply-chain veya insider manipulation çalışmanın temel tehdit modeli değildir. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Bu çalışma projem için özellikle çok katmanlı bulgu birleştirme ve tek bir risk skoru üretme açısından yararlı bir referanstır. Üç farklı reasoning view'un — configuration, structural abstraction ve semantic fusion — ayrı değerlendirilip daha sonra ortak bir conceptual risk çıktısına dönüştürülmesi, projemde hash, entropy, YARA ve permission analysis gibi farklı katmanların tek bir firmware suspicion score altında birleştirilmesi fikrine metodolojik destek sağlamaktadır.

  Çalışmanın ikinci önemli katkısı, klasik firmware analizinin çalışamadığı durumlara alternatif bir yaklaşım göstermesidir. Firmware encrypted, proprietary, partially corrupted veya binary olarak erişilemez olduğunda sistem metadata, configuration semantics, service manifests ve non-executable structural proxy'lerle çalışmayı amaçlamaktadır. Bu, projem için ana analiz yöntemi olmaktan ziyade gelecekte firmware tamamen unpack edilemediğinde yardımcı/fallback risk estimation katmanı olarak düşünülebilecek bir fikir sunmaktadır.

  Ayrıca ablation sonuçlarında fusion katmanının kaldırılmasının belirgin performans kaybı oluşturması, farklı kanıt türlerini sadece yan yana koymanın değil, aralarındaki ilişkileri değerlendiren bir fusion mekanizmasının önemini göstermektedir.
- **Eksik bıraktığı nokta (Gap):** Makale başlığındaki "zero-day detection" ifadesine rağmen çalışma gerçek bir zero-day exploit'i tespit edip doğruladığını iddia etmemektedir; güncel v2 metni özellikle çıktının conceptual zero-day likelihood estimation olduğunu ve exploit confirmation olmadığını vurgulamaktadır. Bu ayrım önemlidir.

  Projem açısından en büyük eksiklik, firmware binary'sini özellikle analiz etmemesidir. SHA-256 bütünlük kontrolü, A-vs-B firmware comparison, filesystem extraction, added/deleted/modified file detection, entropy analysis, YARA scanning, permission/ownership değişiklikleri ve binary-level artefact analizi bulunmamaktadır. Bu nedenle firmware forensics açısından doğrudan uygulanabilirliği P07 gibi binary-diff çalışmalarına göre daha düşüktür.

  Ayrıca chain of custody veya kriptografik evidence integrity bulunmamaktadır. Değerlendirmenin önemli bölümü synthetic descriptors ve proxy ground-truth üzerinden yapılmıştır; gerçek zero-day ground truth mevcut değildir. Makalenin kendisi de correlation'ın predictive accuracy veya exploit confirmation anlamına gelmediğini açıkça belirtmektedir.

  Enerji tarafında da ölçülen değerler fiziksel enerji tüketimi değildir. CPU/GPU, latency ve token-flow'dan türetilen relative symbolic energy/load surrogate kullanılmaktadır. Dolayısıyla "energy-efficient" sonucu gerçek cihaz güç ölçümü olarak yorumlanmamalıdır.

  **Projemin bu makaleye göre temel farkı:** Bu çalışma binary erişimi olmadan descriptor-level LLM reasoning ile kavramsal zero-day riskini tahmin ederken benim projem firmware imajının kendisini adli olarak inceleyen, güvenilir ve şüpheli firmware arasında diferansiyel analiz yapan, çoklu statik analiz katmanlarını kullanan, kriptografik delil bütünlüğünü hedefleyen ve sonuçları birleşik firmware suspicion score'da özetleyen bir firmware-forensics sistemidir.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** Güncel arXiv v2, 12 Haziran 2026 tarihlidir. Controlled descriptor perturbation deneylerinde daha yüksek exposure koşullarının tahmin edilen conceptual zero-day likelihood değerlerini modeller genelinde yaklaşık %20–35 artırdığı raporlanmıştır. Proxy-ground-truth karşılaştırmasında tri-LLM sisteminin correlation değeri 0.72 (R²=0.52) olarak verilmiş; descriptor bileşenlerinin %20–50'si maskelendiğinde de korelasyonun yaklaşık 0.67–0.71 aralığında kaldığı raporlanmıştır. GPT-4o daha yüksek ortalama conceptual risk ve daha yüksek resource/energy index üretirken, LLaMA 3-8B daha düşük operational cost göstermiştir. Bu sonuçlar exploit-detection accuracy değil, descriptor-level risk-estimation davranışı olarak yorumlanmalıdır.
