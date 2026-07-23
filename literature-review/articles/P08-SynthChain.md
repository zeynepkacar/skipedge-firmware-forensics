# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P08 |
| Başlık | SynthChain: A Synthetic Benchmark and Forensic Analysis of Advanced and Stealthy Software Supply Chain Attacks |
| Yazarlar | Zhuoran Tan, Wenbo Guo, Taylor Brierley, Jiewen Luo, Jeremy Singer, Christos Anagnostopoulos |
| Yıl | 2026 |
| Yayın Yeri (Venue) | arXiv preprint, arXiv:2603.16694v1 [cs.CR] |
| DOI / Link | 10.48550/arXiv.2603.16694 — https://arxiv.org/abs/2603.16694 |
| Anahtar Kelimeler | Software supply chain, digital forensics, multi-source telemetry, attack-chain reconstruction, provenance, runtime analysis, MITRE ATT&CK, eBPF, PyPI, npm |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Firmware veya belirli bir CPU mimarisine özel değildir. Windows ve Linux hostlar ile Docker tabanlı container workload'larını kapsayan near-production bir software supply-chain testbed kullanılır. PyPI, npm ve native C/C++ supply-chain senaryoları incelenmektedir.
- **Analiz Türü:** Dinamik, runtime ve forensic-oriented multi-source telemetry analysis. Host, process, system/authentication, network ve service-level telemetry birlikte analiz edilerek saldırı zincirleri yeniden oluşturulur.
- **Tespit Edilen Tehdit Türü:** Gelişmiş ve stealthy software supply-chain saldırıları. Typosquatting, dependency-chain saldırıları, CI/CD compromise, trojanized installer, DLL side-loading/process injection, fileless execution, steganography/obfuscation, persistence, C2, credential/token abuse, data theft ve exfiltration gibi davranışlar ele alınır.
- **Kullanılan Ana Teknik/Algoritma:** SynthChain öncelikle bir benchmark/testbed ve forensic analysis pipeline'ıdır. Yedi uçtan uca saldırı senaryosu oluşturulur; senkronize çok kaynaklı telemetry toplanır; olaylar normalize/anonymize edilir; MITRE ATT&CK ile etiketlenir; coarse attack-step tagging uygulanır; farklı kaynaklardaki olaylar ortak host/process/user/network endpoint gibi join key'ler üzerinden korele edilerek attack chain reconstruction yapılır.

  **Ground Truth:** C2 tarafından yürütülen adımlar Mythic tasking kayıtları ve ATT&CK mapping ile; payload-originated davranışlar ise GPT-5.1 destekli ATT&CK önerileri, insan doğrulaması, multi-annotator cross-checking ve adjudication ile etiketlenmiştir.

  **Senaryolar:** Stegano, Starter, Parallel, NPMEX, 3CX, CloudEX ve LayerInj olmak üzere 7 senaryo bulunmaktadır. Senaryolar gerçek kötü amaçlı paketler ve exploit campaign'lerden türetilmiştir.

  **Çok Kaynaklı Analiz:** Tek kaynak, iki kaynak ve üç veya daha fazla kaynak içeren telemetry kombinasyonları ayrı ayrı değerlendirilerek hangi kanıt kaynaklarının attack-chain reconstruction için gerekli olduğu ölçülmektedir.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** SynthChain, yaklaşık 0,58 milyon raw multi-source event ve 1,50 milyon evaluation row içeren runtime dataset sunmaktadır. Yedi supply-chain saldırı senaryosu PyPI, npm ve native C/C++ ekosistemlerini; Windows, Linux ve container ortamlarını kapsamaktadır. Senaryolar toplam 14 MITRE ATT&CK tactic ve 161 technique ile ilişkilendirilmiştir; senaryo başına 29–104 teknik bulunmaktadır.
- **Veri Seti Erişilebilir mi?** Evet — makale dataset, chain-level ground truth ve artifacts'ın yayımlandığını açıkça belirtmektedir. Ancak arXiv v1 metninde ayrı bir doğrulanabilir dataset/GitHub URL'si görünmediğinden burada bağlantı uydurulmamıştır; resmi artifact URL'si ayrıca doğrulandığında eklenmelidir.
- **Kaynak Kod Açık mı?** Hayır / Belirtilmemiş — makale dataset, ground truth ve artifacts'ın release edildiğini belirtse de SynthChain analiz pipeline'ının kaynak koduna ait doğrulanabilir resmi bir GitHub repository bağlantısı arXiv v1 metninde belirtilmemektedir. Makalede kullanılan Mythic/Apollo/Medusa gibi açık kaynak araçlar SynthChain'in kendi kaynak kodu değildir.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Güvenilir A firmware ile şüpheli B firmware'i dosya/binary/hash seviyesinde karşılaştırılmaz. Çalışmanın karşılaştırma ekseni farklı telemetry-source kombinasyonlarının saldırı zincirini ne ölçüde gözlemleyip yeniden oluşturabildiğidir. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Host/process telemetry, system/auth logs, network/service traces ve eBPF tabanlı behavioral tracing gibi heterojen kanıt kaynakları birlikte korele edilir. Makalenin ana bulgularından biri tek kaynağın yetersiz, tamamlayıcı çoklu kaynakların ise daha etkili olduğudur. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Kısmen | Çalışma güçlü biçimde forensic-aware'dır; chain-level ground truth, provenance context, collection-origin/trust-domain ayrımı, zaman çizelgesi ve cross-source evidence alignment sağlar. Ancak klasik chain-of-custody prosedürü, evidence acquisition hash'i, examiner/action log veya kriptografik evidence sealing mekanizması sunmaz. |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | 0–100 benzeri tek bir suspicion/risk score yoktur. Tag coverage, chain coverage, step/chain precision-recall ve reconstructability gibi ayrı metrikler kullanılır. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Evet | Makalenin tamamı advanced software supply-chain compromise üzerinedir. Dependency/package saldırıları, CI/CD compromise, 3CX benzeri trojanized software ve diğer çok aşamalı supply-chain senaryoları doğrudan modellenir. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** SynthChain projem için özellikle çok katmanlı analiz, tedarik zinciri tehdidi ve adli kanıt korelasyonu açısından güçlü bir referanstır. Çalışmanın temel sonucu, tek bir telemetry/kanıt kaynağının gelişmiş supply-chain saldırısının tamamını açıklamak için yeterli olmadığıdır. En iyi tek kaynak yalnızca 0.391 weighted coverage ve 0.403 mean chain reconstruction elde ederken, tamamlayıcı iki kaynağın birleştirilmesi coverage'ı 0.636'ya ve reconstruction'ı 0.639'a çıkarmaktadır. Bu sonuç, projemde hash, entropi, YARA ve permission analysis gibi farklı katmanların birlikte değerlendirilmesinin neden gerekli olduğunu kavramsal olarak desteklemektedir.

  Makalenin cross-source evidence alignment yaklaşımı da projem açısından önemlidir. SynthChain farklı log/telemetry kaynaklarında dağılmış kanıtları host, process, user ve network endpoint gibi ortak bağlar üzerinden birleştirerek saldırı zincirini yeniden oluşturmaktadır. Benzer biçimde projemde farklı analiz katmanlarından gelen bulguların tek bir firmware değişikliği veya artefact etrafında korele edilmesi, tek başına bir bulgunun sağlayamayacağı daha güçlü bağlamsal kanıt oluşturabilir.

  Çalışmanın forensic-aware yaklaşımı ve chain-level ground truth sağlaması, adli bilişim tarafında da değerlidir. Özellikle attacker-side ve target-side telemetry'nin collection origin bilgisinin korunması ve trust-domain sınırlarının açıkça işaretlenmesi, kanıtın kaynağının ve bağlamının korunmasının önemini göstermektedir.

  Ayrıca dataset'in gerçek supply-chain olaylarından türetilen yedi senaryo içermesi, projemdeki supply-chain/insider manipulation threat modelini gerekçelendirmek için kullanılabilir.
- **Eksik bıraktığı nokta (Gap):** SynthChain projemle aynı problemi çözmemektedir. En önemli fark, çalışmanın firmware bütünlüğü veya firmware image differential analysis yapmamasıdır. Orijinal firmware ile şüpheli firmware'in SHA-256 hash, filesystem, added/deleted/modified files, entropy, YARA signatures veya permission changes açısından karşılaştırılması bulunmamaktadır. Analiz saldırı gerçekleştikten sonra oluşan runtime telemetry ve attack-chain reconstruction üzerine kuruludur.

  İkinci olarak, çalışma forensic-aware olsa da klasik anlamda tam bir chain of custody sistemi sunmaz. Evidence acquisition sırasında kriptografik hash alma, evidence ID, timestamped examiner actions ve delilin analiz boyunca değişmediğinin kriptografik olarak doğrulanması gibi mekanizmalar tanımlanmamıştır.

  Üçüncü olarak, makale farklı kanıt kaynaklarını korele etmesine rağmen sonuçları tek bir suspicion score altında birleştirmemektedir. Bunun yerine coverage, recall, precision ve reconstructability gibi birden fazla değerlendirme metriği kullanılmaktadır.

  Makalenin kendi sonuçları da önemli bir sınırlama göstermektedir: daha fazla telemetry her zaman daha iyi sonuç vermemektedir. Eğer eklenen kaynak saldırının eksik aşamasını görünür hale getirmiyor veya diğer kaynaklarla bağlanabilir join key sağlamıyorsa yalnızca gürültü ve veri hacmi artmaktadır. Bu, projem açısından da önemlidir: çok katmanlı olmak tek başına yeterli değildir; katmanların birbirini tamamlayan ve anlamlı bulgular üretmesi gerekir.

  **Projemin bu makaleye göre temel farkı:** SynthChain runtime'da oluşmuş heterojen telemetry'yi birleştirerek software supply-chain saldırı zincirini adli olarak yeniden oluştururken benim projem firmware imajının kendisine odaklanan, güvenilir ve şüpheli firmware arasında diferansiyel analiz yapan, çoklu statik analiz katmanlarını birleştiren, kriptografik delil bütünlüğü hedefleyen ve sonuçları tek bir firmware suspicion score ile özetlemeyi amaçlayan bir firmware-forensics sistemidir.
- **Uygunluk Skoru (1–5):** 4
- **Ek Notlar:** SynthChain yaklaşık 0,58 milyon raw event ve 1,50 milyon evaluation row içermektedir. En iyi single-source yaklaşım 0.391 weighted coverage ve 0.403 mean reconstructability sağlarken, en iyi two-source kombinasyonu 0.636 coverage ve 0.639 reconstructability değerine ulaşmaktadır. Çalışma, tamamlayıcı kaynak seçiminin kaynak sayısından daha önemli olduğunu göstermektedir. Dataset/testbed karşılaştırmasında SynthChain; supply-chain specific, multi-stage, multi-source, explicit alignment, ATT&CK TTP mapping, Tracee/eBPF ve normal behavior özelliklerinin tümünü birlikte sağlayan çalışma olarak sunulmaktadır. Bununla birlikte firmware analizi, A-vs-B firmware karşılaştırması ve birleşik suspicion score bulunmadığından projem açısından 5/5 değil, 4/5 daha dengeli bir uygunluk değerlendirmesidir.
