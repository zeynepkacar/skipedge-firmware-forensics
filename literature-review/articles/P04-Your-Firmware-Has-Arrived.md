# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

  --------------------------------------------------------------------------------------------------------------
  Alan                                Bilgi
  ----------------------------------- --------------------------------------------------------------------------
  Makale ID                           P04

  Başlık                              Your Firmware Has Arrived: A Study of Firmware Update Vulnerabilities

  Yazarlar                            Yuhao Wu, Jinwen Wang, Yujie Wang, Shixuan Zhai, Zihan Li, Yi He, Kun Sun,
                                      Qi Li, Ning Zhang

  Yıl                                 2024

  Yayın Yeri (Venue)                  33rd USENIX Security Symposium (USENIX Security 24)

  DOI / Link                          USENIX Security 2024 ---
                                      https://www.usenix.org/conference/usenixsecurity24/presentation/wu-yuhao

  Anahtar Kelimeler                   Firmware update security, embedded firmware, ChkUp, firmware verification,
                                      authenticity, integrity, freshness, compatibility, program slicing,
                                      control flow analysis, vulnerability detection
  --------------------------------------------------------------------------------------------------------------

## 2. Teknik Analiz ve Metodoloji

-   **Hedef Mimari:** Dosya sistemi içeren OS-tabanlı firmware'ler;
    özellikle Linux tabanlı embedded firmware. ChkUp prototipi ARM, MIPS
    ve PowerPC dahil birden fazla mimariyi desteklemektedir.

-   **Analiz Türü:** Hibrit --- temel zafiyet keşfi statik binary
    analizine dayanır; tespit edilen alarmların doğrulanmasında yarı
    otomatik dinamik analiz, firmware emülasyonu, patching ve PoC
    üretimi kullanılır. Kaynak koda erişim gerektirmeyen binary-based
    bir yaklaşımdır.

-   **Tespit Edilen Tehdit Türü:** Firmware update mekanizmalarındaki
    eksik veya hatalı doğrulamalar. Dört temel güvenlik özelliği
    incelenir: **authenticity, integrity, freshness ve compatibility**.
    Sistem; imza doğrulamasının eksikliği, zayıf bütünlük algoritmaları
    (CRC, SHA-1, MD5), güvenli olmayan freshness/version kontrolü ve
    compatibility/device-ID doğrulama problemlerini tespit etmeyi
    hedefler. Bu zafiyetler değiştirilmiş firmware yükleme, firmware
    downgrade ve uyumsuz firmware yükleme gibi saldırılara yol açabilir.

-   **Kullanılan Ana Teknik/Algoritma:** ChkUp dört ana modülden oluşur:

    1.  **Execution Path Recovery:** Firmware update giriş noktası
        belirlenir ve farklı programlama dillerindeki programların
        kontrol akışlarını birleştiren **Update Flow Graph (UFG)**
        oluşturulur. HTML/JavaScript, shell script ve binary bileşenleri
        ile IPC ve program invocation ilişkileri birlikte analiz edilir.
        Firmware update execution path'leri, reboot noktasından geriye
        doğru **function-level backward program slicing** ile çıkarılır.
    2.  **Verification Procedure Recognition:** Firmware doğrulama
        fonksiyonları önce syntactic ve structural özelliklere göre
        benzerlik skoru ile sıralanır. Ardından daha hassas semantik
        eşleştirme için **Data Flow Graph (DFG) subgraph isomorphism**
        uygulanır. Ullmann algoritması kullanılarak authenticity,
        integrity, freshness ve compatibility doğrulama zincirleri
        belirlenir.
    3.  **Vulnerability Discovery:** Çıkarılan execution path üzerindeki
        doğrulama prosedürlerinin eksik veya hatalı olup olmadığı
        belirlenen güvenlik kriterlerine göre incelenir.
    4.  **Vulnerability Validation:** Alarmlar firmware emülasyonu ve
        PoC ile dinamik olarak doğrulanır. Gerekli durumlarda
        verification dependency'leri firmware patching ile bypass edilir
        ve değiştirilmiş firmware'in update sürecinde reboot aşamasına
        ulaşıp ulaşmadığı gözlemlenir.

-   **Kullanılan Araçlar:** angr, NetworkX, Ghidra, Firmadyne, FirmAE ve
    Firmware-mod-kit. Firmware koleksiyonunun unpack edilmesinde Binwalk
    kullanılmıştır.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

-   **Veri Seti:** Araştırmacılar IoT üreticilerinin web sitelerinden
    toplam **157.141 firmware imajı** toplamış ve bunların **111.958'ini
    başarıyla unpack** etmiştir. Büyük ölçekli analiz için bu
    koleksiyondan sekiz büyük üreticiye ait **12.000 firmware imajı**
    rastgele seçilerek **DL** veri seti oluşturulmuştur. Üreticiler:
    Netgear, TP-Link, D-Link, TRENDnet, Asus, Ubiquiti, Zyxel ve
    Linksys. Ayrıca DL içerisinden 33 farklı cihaz ailesini kapsayan
    **150 firmware imajı** seçilerek dört güvenlik uzmanının manuel
    analiziyle **DG ground-truth dataset** oluşturulmuştur.
-   **Veri Seti Erişilebilir mi?** Evet --- araştırmacıların firmware
    koleksiyonu için açık bir repository bulunmaktadır. Repository,
    firmware download listelerini ve firmware'leri indirme/unpack etme
    yardımcı scriptlerini sunmaktadır.
-   **Veri Seti / Firmware Dataset Linki:**
    https://github.com/WUSTL-CSPL/Firmware-Dataset
-   **Artifact / Proje Sayfası:** https://fw-chkup.github.io
-   **Kaynak Kod Açık mı?** Evet.
-   **GitHub / Kaynak Kod Linki:** https://github.com/WUSTL-CSPL/ChkUp

## 4. Proje Kriterleriyle Karşılaştırma

  -----------------------------------------------------------------------
  Kriter                  Var mı?                 Not
  ----------------------- ----------------------- -----------------------
  Diferansiyel Analiz (A  Kısmen                  ChkUp temiz bir A
  vs B imaj                                       firmware'i ile şüpheli
  karşılaştırması)                                bir B firmware'ini
                                                  sistematik olarak
                                                  dosya/hash seviyesinde
                                                  karşılaştırmaz. Ancak
                                                  vulnerability
                                                  validation aşamasında
                                                  benign firmware ile
                                                  değiştirilmiş, eski
                                                  veya uyumsuz firmware
                                                  örnekleri kullanılarak
                                                  davranışsal doğrulama
                                                  yapılır. Bu nedenle
                                                  sınırlı ve amaç-odaklı
                                                  bir karşılaştırma
                                                  vardır.

  Çok Katmanlı Analiz     Evet                    Cross-language
  (birden fazla bağımsız                          control-flow analysis,
  yöntem)                                         UFG, backward slicing,
                                                  syntactic/structural
                                                  function similarity,
                                                  DFG isomorphism, static
                                                  vulnerability
                                                  discovery, firmware
                                                  patching, emülasyon ve
                                                  PoC tabanlı dinamik
                                                  doğrulama birlikte
                                                  kullanılmaktadır.

  Delil Zinciri (Chain of Hayır                   Firmware'in adli delil
  Custody / kriptografik                          olarak edinilmesi,
  doğrulama)                                      hash'lenmesi, zaman
                                                  damgası, delil zinciri
                                                  veya inceleme sürecinin
                                                  adli bütünlüğünün
                                                  korunması ele
                                                  alınmamaktadır.

  Tek Bir Şüphe Skoru ile Hayır                   ChkUp tek bir birleşik
  Özetleme                                        risk/şüphe skoru
                                                  üretmez. Sistem
                                                  authenticity,
                                                  integrity, freshness ve
                                                  compatibility
                                                  kategorilerindeki
                                                  eksik/hatalı
                                                  doğrulamalar için ayrı
                                                  alarmlar üretir.

  Tedarik Zinciri / İç    Evet                    Makale firmware
  Tehdit Senaryosu Ele                            generation aşamasında
  Alınmış mı                                      supply-chain
                                                  saldırılarını doğrudan
                                                  tehdit olarak ele alır.
                                                  Yazılım geliştirme
                                                  araçlarının veya
                                                  altyapının ele
                                                  geçirilmesi ve kötü
                                                  niyetli firmware
                                                  update'lerinin tedarik
                                                  zinciri üzerinden
                                                  dağıtılması tartışılır.
                                                  SolarWinds olayı örnek
                                                  olarak verilir. Ancak
                                                  özel olarak kötü
                                                  niyetli çalışan/insider
                                                  threat tespiti
                                                  geliştirilmemiştir.
  -----------------------------------------------------------------------

## 5. Değerlendirme

-   **Bu makalenin projeme katkısı:** Bu çalışma projem açısından en
    güçlü referanslardan biridir çünkü doğrudan **firmware bütünlüğü,
    değiştirilmiş firmware, firmware update güvenliği ve tedarik zinciri
    riski** ile ilişkilidir. ChkUp'ın authenticity ve integrity
    verification kontrollerini incelemesi, projemdeki firmware bütünlüğü
    değerlendirmesiyle doğrudan kesişmektedir. Özellikle MD5, SHA-1 ve
    CRC gibi zayıf bütünlük mekanizmalarının tespit edilmesi, yalnızca
    bir hash değerinin mevcut olup olmadığını değil, kullanılan bütünlük
    doğrulama mekanizmasının güvenli olup olmadığını değerlendirmenin
    önemini göstermektedir.

    Makalenin firmware update sürecini **generation → delivery →
    verification → installation** şeklinde dört aşamaya ayırması,
    projenin tedarik zinciri senaryosunun modellenmesinde
    kullanılabilecek güçlü bir kavramsal çerçevedir. Özellikle
    generation aşamasında firmware'in supply chain üzerinden dağıtılması
    ve verification aşamasındaki eksikliklerin değiştirilmiş firmware'in
    cihaza yüklenmesine izin verebilmesi, projemde ele alınan firmware
    manipülasyonu senaryosunu akademik olarak desteklemektedir.

    ChkUp'ın yalnızca statik alarm üretmekle kalmayıp firmware patching,
    emülasyon ve PoC ile bazı bulguları dinamik olarak doğrulaması da
    çok katmanlı analiz açısından değerlidir. Projem ileride dinamik
    analiz katmanıyla genişletilecekse bu yaklaşım güçlü bir metodolojik
    referans olabilir.

-   **Eksik bıraktığı nokta (Gap):** ChkUp'ın temel amacı firmware
    update mekanizmasındaki güvenlik kontrollerinin doğru uygulanıp
    uygulanmadığını tespit etmektir; doğrudan **iki firmware imajı
    arasındaki tüm değişiklikleri adli olarak karşılaştıran bir
    differential firmware forensics sistemi değildir**. A ve B firmware
    imajlarının SHA-256 değerlerinin karşılaştırılması, filesystem
    içerisindeki eklenen/silinen/değiştirilen dosyaların sistematik
    olarak çıkarılması, entropi farklarının incelenmesi, YARA tabanlı
    zararlı imza taraması veya izin/yetki değişikliklerinin
    karşılaştırılması ChkUp'ın kapsamı dışındadır.

    Ayrıca chain of custody, incelemeye alınan firmware'in kriptografik
    delil bütünlüğünün korunması ve tüm analiz sonuçlarının tek bir
    birleşik şüphe skorunda özetlenmesi gibi adli bilişim özellikleri
    bulunmamaktadır.

    Teknik olarak ChkUp'ın da sınırlamaları vardır. DG'deki 150
    firmware'in yalnızca 72'si mevcut firmware emulator'larıyla emüle
    edilebilmiştir. Execution path recovery; yanlış entry program
    seçimi, timeout, alışılmadık IPC mekanizmaları veya desteklenmeyen
    programlama dilleri nedeniyle başarısız olabilmektedir. Dynamic
    validation ise firmware'in başarılı biçimde repack ve emulate
    edilebilmesine bağlıdır.

    **Projemin bu makaleye göre temel farkı:** ChkUp firmware update
    prosedürünün güvenliğini ve verification logic'ini analiz ederken,
    benim projem **orijinal ve şüpheli firmware arasında diferansiyel
    karşılaştırma + çok katmanlı statik analiz + firmware
    manipülasyonunun tespiti + adli delil bütünlüğü + birleşik şüphe
    skoru** yaklaşımını hedeflemektedir.

-   **Uygunluk Skoru (1--5):** 5

-   **Ek Notlar:** ChkUp, DL veri setindeki 12.000 firmware üzerinde
    çalıştırılmış ve **10.670 firmware için update execution path**
    çözümleyebilmiştir. Toplam **15.132 alarm** üretmiştir. 150
    firmware'lik DG ground-truth veri setinde yapılan doğrulamada
    **%86,7 true positive rate (TPR)** ve **%5,3 false positive rate
    (FPR)** raporlanmıştır. Çalışma sonucunda hem zero-day hem n-day
    firmware update zafiyetleri keşfedilmiş; sorumlu açıklama sonucunda
    **25 CVE ID ve 1 PSV ID** atanmıştır. Araştırmacılar ayrıca firmware
    downgrade ve firmware modification saldırılarıyla bulunan
    zafiyetlerin pratik olarak sömürülebilirliğini göstermiştir.
