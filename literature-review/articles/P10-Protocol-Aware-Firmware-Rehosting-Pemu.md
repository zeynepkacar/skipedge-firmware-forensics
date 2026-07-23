# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

  ------------------------------------------------------------------------------------
  Alan                                Bilgi
  ----------------------------------- ------------------------------------------------
  Makale ID                           P10

  Başlık                              Protocol-Aware Firmware Rehosting for Effective
                                      Fuzzing of Embedded Network Stacks

  Yazarlar                            Moritz Bley, Tobias Scharnowski, Simon Wörner,
                                      Moritz Schloegel, Thorsten Holz

  Yıl                                 2025

  Yayın Yeri (Venue)                  Proceedings of the 2025 ACM SIGSAC Conference on
                                      Computer and Communications Security (CCS '25),
                                      Taipei, Taiwan

  DOI / Link                          10.1145/3719027.3765125 ---
                                      https://dl.acm.org/doi/10.1145/3719027.3765125

  Anahtar Kelimeler                   Firmware fuzzing, firmware rehosting, network
                                      fuzzing, embedded network stacks, protocol-aware
                                      fuzzing, software security, Pemu
  ------------------------------------------------------------------------------------

## 2. Teknik Analiz ve Metodoloji

-   **Hedef Mimari:** Embedded/bare-metal firmware ve Embedded Network
    Stack (ENS) kullanan mikrodenetleyici firmware'leri. Pemu tek bir
    MCU mimarisine özgü bir analiz sistemi olarak tasarlanmamış; mevcut
    firmware rehosting platformları SEmu, Fuzzware ve Hoedur üzerine
    entegre edilmiştir.
-   **Analiz Türü:** Dinamik analiz --- firmware rehosting +
    coverage-guided fuzzing + protocol-aware network fuzzing. Firmware
    fiziksel donanım yerine emülatör üzerinde çalıştırılarak network
    stack davranışı çalışma zamanında analiz edilmektedir.
-   **Tespit Edilen Tehdit Türü:** Embedded network stack içerisindeki
    yazılım hataları ve güvenlik açıkları. Özellikle network packet
    parsing, protocol state handling, memory corruption, out-of-bounds
    read/write, race condition ve ağ üzerinden tetiklenebilen derin
    yazılım hataları hedeflenmektedir.
-   **Kullanılan Ana Teknik / Algoritma:** Çalışmanın geliştirdiği
    sistem **Pemu**'dur. Pemu firmware'in kullandığı network protocol
    stack'i otomatik olarak çıkarır ve fuzzing girdilerini geçerli ağ
    paketleri içine yerleştirerek girdinin network stack'in daha
    üst/derin katmanlarına ulaşmasını sağlar.

Pemu'nun temel bileşenleri:

1.  **Protocol-Aware Packet Encapsulation:** Fuzzing girdisi, protocol
    grammar'ları kullanılarak semantik olarak geçerli network
    packet'larına dönüştürülür. IPv4, IPv6, TCP, UDP, Ethernet, IEEE
    802.15.4, 6LoWPAN gibi katmanlı protokollerde gerekli header,
    checksum, fragmentation ve state bilgileri korunur.
2.  **State Extraction:** Firmware'in dışarı gönderdiği packet'lar
    analiz edilerek network state'e ilişkin değerler çıkarılır ve
    sonraki fuzzing input'larının doğru biçimde encapsulate edilmesinde
    kullanılır.
3.  **Automatic Protocol Stack Deduction:** Pemu başlangıçta boş network
    configuration ile başlar. Protocol-specific probe'lar firmware'e
    gönderilir ve **code coverage feedback** kullanılarak hangi
    protocol'lerin desteklendiği dinamik biçimde belirlenir. Fuzzing
    ilerledikçe yapılandırma güncellenir.
4.  **Layer-by-Layer Fuzzing:** Encapsulation depth fuzzer tarafından
    değiştirilerek network stack'in farklı katmanları ayrı ayrı
    hedeflenebilir. Böylece yalnızca düşük seviyeli packet parsing değil
    application layer'a kadar ulaşan input'lar üretilebilir.
5.  **Rehosting Integration:** Pemu mevcut rehosting çözümleri olan
    **SEmu, Fuzzware ve Hoedur** ile entegre edilerek aynı firmware
    örneklerinin baseline ve Pemu-enabled fuzzing sonuçları
    karşılaştırılmıştır.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

-   **Veri Seti:** Çalışmanın evaluation set'i farklı embedded network
    stack ve protocol'lerini kullanan firmware örneklerinden
    oluşmaktadır. Örnekler arasında HTTP Server, UDP Server, TCP Echo
    Server/Client ve IEEE 802.15.4/6LoWPAN gibi farklı protocol
    stack'lerini kullanan firmware'ler bulunmaktadır. Pemu; SEmu,
    Fuzzware ve Hoedur tarafından desteklenen firmware örnekleri
    üzerinde baseline karşılaştırmalarıyla değerlendirilmiştir.
 **Veri Seti Erişilebilir mi?** ☐ Evet ☒ Hayır
  **Link:** Makalede bağımsız olarak yayımlanmış bir veri seti bağlantısı belirtilmemiştir.

 - **Kaynak Kod Açık mı?** ☒ Evet ☐ Hayır
    **GitHub:** https://github.com/MPI-SysSec/pemu

  - **Artifact Erişilebilir mi?** ☒ Evet ☐ Hayır
    **Artifact:** https://zenodo.org/records/17035985
    **DOI:** 10.5281/zenodo.17035985
    **Dil:** Python ağırlıklı (%93+), ayrıca Shell ve Dockerfile.
-   **Tekrarlanabilirlik Notu:** Repository'de SEmu, Fuzzware ve Hoedur
    için kurulum scriptleri ile coverage experiments, bug rediscovery ve
    industrial example deneylerini çalıştıran scriptler bulunmaktadır.
    `scripts/run_experiments.sh` tüm evaluation sürecini çalıştırmak
    için sağlanmıştır.

## 4. Proje Kriterleriyle Karşılaştırma

  ------------------------------------------------------------------------
  Kriter                  Var mı?                 Not
  ----------------------- ----------------------- ------------------------
  Diferansiyel Analiz (A  Hayır                   Pemu güvenilir firmware
  vs B imaj                                       A ile şüpheli firmware
  karşılaştırması)                                B'yi
                                                  karşılaştırmamaktadır.
                                                  Evaluation'da baseline
                                                  rehosting/fuzzing ile
                                                  Pemu-enabled fuzzing
                                                  sonuçları
                                                  karşılaştırılsa da bu
                                                  firmware image
                                                  differential analysis
                                                  değildir.

  Çok Katmanlı Analiz     Kısmen                  Protocol deduction,
  (birden fazla bağımsız                          packet encapsulation,
  yöntem)                                         state extraction,
                                                  code-coverage feedback,
                                                  firmware rehosting ve
                                                  fuzzing birlikte
                                                  kullanılmaktadır. Ancak
                                                  bunlar tek bir dinamik
                                                  network-fuzzing
                                                  pipeline'ının
                                                  bileşenleridir; hash,
                                                  entropy, YARA,
                                                  permission veya bağımsız
                                                  statik
                                                  firmware-forensics
                                                  katmanları
                                                  bulunmamaktadır.

  Delil Zinciri (Chain of Hayır                   Firmware'in adli delil
  Custody / kriptografik                          olarak acquisition'ı,
  doğrulama)                                      SHA-256 doğrulaması,
                                                  evidence ID,
                                                  examiner/action log veya
                                                  chain-of-custody
                                                  mekanizması ele
                                                  alınmamaktadır.

  Tek Bir Şüphe Skoru ile Hayır                   Birleşik risk/suspicion
  Özetleme                                        score bulunmamaktadır.
                                                  Başarım code coverage,
                                                  discovered bugs ve
                                                  fuzzing effectiveness
                                                  gibi metriklerle
                                                  ölçülmektedir.

  Tedarik Zinciri / İç    Hayır                   Çalışmanın tehdit modeli
  Tehdit Senaryosu                                firmware supply-chain
                                                  manipulation veya
                                                  insider threat değildir.
                                                  Odak network-exposed
                                                  firmware code
                                                  içerisindeki güvenlik
                                                  açıklarının fuzzing ile
                                                  keşfedilmesidir.
  ------------------------------------------------------------------------

## 5. Değerlendirme

-   **Bu makalenin projeme katkısı:** Bu çalışma projem için özellikle
    **firmware'in dinamik olarak doğrulanması ve statik analizle
    görülemeyen network-exposed davranışların ortaya çıkarılması**
    açısından yararlı bir referanstır. Pemu'nun temel katkısı,
    firmware'i yalnızca emüle etmek yerine network protocol semantics'i
    dikkate alarak fuzzing girdisinin daha derin firmware logic
    katmanlarına ulaşmasını sağlamasıdır.

    Bu yaklaşım, projemin mevcut statik/diferansiyel analiz hattının
    gelecekte dinamik bir doğrulama aşamasıyla genişletilmesi açısından
    değerlidir. Örneğin statik analizde şüpheli olduğu belirlenen bir
    network binary'si veya servis, Pemu benzeri protocol-aware
    rehosting/fuzzing yaklaşımıyla çalıştırılarak değişikliğin gerçekten
    network üzerinden exploitable bir davranış oluşturup oluşturmadığı
    araştırılabilir.

    Pemu'nun mevcut **SEmu, Fuzzware ve Hoedur** platformlarıyla entegre
    edilmesi de modüler mimari açısından yararlıdır. Projemde farklı
    analiz araçlarının tek pipeline altında birleştirilmesi fikrine
    benzer biçimde Pemu, mevcut rehosting araçlarını değiştirmek yerine
    onların network fuzzing yeteneğini genişleten bir katman olarak
    tasarlanmıştır.

    Ayrıca makalenin bulguları firmware analizinde yalnızca code
    presence veya statik değişikliklerin değil, değişikliğin runtime'da
    erişilebilirliğinin de önemli olduğunu göstermektedir. Pemu'nun daha
    geçerli network input'ları üretmesi sayesinde baseline fuzzing'in
    ulaşamadığı code path'lere erişebilmesi, gelecekte projemde statik
    şüphe skorunun dinamik doğrulama sonucu ile desteklenebileceğini
    göstermektedir.

-   **Eksik bıraktığı nokta (Gap):** Pemu doğrudan **firmware integrity
    veya firmware tampering detection sistemi değildir**. Güvenilir ve
    şüpheli firmware imajları arasında A-vs-B karşılaştırması yapmaz;
    SHA-256/hash integrity, filesystem diff, added/deleted/modified file
    detection, entropy analysis, YARA scanning, permission/ownership
    changes veya configuration comparison gibi projemin temel statik
    analiz katmanlarını içermez.

    Adli bilişim açısından da önemli bir boşluk vardır. Firmware'in
    nasıl elde edildiği, acquisition hash'i, delil bütünlüğünün analiz
    süresince korunması ve chain-of-custody kaydı ele alınmamaktadır.
    Ayrıca farklı analiz bulgularını tek bir suspicion score altında
    birleştiren bir mekanizma yoktur.

    Makalenin kendi teknik sınırlamalarından biri, Pemu'nun kullandığı
    protocol grammar'ların resmi specification'lardan **manuel olarak
    bir kez türetilmesidir**. Sistem firmware'in hangi protocol'leri
    kullandığını otomatik belirleyebilse de tamamen bilinmeyen/yeni bir
    protocol için grammar'ın önceden mevcut olması gerekir. Ayrıca
    low-level packet transmission ve özellikle karmaşık **DMA**
    mekanizmalarının modellenmesi mevcut rehosting sistemlerinin
    yeteneklerine bağlıdır.

    **Projemin bu makaleye göre temel farkı:** Pemu firmware'in network
    stack'ini dinamik olarak rehost edip protocol-aware fuzzing ile
    zafiyet keşfetmeye odaklanırken benim projem **güvenilir ve şüpheli
    firmware imajları arasında diferansiyel adli analiz**, çoklu statik
    analiz katmanları, kriptografik delil bütünlüğü ve birleşik firmware
    suspicion score yaklaşımını hedeflemektedir.

-   **Uygunluk Skoru (1--5):** 3

-   **Ek Notlar:** Pemu üç mevcut firmware rehosting platformuyla
    değerlendirilmiştir. Makalede Pemu'nun **Fuzzware baseline code
    coverage'ını ortalama %40,7**, Hoedur baseline'ını ise **%39,2**
    artırdığı raporlanmaktadır. Sistem daha önce bilinen çeşitli
    zafiyetleri yeniden keşfetmiş ve ayrıca **5 daha önce bilinmeyen
    software fault** tespit etmiştir. Bunlardan biri STM32F767 HAL
    içerisinde, geçerli TCP segmenti ve eşzamanlı ARP broadcast'in
    çakışmasıyla tetiklenen race-condition kaynaklı **out-of-bounds
    read** problemidir; vendor problemi doğrulamış ve security advisory
    yayımlamıştır. Çalışmanın artifact'ı hem GitHub hem Zenodo üzerinden
    açık olarak yayımlanmıştır.
