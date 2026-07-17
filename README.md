# skipedge-firmware-forensics
# Gömülü Sistem Firmware'lerinde Çok Katmanlı Bütünlük İhlali Tespiti ve Adli Bilişim Analizi

*Multi-Layer Firmware Integrity Violation Detection and Digital Forensics Analysis for Embedded Systems*

Bu proje, Spikedge bünyesinde yürütülen yaz stajı kapsamında geliştirilmektedir.

## Proje Hakkında

- **Öğrenci:** Zeynep
- **Bölüm:** Adli Bilişim Mühendisliği (3. sınıf → 4. sınıf)
- **Şirket:** Spikedge
- **Staj türü:** Uzaktan, 20 iş günü

## Amaç

Spikedge gibi firmaların geliştirdiği gömülü/endüstriyel cihazlar, secure boot ve OTA (over-the-air) güncelleme mekanizmalarıyla korunur. Ancak bir firmware güncellemesi tedarik zinciri saldırısı, yetkisiz müdahale veya iç tehdit yoluyla manipüle edilirse (arka kapı eklenmesi, izin değişikliği, kod enjeksiyonu), bu ihlalin ne zaman, nasıl ve hangi kanıtlarla tespit edilebileceği kritik bir sorudur.

Bu projenin amacı; iki firmware imajı (orijinal ve şüpheli/güncellenmiş) arasındaki bütünlük ihlallerini birden fazla bağımsız analiz katmanına dayanarak tespit eden, bulgularını delil zinciriyle (chain of custody) belgeleyen ve sonucu tek bir şüphe skoru ile özetleyen çok katmanlı bir dijital adli bilişim analiz sistemi geliştirmektir.

## Kapsam

- Açık kaynak firmware imajları (ör. OpenWrt, Yocto örnek build'leri) ve bilinen CVE örnekleri üzerinde statik analiz
- Çok katmanlı analiz motoru (bkz. aşağıda)
- Delil zinciri (chain of custody) ile bulgu bütünlüğünün korunması
- Bilinen CVE örnekleriyle yöntemin değerlendirilmesi
- Web tabanlı bir arayüz üzerinden görselleştirme ve raporlama

## Analiz Katmanları

| Katman | İşlevi |
|---|---|
| 1. Statik Bütünlük | Dosya/blok seviyesinde SHA-256 hash karşılaştırma; eklenen, silinen, değiştirilen dosyaların tespiti |
| 2. Entropi Analizi | Firmware bölümlerinin entropi değerleri hesaplanarak gizlenmiş/şifrelenmiş kötü amaçlı kodun tespiti |
| 3. İmza / Pattern Tarama | YARA kuralları ile bilinen backdoor ve zararlı kod imzalarının taranması |
| 4. İzin / Yetki Analizi | SUID/SGID ve yürütme izinlerindeki şüpheli değişikliklerin tespiti |
| 5. Skorlama ve Zaman Çizelgesi | Tüm katmanlardan gelen bulguların ağırlıklandırılıp tek bir şüphe skoruna dönüştürülmesi |
| 6. Değerlendirme | Yöntemin bilinen gerçek CVE örnekleriyle test edilmesi |

## Arayüz Fonksiyonel Gereksinimleri

| Kod | Gereksinim |
|---|---|
| FR-1 | Kullanıcı, orijinal (referans) ve şüpheli firmware imajlarını arayüz üzerinden yükleyebilecektir. |
| FR-2 | Arayüz, iki imaj arasındaki SHA-256 hash farklarını karşılaştırıp değişen dosyaları tablo halinde listeleyebilecektir. |
| FR-3 | Kullanıcı, seçtiği bölüm/dosyanın entropi grafiğini görebilecek; şüpheli alanlar görsel olarak işaretlenebilecektir. |
| FR-4 | Arayüz, YARA kuralları ile zararlı kod izlerini tarayıp risk derecesiyle gösterebilecektir. |
| FR-5 | Arayüz, SUID/SGID izin değişikliklerini ayrı bir sekmede raporlayabilecektir. |
| FR-6 | Bulgular kronolojik bir zaman çizelgesinde ve 0-100 arası şüphe skoru olarak gösterilecektir. |
| FR-7 | Kullanıcı, tüm bulguları delil zinciriyle birlikte PDF/HTML rapor olarak indirebilecektir. |
| FR-8 | Kullanıcı, her analiz katmanının sonuçlarını arayüzde ayrı sekmelerde inceleyebilecektir. |

## Kullanılacak Teknolojiler

- **Dil:** Python
- **Statik analiz:** binwalk, hashlib (SHA-256)
- **İmza tarama:** YARA
- **Arayüz:** Streamlit
- **Versiyon kontrolü:** Git / GitHub

## Kullanım

> Geliştirme ilerledikçe bu bölüm, kurulum adımları ve çalıştırma komutlarıyla güncellenecektir.

```bash
# Depoyu klonlayın
git clone <repo-url>
cd <repo-adi>

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Arayüzü başlatın
streamlit run app.py
```

## Proje Planı (20 İş Günü)

| Hafta | Başlık | Yapılacaklar |
|---|---|---|
| 1. Hafta | Veri toplama ve temel katman | Firmware imajlarının toplanması, statik bütünlük katmanının geliştirilmesi |
| 2. Hafta | İleri analiz katmanları | Entropi, YARA imza tarama ve izin/yetki analizi katmanlarının geliştirilmesi |
| 3. Hafta | Skorlama ve delil zinciri | Şüphe skoru, zaman çizelgesi, chain of custody belgeleme |
| 4. Hafta | Değerlendirme, arayüz ve raporlama | CVE ile test, Streamlit arayüzü, rapor çıktısı, dokümantasyon |

## Günlük İlerleme

Her günün yapılan çalışmaları [`daily_log.md`](./daily_log.md) dosyasında tarih bazında kayıt altına alınmaktadır.

## Lisans

Bu proje, Spikedge bünyesinde yürütülen staj kapsamında eğitim amaçlı geliştirilmektedir.
