# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P05 |
| Başlık | MARS: The First Line of Defense for IoT Incident Response |
| Yazarlar | Karley M. Waguespack, Kaitlyn J. Smith, Olame A. Muliri, Ramyapandian Vijayakanthan, Aisha Ali-Gombe |
| Yıl | 2024 |
| Yayın Yeri (Venue) | Forensic Science International: Digital Investigation, Volume 49, 301754 — DFRWS USA 2024 Selected Papers |
| DOI / Link | 10.1016/j.fsidi.2024.301754 |
| Anahtar Kelimeler | IoT, incident response, host-based intrusion detection, anomaly detection, memory forensics, Trusted Execution Environment, ARM TrustZone, CNN, memory acquisition |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** Kaynakları kısıtlı IoT mikrodenetleyicileri. Proof-of-concept uygulama ARM TrustZone destekli STM32L562QEI6QU MCU üzerinde gerçekleştirilmiştir. STM32'nin ağ bağlantısı için ESP32 kullanılmıştır.
- **Analiz Türü:** Dinamik / çalışma zamanı tabanlı host-based intrusion detection (HIDS) ve anomaly detection. MARS, cihaz belleğindeki değişiklikleri çalışma sırasında izleyerek normal davranıştan sapmaları belirlemeye çalışır.
- **Tespit Edilen Tehdit Türü:** IoT cihazında malware enfeksiyonu ve çalışma zamanı anomalileri. Çalışma özellikle ICS/IoT ortamlarında Stuxnet benzeri saldırıları motivasyon senaryosu olarak kullanmaktadır. Sistem imza tabanlı belirli bir malware ailesini aramak yerine normal bellek davranışından sapmaları tespit etmeyi hedefler.
- **Kullanılan Ana Teknik/Algoritma:** MARS, Trusted Execution Environment (TEE) + bellek acquisition + hash tabanlı değişiklik tespiti + memory-to-audio transformation + CNN tabanlı anomaly classification yaklaşımını kullanmaktadır.

  MARS'ın mimarisi iki ana taraftan oluşmaktadır:

  1. **Client-side / IoT cihazı:** Memory acquisition bileşeni ARM TrustZone tarafından sağlanan TEE içerisinde çalışır. REE'deki firmware belleği bloklar halinde izlenir. Her bellek bloğunun hash'i önceki hash ile karşılaştırılır ve yalnızca değişen bloklar sunucuya gönderilir. Prototype uygulamasında 1024-byte bloklar ve MD5 kullanılmıştır. Watchdog timer, memory acquisition işleminin düzenli olarak gerçekleştirilmesini zorlar.
  2. **Server-side:** Değişen bellek blokları kullanılarak güncel memory dump yeniden oluşturulur. Bellek verisi ön işleme tabi tutulur ve anomaly detection modeline aktarılır.
  3. **Feature preprocessing:** Araştırmacılar n-gram tabanlı binary analiz ile memory-to-audio transformation yöntemlerini değerlendirmiş ve audio dönüşümünü tercih etmiştir. MFCC, Mel spectrogram ve chroma özellikleri çıkarılmaktadır.
  4. **Classification:** TensorFlow/Keras ile geliştirilen CNN modeli memory dump'ı benign veya anomalous olarak sınıflandırır.
  5. **Incident response:** Anomali tespit edilirse watchdog timer'ın resetlenmemesine izin verilerek cihaz resetlenebilir. Makale, kalıcı malware için gelecekte secure boot ile temiz firmware'in yeniden yüklenmesini önermektedir.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Çalışmanın doğruluk değerlendirmesinde toplam 40 memory image kullanılmıştır. Bunların 20'si Infrared Motion-Sensing uygulamasından normal/benign, diğer 20'si Blinking LED uygulamasından anomalous olarak oluşturulmuştur. Veri 70:30 training/testing oranıyla bölünmüştür. Robustness testi için ayrıca memory image'larda %0.1, %0.2, %0.5 ve %1.0 oranlarında rastgele bit-flip değişiklikleri oluşturulmuştur.
- **Veri Seti Erişilebilir mi?** Hayır — makalede bu 40 memory image'dan oluşan deney veri seti için açık bir dataset repository veya indirme bağlantısı belirtilmemektedir.
- **Kaynak Kod Açık mı?** Hayır — makalede MARS prototype'ının kaynak kodu için doğrulanabilir bir GitHub repository bağlantısı belirtilmemektedir. Açık web aramasında da makaleyle güvenilir biçimde eşleştirilebilen resmi bir MARS kod deposu doğrulanamamıştır. Uygulama detayı: Client-side memory acquisition yaklaşık 3000 satır C, server-side bileşen yaklaşık 200 satır Python olarak geliştirilmiştir. CNN modeli TensorFlow Keras API kullanmaktadır.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Kısmen | MARS iki ayrı firmware imajını A-vs-B biçiminde karşılaştırmaz. Ancak runtime belleği bloklara ayırır, her bloğun mevcut hash'ini önceki hash ile karşılaştırır ve yalnızca değişen blokları belirler. Bu nedenle zaman-temelli bellek diferansiyel analizi vardır. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Hash tabanlı memory-change detection, TEE tabanlı güvenli acquisition, memory-to-audio preprocessing, MFCC/Mel/chroma feature extraction ve CNN anomaly classification birlikte kullanılmaktadır. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Kısmen | Klasik adli chain-of-custody mekanizması sunulmamaktadır. Bununla birlikte memory acquisition'ın TEE içerisinde gerçekleştirilmesi, REE'den izole edilmesi ve aktarılan memory dump bütünlüğünün doğrulanması güvenilir veri toplama açısından adli bilişimle güçlü biçimde ilişkilidir. |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | Sistem birleşik 0–100 benzeri bir şüphe skoru üretmez. CNN çıktısı binary classification şeklindedir: `1 = normal`, `0 = potentially anomalous`. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Çalışmanın ana tehdit modeli runtime malware intrusion'dır. Firmware supply-chain veya kötü niyetli insider senaryosu doğrudan incelenmemektedir. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** MARS, projem açısından özellikle bellek bütünlüğü, hash tabanlı değişiklik tespiti, güvenilir veri toplama ve IoT incident response konularında güçlü bir referanstır. Projem firmware imajlarını statik ve diferansiyel olarak analiz ederken MARS cihaz çalışırken bellekte meydana gelen değişiklikleri izlemektedir. Bu nedenle iki çalışma farklı analiz zamanlarında çalışsa da temel fikir açısından önemli bir ortaklık vardır: normal/baseline durum ile sonraki durum arasındaki değişikliklerin tespit edilmesi.

  Özellikle MARS'ın her memory block için hash hesaplayıp bunu önceki hash ile karşılaştırması, projemdeki bütünlük ve diferansiyel analiz yaklaşımıyla doğrudan ilişkilidir. MARS ayrıca tüm belleği sürekli göndermek yerine yalnızca hash'i değişen blokları analiz ederek büyük verilerde işlem yükünü azaltmaktadır. Bu yaklaşım ileride projemin performans optimizasyonunda değerlendirilebilir.

  Makalenin ikinci önemli katkısı Trusted Execution Environment kullanımıdır. Memory acquisition bileşeninin ARM TrustZone içerisinde tutulması, malware cihazın normal çalışma ortamını ele geçirse bile IDS bileşeninin manipüle edilmesini zorlaştırmaktadır. Bu yaklaşım, projemdeki chain-of-custody ve analiz edilen verinin güvenilirliği tartışılırken donanımsal güven kökü açısından yararlı bir akademik referans sağlar.

  MARS ayrıca incident response perspektifini doğrudan ele almaktadır. Anomali tespit edildiğinde cihazın watchdog üzerinden resetlenebilmesi ve gelecekte secure boot ile temiz firmware'in yeniden yüklenmesinin önerilmesi, firmware analizinden incident response aşamasına geçiş için yararlı bir yaklaşım sunmaktadır.
- **Eksik bıraktığı nokta (Gap):** MARS'ın temel amacı firmware dosyasının kendisini adli olarak analiz etmek değil, çalışan IoT cihazının belleğinde oluşan anomalileri tespit etmektir. Bu nedenle temiz/orijinal firmware ile şüpheli firmware arasında dosya sistemi seviyesinde A-vs-B karşılaştırması, eklenen/silinen/değiştirilen dosyaların tespiti, firmware entropi analizi, YARA taraması, izin/yetki değişiklikleri ve firmware içerisindeki şüpheli bileşenlerin statik analizi bulunmamaktadır.

  Ayrıca sistem klasik anlamda chain of custody kaydı, zaman damgalı adli işlem günlüğü veya bütün analiz sonuçlarını tek bir şüphe skorunda birleştiren bir mekanizma sunmamaktadır. TEE, acquisition bütünlüğünü güçlendirse de tek başına tam bir adli delil zinciri değildir.

  Makalenin kendi belirttiği önemli sınırlamalardan biri de değerlendirmede gerçek malware kullanılmamış olmasıdır. Sistem iki basit IoT uygulamasından alınan toplam 40 memory image ile test edilmiş, robustness değerlendirmesinde ise yapay bit-flip değişiklikleri kullanılmıştır. Araştırmacılar gelecekte gerçek malware saldırıları, daha karmaşık IoT uygulamaları, secure boot ve SRAM acquisition ile değerlendirme yapılması gerektiğini belirtmektedir.

  **Projemin bu makaleye göre temel farkı:** MARS çalışma zamanındaki memory anomaly'lerini TEE + CNN ile tespit eden bir HIDS iken benim projem orijinal ve şüpheli firmware imajlarını doğrudan karşılaştıran, çok katmanlı statik/diferansiyel firmware analizi gerçekleştiren, adli bütünlük ve birleşik şüphe skoru hedefleyen bir firmware forensics yaklaşımıdır.
- **Uygunluk Skoru (1–5):** 5
- **Ek Notlar:** MARS'ın proof-of-concept değerlendirmesinde CNN sınıflandırıcısı 40 memory image üzerinde %100 test accuracy, F1-score 1.0, recall 1.0 ve precision 1.0 raporlamıştır. Ancak veri setinin küçük olması ve gerçek malware içermemesi nedeniyle bu sonuç genelleştirilirken dikkatli olunmalıdır. Stress testing sonucunda sistem, bellekteki byte'ların %1.0'ı değiştirildiğinde tüm test örneklerini anomalous olarak sınıflandırmıştır; daha küçük değişikliklerde sonuçlar tutarsızdır. Bir tam 256 KB memory dump'ın DMA ile acquisition/buffering süresi yaklaşık 500 ms, ağ üzerinden sunucuya gönderilmesi ise kullanılan ESP32 Wi-Fi bağlantısı nedeniyle yaklaşık 5 dakika sürmüştür. Tek bir değiştirilmiş memory block'un tespit, acquisition ve transfer süreci yaklaşık 8 saniye olarak raporlanmıştır. Makalenin mimari diyagramı, TEE içerisinde memory acquisition ve network bileşenlerinin; REE içerisinde IoT process'in; harici classification server üzerinde ise anomaly detection'ın konumlandırıldığını göstermektedir.
