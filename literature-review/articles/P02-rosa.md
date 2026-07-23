# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

  -----------------------------------------------------------------------
  Alan                                Bilgi
  ----------------------------------- -----------------------------------
  Makale ID                           P02

  Başlık                              ROSA: Finding Backdoors with
                                      Fuzzing

  Yazarlar                            Dimitri Kokkonis, Michael Marcozzi,
                                      Emilien Decoux, Stefano Zacchiroli

  Yıl                                 2025

  Yayın Yeri (Venue)                  arXiv preprint, arXiv:2505.08544v1
                                      \[cs.CR\]

  DOI / Link                          arXiv:2505.08544

  Anahtar Kelimeler                   Fuzzing, dynamic analysis,
                                      metamorphic testing, backdoors,
                                      vulnerability detection, AFL++,
                                      software supply chain
  -----------------------------------------------------------------------

## 2. Teknik Analiz ve Metodoloji

-   **Hedef Mimari:** Linux üzerinde x86/x64 binary programlar. ROSA,
    AFL++'ın binary-only modunda QEMU backend kullanıyor. Mevcut
    implementasyon x86/x64 Linux binary'leriyle sınırlı.
-   **Analiz Türü:** Dinamik analiz --- graybox fuzzing + metamorphic
    testing. ROSA, AFL++ fuzzer'ını geliştirilen bir metamorphic test
    oracle ile birleştiriyor. Program çalıştırılırken CFG edge coverage
    ve system call davranışları takip ediliyor.
-   **Tespit Edilen Tehdit Türü:** Code-level backdoor'lar. Özellikle
    hard-coded credentials, gizli komutlar/anahtar girdiler,
    authentication bypass, root shell oluşturma, command execution,
    yetkisiz dosya sistemi erişimi ve privilege escalation gibi gizli
    davranışlar hedefleniyor. Gerçek örnekler arasında router firmware
    backdoor'ları ile PHP, ProFTPD ve vsFTPd gibi yazılımlardaki
    supply-chain kaynaklı backdoor'lar bulunuyor.
-   **Kullanılan Ana Teknik / Algoritma:** AFL++ graybox fuzzing +
    metamorphic test oracle + CFG edge coverage + system call
    karşılaştırması + Hamming distance.

ROSA iki ana fazdan oluşuyor:

**Phase 1 -- Representative Inputs Collection:** Program AFL++ ile fuzz
ediliyor ve farklı CFG edge kombinasyonlarını ortaya çıkaran girdilerden
bir representative input database oluşturuluyor.

**Phase 2 -- Backdoor Detection:** Yeni üretilen her fuzzing girdisi
için veritabanındaki CFG davranışı en yakın temsilci girdi bulunuyor.
Yakınlık, CFG edge vektörleri arasındaki Hamming distance ile
belirleniyor. Ardından iki girdinin oluşturduğu system call kümeleri
karşılaştırılıyor. Aynı input family içerisinde olduğu düşünülen iki
girdinin belirgin biçimde farklı sistem çağrıları oluşturması potansiyel
backdoor davranışı olarak raporlanıyor.

Son aşamada tekrar eden raporlar eleniyor ve kalan şüpheli davranışlar
`strace` benzeri araçlarla uzman tarafından doğrulanıyor.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

-   **Veri Seti:** ROSARUM benchmark --- toplam 17 backdoor. Bunların
    7'si authentic, 10'u synthetic backdoor'dur. Gerçek backdoor
    örnekleri arasında Belkin/httpd, D-Link/thttpd, Linksys/scfgmgr,
    Tenda/goahead, PHP, ProFTPD ve vsFTPd bulunuyor. Sentetik örnekler
    ise sudo, libpng, libsndfile, libtiff, libxml2, Lua, OpenSSL/bignum,
    PHP/unserialize, Poppler ve SQLite3 üzerinde oluşturulmuş.
-   **Veri Seti Erişilebilir mi?** Evet.
    Link: https://github.com/binsec/rosa
    ROSARUM açık olarak
    yayımlanmış. Her örnek için güvenli program kaynağı, backdoor
    patch'i ve ground-truth patch'i sağlanıyor. Makale ayrıca sonuçların
    yeniden üretilebilmesi için bir replication package yayımlandığını
    belirtiyor.
-   **Kaynak Kod Açık mı?** Evet.
    **GitHub:** https://github.com/binsec/rosa + https://github.com/binsec/rosarum
 ROSA ve ROSARUM GitHub üzerinde
    yayımlanmış ve ayrıca Software Heritage üzerinde arşivlenmiş.
    ROSA'nın implementasyonu AFL++ 4.20c ve QEMU üzerinde değişiklikler
    içeriyor.
    

## 4. Proje Kriterleriyle Karşılaştırma

  -----------------------------------------------------------------------
  Kriter                  Var mı?                 Not
  ----------------------- ----------------------- -----------------------
  Diferansiyel Analiz (A  Hayır                   Temiz/orijinal firmware
  vs B imaj                                       ile şüpheli firmware
  karşılaştırması)                                imajını doğrudan
                                                  karşılaştıran bir
                                                  A-vs-B yaklaşımı
                                                  kullanılmıyor. Bunun
                                                  yerine aynı program
                                                  üzerinde farklı
                                                  girdilerin oluşturduğu
                                                  runtime davranışları
                                                  karşılaştırılıyor.

  Çok Katmanlı Analiz     Kısmen                  CFG edge coverage,
  (birden fazla bağımsız                          fuzzing, metamorphic
  yöntem)                                         oracle ve system call
                                                  analizi birlikte
                                                  kullanılıyor. Ancak
                                                  bunlar ROSA'nın tek
                                                  dinamik backdoor
                                                  detection pipeline'ının
                                                  parçaları; hash,
                                                  entropi, YARA,
                                                  permission analysis
                                                  gibi bağımsız bütünlük
                                                  katmanları bulunmuyor.

  Delil Zinciri (Chain of Hayır                   Firmware'in adli delil
  Custody / kriptografik                          olarak elde edilmesi,
  doğrulama)                                      hash ile korunması veya
                                                  chain-of-custody kaydı
                                                  tutulması ele
                                                  alınmıyor.

  Tek Bir Şüphe Skoru ile Hayır                   0--100 benzeri birleşik
  Özetleme                                        risk/şüphe skoru
                                                  bulunmuyor. Sistem
                                                  şüpheli girdileri ve
                                                  farklılaşan system call
                                                  davranışlarını
                                                  raporluyor.

  Tedarik Zinciri / İç    Evet                    Software supply-chain
  Tehdit Senaryosu                                saldırıları çalışmanın
                                                  önemli
                                                  motivasyonlarından
                                                  biri. PHP, ProFTPD,
                                                  vsFTPd ve xz gibi
                                                  gerçek supply-chain
                                                  backdoor vakaları
                                                  tartışılıyor. Router
                                                  firmware'lerine
                                                  üretici/geliştirici
                                                  tarafından
                                                  yerleştirilebilecek
                                                  backdoor'lar da ele
                                                  alınıyor.
  -----------------------------------------------------------------------

## 5. Değerlendirme

-   **Bu makalenin projeme katkısı:** Bu makale projeme özellikle
    backdoor tespiti ve tedarik zinciri tehdidi açısından güçlü bir
    akademik dayanak sağlar. ROSA'nın en önemli katkısı, klasik imza
    tabanlı yöntemlerden farklı olarak bir backdoor'un çalıştırıldığında
    oluşturduğu anormal runtime davranışını tespit etmeye çalışmasıdır.
    Benim projem firmware bütünlüğünü hash, entropi, YARA ve izin/yetki
    analizi gibi statik katmanlardan değerlendirirken ROSA tamamen
    farklı bir bakış açısı sunmaktadır: firmware içerisindeki şüpheli
    kod gerçekten çalıştırıldığında sistem davranışının değişip
    değişmediğinin araştırılması. Özellikle makaledeki system call
    davranışlarının karşılaştırılması, ileride projeye dinamik analiz
    katmanı eklenmek istenirse değerlendirilebilecek güçlü bir
    yöntemdir. Ayrıca ROSA'nın gerçek router firmware backdoor'larını ve
    supply-chain kaynaklı backdoor'ları incelemesi, projenin tedarik
    zinciri / iç tehdit senaryosunu akademik olarak desteklemektedir.

-   **Eksik bıraktığı nokta (Gap):** ROSA, backdoor tespitinde güçlü bir
    dinamik analiz yöntemi sunmasına rağmen firmware bütünlüğünü
    bütüncül ve adli bilişim odaklı şekilde değerlendirmemektedir. Temiz
    firmware ile şüpheli firmware arasında doğrudan diferansiyel analiz
    gerçekleştirilmemekte; SHA-256/hash bütünlük kontrolü, entropi
    analizi, YARA tabanlı imza taraması ve izin/yetki değişiklikleri
    gibi statik analiz katmanları bulunmamaktadır. Ayrıca chain of
    custody, delil bütünlüğünün kriptografik olarak korunması ve
    birleşik şüphe skoru gibi adli bilişim mekanizmaları
    sunulmamaktadır. Bunun yanında ROSA'nın dinamik yapısı nedeniyle
    backdoor'un bulunabilmesi, AFL++'ın backdoor'u tetikleyecek girdiyi
    üretmesine bağlıdır. Makale de fuzzing'in büyük input space,
    karmaşık input formatları, yavaş execution ve hashing/cryptography
    gibi işlemler nedeniyle backdoor'u kaçırabileceğini belirtmektedir.
    Örneğin xz backdoor'unun kriptografik tetikleme mekanizması
    nedeniyle makul sürede fuzzing ile tetiklenemediği belirtilmiştir.
    Projemin bu makaleye göre farkı: ROSA tek bir dinamik backdoor
    detection yaklaşımına odaklanırken benim projem orijinal ve şüpheli
    firmware'in diferansiyel karşılaştırılması + çok katmanlı statik
    analiz + adli bilişim süreçleri + birleşik şüphe skoru yaklaşımını
    hedeflemektedir.

-   **Uygunluk Skoru (1--5):** 4

-   **Ek Notlar:** Deneylerde ROSA, ROSARUM üzerindeki 17 backdoor'un
    tamamını en az bir deney koşulunda tespit edebilmiş ve başarılı
    koşular genelinde ilk backdoor girdisinin bulunması ortalama
    yaklaşık 1 saat 30 dakika sürmüştür. 180 çalıştırmanın 156'sında
    (%87) backdoor bulunmuş; başarısız koşuların tamamı ROSA
    oracle'ından değil, AFL++'ın tetikleyici girdiyi üretememesinden
    kaynaklanmıştır. ROSA, statik analiz tabanlı STRINGER ile
    karşılaştırılmıştır. STRINGER yalnızca 4/17 backdoor'u tespit
    ederken ROSA tüm 17 backdoor'u kapsayabilmiştir. Buna karşılık
    STRINGER statik yapısı nedeniyle çok daha hızlıdır. ROSA'da uzman
    tarafından manuel olarak incelenmesi gereken şüpheli girdi sayısı
    ortalama 7 iken STRINGER'da ortalama 308 string incelenmesi
    gerektiği raporlanmıştır. Makale ayrıca gelecekte ROSA'nın statik
    analiz yöntemleriyle birleştirilmesinin fuzzing'in sınırlamalarını
    azaltabileceğini belirtmektedir.
