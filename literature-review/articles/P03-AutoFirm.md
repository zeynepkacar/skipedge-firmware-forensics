# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P03 |
| Başlık | AutoFirm: Automatically Identifying Reused Libraries inside IoT Firmware at Large-Scale |
| Yazarlar | YongLe Chen, Feng Ma, Ying Zhang, YongZhong He, Haining Wang, Qiang Li |
| Yıl | 2024 |
| Yayın Yeri (Venue) | arXiv preprint, arXiv:2406.12947v1 [cs.CR]. PDF üzerinde "Anonymous Submission to ACM XXX 2024" ifadesi de bulunmaktadır; kesin ACM venue adı belirtilmemiştir. |
| DOI / Link | arXiv:2406.12947v1 |
| Anahtar Kelimeler | IoT firmware, reused software libraries, vulnerable libraries, firmware analysis, library identification, version detection, CVE, NVD, CPE, Binwalk, QEMU, vulnerability analysis |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** IoT cihaz firmware'leri. Çalışma; router, switch, kamera ve benzeri IoT cihazlarının firmware imajlarında bulunan yeniden kullanılmış açık kaynak yazılım kütüphanelerini incelemektedir.
- **Analiz Türü:** Büyük ölçekli otomatik firmware analizi; ağırlıklı olarak statik firmware/filesystem analizi, kütüphane ve sürüm tespiti ve bilinen zafiyetlerle eşleştirme. QEMU, bazı kütüphanelerden sürüm bilgisinin elde edilmesinde emülasyon amacıyla da kullanılmaktadır.
- **Tespit Edilen Tehdit Türü:** Firmware içerisinde kullanılan eski ve/veya bilinen güvenlik açıklarına sahip yeniden kullanılmış yazılım kütüphaneleri. Çalışma bu kütüphanelerin CVE/CWE/CVSS bilgileri üzerinden IoT cihazlarına oluşturduğu güvenlik riskini araştırmaktadır.
- **Kullanılan Ana Teknik/Algoritma:** AutoFirm üç ana bileşenden oluşmaktadır:
  1. **IoT Firmware Collection:** Üretici web sitelerinden Scrapy tabanlı crawler ile firmware imajlarının ve cihaz meta verilerinin otomatik toplanması. Dinamik web sayfaları için BrowserMob Proxy kullanılmaktadır.
  2. **Library Identification:** Firmware imajının Binwalk ile filesystem'e çıkarılması, filesystem içerisindeki aday yazılım kütüphanelerinin belirlenmesi ve kütüphane başlıklarındaki syntax/string bilgilerinin incelenmesi.
  3. **Vulnerable Library Detection:** Kütüphane adı ve sürümünün belirlenmesi; String/QEMU ve regex tabanlı sürüm çıkarımı; ardından `(library name, version)` bilgisinin NVD'deki CPE/CVE bilgileriyle eşleştirilmesi.

  Sistemin temel çıktısı `(lib, version, CVE)` üçlüsüdür.

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** Araştırmacılar 37 farklı IoT üreticisinin web sitelerinden 6.901 IoT firmware imajı toplamıştır. Çalışmada 349 açık kaynak yazılım kütüphanesi, 11.342 zafiyetli sürüm ve bunlarla ilişkili 2.729 farklı CVE analiz edilmiştir. Zafiyet verileri NVD ile birleştirilmiştir.
- **Veri Seti Erişilebilir mi?** Evet (Link: https://github.com/sure17/AutoFirm — artifact klasörü) — Makale "Artifact available: vulnerable libraries in IoT firmware" şeklinde bir araştırma artefaktı belirtmektedir. Firmware imajlarının tamamının tek bir bağımsız açık veri seti olarak sunulduğu ise metinden kesin biçimde söylenemez; firmware'lerin önemli bölümü üretici kaynaklarından toplanmıştır.
- **Kaynak Kod Açık mı?** Evet (Link: https://github.com/sure17/AutoFirm) — Dil: Python. Kullanılan başlıca teknolojiler: Scrapy, BrowserMob Proxy, Binwalk, String, QEMU, regex ve NVD/CPE eşleştirmesi.

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Kısmen | Makalenin temel amacı iki firmware imajını adli olarak byte/dosya bazında karşılaştırmak değildir. Ancak firmware sürümleri ve kullanılan kütüphane sürümleri zaman içerisinde karşılaştırılarak üreticinin eski/zafiyetli kütüphaneyi güncelleyip güncellemediği incelenmektedir. Bu nedenle sınırlı bir sürüm-temelli karşılaştırma vardır. |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Evet | Firmware toplama, filesystem extraction, library identification, version extraction ve NVD/CPE/CVE eşleştirmesi gibi birden fazla aşama birlikte kullanılmaktadır. |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Çalışmanın amacı adli delil bütünlüğü veya chain-of-custody sağlamak değildir. Crawler aşamasında duplicate firmware'leri ayıklamak için firmware metadata checksum kullanılsa da bu, adli delil zinciri mekanizması olarak sunulmamaktadır. |
| Tek Bir Şüphe Skoru ile Özetleme | Hayır | AutoFirm tek bir birleşik "şüphe skoru" üretmez. CVE, CVSS, CWE, library version ve yaygınlık gibi bilgiler ayrı ayrı değerlendirilir. |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Kısmen | Yeniden kullanılan üçüncü taraf/açık kaynak kütüphanelerin firmware'e taşıdığı güvenlik riski yazılım tedarik zinciri açısından doğrudan ilişkilidir. Ancak çalışma kasıtlı iç tehdit, firmware manipülasyonu veya kötü niyetli çalışan senaryosunu analiz etmemektedir. |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** AutoFirm, projem açısından özellikle firmware'in otomatik olarak açılması, filesystem yapısının incelenmesi ve firmware içerisindeki yazılım bileşenlerinin/kütüphanelerin belirlenmesi bakımından güçlü bir referanstır. Makalede Binwalk kullanılarak firmware imajlarının filesystem'e dönüştürülmesi ve buradan kütüphane bilgilerinin çıkarılması, firmware analiz hattının otomatikleştirilebileceğini göstermektedir.

  İkinci önemli katkı, yalnızca dosya veya kütüphane varlığını belirlemek yerine kütüphane adı + sürüm + CVE ilişkisinin kurulmasıdır. Bu yaklaşım, projede tespit edilen değişikliklerin güvenlik bağlamında anlamlandırılması için kullanılabilecek iyi bir örnektir. Bir firmware içerisindeki bileşenin yalnızca "değişmiş" olduğunu söylemek yerine, bu bileşenin sürümünün eski veya bilinen bir zafiyetle ilişkili olup olmadığı da değerlendirilebilir.

  Çalışmanın büyük ölçekli otomasyon yaklaşımı da önemlidir. AutoFirm'in web crawler → firmware extraction → library identification → version detection → vulnerability matching biçimindeki pipeline yapısı, firmware analizi için modüler bir mimari örneği sunmaktadır.

  Makalenin sonuçları firmware içerisindeki eski bileşenlerin güvenlik açısından neden önemli olduğunu da güçlü biçimde göstermektedir: incelenen durumların yalnızca %32,7'sinde üreticilerin zafiyetli kütüphaneyi daha yeni bir sürüme güncellediği, %67,3'ünde ise eski/zafiyetli sürümün firmware'de kalmaya devam ettiği raporlanmıştır. Güncelleme yapılan durumlarda ortalama sürenin yaklaşık 1,34 yıl olduğu belirtilmektedir.
- **Eksik bıraktığı nokta (Gap):** AutoFirm'in temel hedefi firmware manipülasyonunu veya iki firmware imajı arasındaki şüpheli değişiklikleri adli olarak tespit etmek değildir. Sistem esas olarak firmware içerisinde hangi kütüphanenin ve hangi sürümün kullanıldığını belirleyerek bunu bilinen CVE verileriyle eşleştirmektedir.

  Bu nedenle projedeki A ve B firmware imajlarının sistematik diferansiyel karşılaştırılması, dosya ekleme/silme/değiştirme tespiti, değişikliklerin birden fazla bağımsız analiz yöntemiyle doğrulanması, bulguların tek bir şüphe skorunda birleştirilmesi ve adli chain of custody mekanizmasının oluşturulması AutoFirm tarafından ele alınmamaktadır.

  Makalenin kendi belirttiği teknik sınırlamalar da önemlidir. Bazı üreticiler firmware indirme bağlantısı sağlamamaktadır; proprietary veya alışılmadık firmware/filesystem formatları Binwalk ile çıkarılamayabilir; ayrıca AutoFirm sürüm bilgisine dayandığı için binary içerisinde sürüm bilgisi bulunmadığında vulnerable-library detection başarımı sınırlanmaktadır.

  Dolayısıyla AutoFirm'den alınabilecek güçlü taraf otomatik firmware extraction + bileşen/kütüphane envanteri + sürüm/CVE korelasyonu iken, projenin özgünleşebileceği alan diferansiyel adli analiz + çoklu doğrulama + delil bütünlüğü + birleşik şüphe skoru + olası tedarik zinciri manipülasyonunun yorumlanmasıdır.
- **Uygunluk Skoru (1–5):** 5
- **Ek Notlar:** AutoFirm toplam 6.901 firmware imajını incelemektedir. Firmware'ler 37 farklı IoT üreticisinden toplanmıştır. 349 açık kaynak yazılım kütüphanesi değerlendirilmiştir. 11.342 zafiyetli sürüm ve 2.729 farklı CVE raporlanmıştır. Firmware extraction aşamasında Binwalk kullanılmaktadır. Sürüm çıkarımında String, QEMU ve regex yaklaşımı kullanılmaktadır. Zafiyet eşleştirmesinde NVD, CPE ve CVE verileri kullanılmaktadır. Üreticilerin eski/zafiyetli kütüphaneleri güncellemediği durumların oranı %67,3 olarak bulunmuştur. Güncelleme yapılan durumlarda ortalama güncelleme süresi yaklaşık 1,34 yıl olarak raporlanmıştır. Makale, bazı zafiyetlerin firmware'de yıllarca kalabildiğini ve bunun IoT cihazlarında geniş bir saldırı yüzeyi oluşturduğunu göstermektedir.
