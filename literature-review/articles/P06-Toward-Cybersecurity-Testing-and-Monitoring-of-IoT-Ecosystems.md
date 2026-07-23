# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P06 |
| Başlık | Toward Cybersecurity Testing and Monitoring of IoT Ecosystems |
| Yazarlar | Steve Taylor, Martin Gilje Jaatun, Aida Omerovic, Ravi Borgaonkar, Robert Seidl, Norbert Goetze, Jens Kuhr, Dmytro Prosvirin, Manuel Leone, Andrey Kuznetsov, Anatoliy Gritskevich, Antonis Mpantis, Oscar Garcia Perales, Bernd-Ludwig Wenning, Sayon Duttagupta |
| Yıl | 2026 |
| Yayın Yeri (Venue) | SN Computer Science, 7:468, Springer Nature |
| DOI / Link | 10.1007/s42979-026-05048-8 |
| Anahtar Kelimeler | Security testing, security monitoring, IoT, tool chains, workflow, software supply chain, cyber physical systems, systemic vulnerability, threat and risk analysis |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Tek bir CPU mimarisiyle sınırlı değildir. IoT cihazlarını ve bunların içinde bulunduğu daha geniş ekosistemleri Device Under Test (DUT) ve System Under Test (SUT) perspektiflerinden ele alır. Çalışmada havacılık kargo izleme sistemleri, akıllı üretim ortamları ve telekomünikasyon residential gateway/router cihazları üzerinde kullanım senaryoları bulunmaktadır.
- **Analiz Türü:** Hibrit ve çok katmanlı. Tasarım/build aşamasındaki güvenlik testlerini, firmware/binary analizi, SBOM üretimi ve network fuzzing'i; çalışma zamanında ise sistem/ağ izleme ve makine öğrenmesi tabanlı anomaly detection yöntemlerini bir araya getirir. Bunlara dinamik risk değerlendirmesi, secure software update ve auditable evidence management katmanları eklenmiştir.
- **Tespit Edilen Tehdit Türü:** Tek bir tehdit türüne odaklanmaz. Bilinen CVE'ler ve üçüncü taraf kütüphane zafiyetleri, bilinmeyen network/interface zafiyetleri, anomalous network/device behaviour, kötüye kullanım, kritik dosya veya process değişiklikleri, erişim kontrolü riskleri, firmware/software supply-chain zafiyetleri ve interconnected sistemlerde threat propagation gibi çok sayıda güvenlik problemi ele alınır.
- **Kullanılan Ana Teknik/Algoritma:** Çalışmanın ana katkısı tek bir algoritmadan ziyade TELEMETRY adlı extensible cybersecurity testing and monitoring architecture'dır. Başlıca bileşenler:
  1. **Network Fuzzer:** Açık kaynak boofuzz üzerine kuruludur. PCAP verilerinden test girdileri üretip network interface'lerine crafted requests göndererek beklenmeyen davranışları ve bilinmeyen zafiyetleri araştırır.
  2. **SBOM Generator:** Binary/firmware'den sonradan SBOM üretmeyi amaçlar. QEMU ile emülasyon, Binwalk ile firmware extraction, printable-string analizi ve NVD/CVE eşleştirmesi kullanır. Vendor tarafından sağlanan bir SBOM varsa oluşturulan SBOM ile karşılaştırma da yapılabilir.
  3. **Access Control Risk Evaluation:** Kullanıcı, servis ve etkileşim faktörlerini fuzzy logic ile değerlendirerek high/medium/low erişim kontrolü risk seviyeleri üretir.
  4. **Nokia Anomaly Detection Pipeline (NAD):** Normal sensör davranışından bir fingerprint/model öğrenir ve canlı ölçümlerin beklenen davranıştan sapmasını near-real-time olarak tespit eder.
  5. **Misuse Detection ML Toolkit:** CNN tabanlı modellerle normal kullanıcı/sistem davranışından sapmaları tespit etmeyi amaçlar; açıklanabilirlik için SHAP tabanlı yaklaşım geliştirilmesi de ele alınır.
  6. **r-Monitoring:** CPU/memory metrics, process activity, kritik dosya değişiklikleri, process hash'leri ve network traffic'i izler; signature ve anomaly monitoring gerçekleştirir.
  7. **r-Anomaly Detection:** Canlı network traffic'i normal/baseline dataset ile karşılaştırarak anomaly tespit eder; çıktıda anomaly durumu, sapmanın severity değeri ve abnormal parametreler bulunur.
  8. **Spyderisk System Modeller (SSM):** Knowledge-based system-level risk modelling gerçekleştirir. SBOM/CVE ve diğer araçların ürettiği indicators kullanılarak riskler, tehditler, attack paths ve önerilen controls hesaplanır.
  9. **Secure Software Updates:** Resource-constrained IoT cihazlarına lightweight cryptographic protocols kullanarak validated/authenticated ve encrypted update dağıtmayı hedefler.
  10. **Auditable Data Infrastructure:** Distributed Ledger Technology (DLT) kullanarak events, actions, indicators, test results ve reports için immutable ve auditable kayıt sağlar.
  11. **SIEA Pipeline:** Güvenlik olaylarını toplar, filtreler, aggregate eder ve önceliklendirir.
  12. **Workflow Orchestrator:** Farklı TELEMETRY araçlarını workflow template'leriyle otomatik olarak zincirleyip çalıştırmayı hedefler.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Makale tek ve merkezi bir benchmark/dataset üzerinde değerlendirme yapmamaktadır. TELEMETRY, üç endüstriyel kullanım senaryosu üzerinde doğrulanmaktadır: (1) aircraft cargo monitoring, (2) smart manufacturing ve (3) telecommunications residential gateways. Farklı araçlar kendi kullanım senaryolarına özgü veri kullanmaktadır. Örneğin anomaly detection bileşenleri normal çalışma sırasında elde edilen sensor/network baseline verilerini kullanırken, SBOM Generator firmware/binary girdilerini analiz etmektedir.
- **Veri Seti Erişilebilir mi?** Hayır — makalede üç kullanım senaryosunun deney verilerini tek bir açık veri seti olarak indirmeye yönelik bir dataset repository bağlantısı verilmemiştir.
- **Kaynak Kod Açık mı?** Hayır — makale TELEMETRY framework'ünün tamamı için tek bir resmi açık kaynak repository bağlantısı vermemektedir. Bazı bileşenler açık kaynak araçlar üzerine kuruludur (ör. boofuzz, QEMU, Binwalk), ancak bunlar TELEMETRY'nin kendi kaynak kodu olarak değerlendirilmemelidir.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Kısmen | Projedeki gibi iki firmware imajını A-vs-B şeklinde bütüncül olarak karşılaştıran bir differential firmware forensics modülü yoktur. Bununla birlikte vendor-supplied SBOM ile generated SBOM karşılaştırılabilir; anomaly detection araçları canlı gözlemleri normal baseline ile karşılaştırır; r-Monitoring dosya/hash değişikliklerini izler. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Makalenin en güçlü yönlerinden biridir. Firmware/binary SBOM analizi, fuzzing, runtime monitoring, ML anomaly detection, fuzzy-logic access risk evaluation, system-level risk modelling, secure updates, DLT tabanlı audit infrastructure ve workflow orchestration birlikte kullanılmaktadır. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Evet | Klasik adli chain-of-custody terminolojisini birebir uygulamasa da DLT tabanlı Auditable Data Infrastructure; test configuration, event, indicator, result, decision ve action kayıtlarını immutable ve auditable biçimde saklamak üzere tasarlanmıştır. Bu, projenin delil bütünlüğü/izlenebilirlik kriteriyle doğrudan örtüşmektedir. |
| Tek Bir Şüphe Skoru ile Özetleme | Kısmen | Framework genelinde tek bir birleşik firmware suspicion score yoktur. Ancak çeşitli bileşenler risk/severity çıktıları üretir: access-control aracı high/medium/low risk, r-Anomaly Detection deviation severity, SSM ise impact ve likelihood üzerinden risk levels üretir ve CVE'leri bağlamsal olarak önceliklendirir. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Evet | Software supply-chain güvenliği doğrudan ele alınır. Firmware'in üçüncü taraf ve açık kaynak kütüphanelerden oluşması, SBOM ile bunların görünür hale getirilmesi ve SolarWinds/XZ Utils gibi supply-chain attack örnekleri tartışılır. Misuse Detection bileşeni insan kaynaklı misuse davranışını da ele alır. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Bu çalışma projem açısından şimdiye kadarki en kapsamlı mimari referanslardan biridir. Projemin temel fikri tek bir analiz yöntemine güvenmek yerine firmware üzerinde birden fazla bağımsız analiz katmanından bulgu üretmek ve bunları ortak bir değerlendirmede birleştirmektir. TELEMETRY de benzer biçimde tek bir güvenlik aracının IoT ekosistemlerinin karmaşıklığını çözmek için yeterli olmadığını savunmakta; testing, monitoring, risk assessment, secure update ve auditable evidence management bileşenlerini aynı mimari altında bir araya getirmektedir.

  Özellikle SBOM Generator projemin firmware statik analiz katmanına doğrudan yakındır. Firmware/binary'nin QEMU ve Binwalk gibi araçlarla incelenmesi, içerisindeki library/component bilgilerinin çıkarılması ve NVD üzerinden CVE'lerle eşleştirilmesi, firmware'in yalnızca dosya/hash seviyesinde değil yazılım bileşimi açısından da değerlendirilmesinin önemini göstermektedir.

  Auditable Data Infrastructure projem açısından daha da önemli bir katkıdır. Makale audit ve compliance için testing configuration, result ve diğer verilerin immutable biçimde saklanması gerektiğini açıkça savunmakta ve bunu DLT ile gerçekleştirmektedir. Bu yaklaşım projemdeki delil bütünlüğü, chain-of-custody ve analiz sonuçlarının sonradan değiştirilemediğinin gösterilmesi hedefi için güçlü akademik dayanak sağlar.

  TELEMETRY'nin Indicators yaklaşımı da projemdeki birleşik şüphe skoru açısından değerlidir. Makalede farklı araçların tek başına ürettiği çıktılar veya birden fazla aracın çıktılarının korelasyonu indicator olarak ele alınabilmektedir. Benzer biçimde projemde hash farkı, dosya değişikliği, entropi anomalisi, YARA eşleşmesi, izin değişikliği vb. bağımsız bulguların tek bir risk/şüphe değerlendirmesine dönüştürülmesi savunulabilir.

  Ayrıca TELEMETRY'nin araçları workflow template'leri aracılığıyla zincirleme ve otomatik çalıştırma fikri, projemdeki analiz pipeline'ının mimari tasarımında kullanılabilecek önemli bir referanstır.
- **Eksik bıraktığı nokta (Gap):** TELEMETRY çok kapsamlı olmasına rağmen firmware forensics'e özel bir differential A-vs-B analysis sistemi değildir. Orijinal/güvenilir firmware ile şüpheli firmware'in hash, filesystem, file addition/deletion/modification, entropy, YARA, permission/privilege ve benzeri artefact'lar açısından sistematik biçimde karşılaştırıldığı tek bir analiz pipeline'ı sunulmamaktadır.

  Framework çok sayıda bağımsız araçtan oluştuğu için sonuçlar da farklı format ve risk seviyelerinde üretilmektedir. Makale bütün bu çıktıları firmware özelinde tek bir normalize edilmiş suspicion score altında birleştiren bir yöntem önermemektedir. Ayrıca DLT tabanlı auditability güçlü olmasına rağmen klasik dijital adli bilişim chain-of-custody sürecindeki acquisition hash'i, examiner/action log, evidence ID ve adli raporlama gibi prosedürler firmware incelemesine özel biçimde tanımlanmamıştır.

  Makalenin kendi sınırlamalarından biri de framework'ün halen gelişmekte olmasıdır. Yazarlar araçların sonlandırılması, daha fazla test edilmesi, use-case'lere göre yeni tool combinations/workflows geliştirilmesi ve normal davranışın deployment context'e göre değişmesi nedeniyle anomaly modellerinin özelleştirilmesi/dinamik adapte edilmesi gerektiğini belirtmektedir.

  **Projemin bu makaleye göre temel farkı:** TELEMETRY bütün IoT lifecycle'ını kapsayan geniş bir cybersecurity testing/monitoring ecosystem'i sunarken benim projem daha dar fakat daha derin biçimde firmware forensics problemine odaklanmaktadır. Projem, güvenilir ve şüpheli firmware imajlarını diferansiyel olarak karşılaştırmayı; çok katmanlı statik bulguları adli bütünlük altında kaydetmeyi ve sonuçları tek bir birleşik şüphe skorunda özetlemeyi hedeflemektedir.
- **Uygunluk Skoru (1–5):** 5
- **Ek Notlar:** Makale TELEMETRY yaklaşımını üç endüstriyel senaryoda değerlendirir: aviation cargo monitoring, smart manufacturing ve telecommunications residential gateways. Residential Gateway senaryosunda network fuzzing, commercial firmware'de OpenWRT'ye kıyasla ek bir servisi crash ederek daha önce raporlanmamış bir zafiyetin ortaya çıkarılmasına yardımcı olmuştur. SBOM Generator, firmware/binary içerisindeki libraries/components'i CVE'lerle ilişkilendirerek system-level risk modeline girdi sağlar. r-Monitoring ZTE router üzerinde test edilmiş; Nokia Anomaly Detection Pipeline smart-manufacturing robot sensörlerindeki speed/joint-angle anomalilerini izlemek için kullanılmıştır. SIEA Pipeline dört uygulamayla gerçekleştirilmiş ve Docker tabanlı özelleştirilmiş deployment yaklaşımı kullanılmıştır. Makalenin sonuç bölümünde framework'ün ilk bileşenlerinin geliştirildiği ve kullanım senaryolarında değerlendirildiği, ancak araçların ve workflow'ların geliştirilmesinin devam ettiği açıkça belirtilmektedir.
