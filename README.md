# skipedge-firmware-forensics

# Gömülü Sistem Firmware'lerinde Çok Katmanlı Bütünlük İhlali Tespiti ve Adli Bilişim Analizi

*Multi-Layer Firmware Integrity Violation Detection and Digital Forensics Analysis for Embedded Systems*

Bu proje, Spikedge bünyesinde yürütülen yaz stajı kapsamında geliştirilmektedir.

## Proje Hakkında

- **Öğrenci:** Zeynep
- **Bölüm:** Adli Bilişim Mühendisliği (3. sınıf → 4. sınıf)
- **Şirket:** Spikedge
- **Staj türü:** 20 iş günü

## Amaç

Spikedge gibi firmaların geliştirdiği gömülü/endüstriyel cihazlar, secure boot ve OTA (over-the-air) güncelleme mekanizmalarıyla korunur. Ancak bir firmware güncellemesi tedarik zinciri saldırısı, yetkisiz müdahale veya iç tehdit yoluyla manipüle edilirse (arka kapı eklenmesi, izin değişikliği, kod enjeksiyonu), bu ihlalin ne zaman, nasıl ve hangi kanıtlarla tespit edilebileceği kritik bir sorudur.

Bu projenin amacı; iki firmware imajı (orijinal ve şüpheli/güncellenmiş) arasındaki bütünlük ihlallerini birden fazla bağımsız analiz katmanına dayanarak tespit eden, bulgularını delil zinciriyle (chain of custody) belgeleyen ve sonucu tek bir şüphe skoru ile özetleyen çok katmanlı bir dijital adli bilişim analiz sistemidir.

## Kapsam

- Gerçek açık kaynak firmware imajları (OpenWrt) üzerinde statik analiz
- Çok katmanlı analiz motoru (bkz. aşağıda)
- Delil zinciri (chain of custody) ile bulgu bütünlüğünün SHA-256 tabanlı korunması
- Bilinen gerçek CVE örnekleriyle yöntemin değerlendirilmesi
- Streamlit tabanlı web arayüzü ve komut satırı (CLI) aracı üzerinden görselleştirme ve raporlama
- Otomatik test paketi (pytest) ile tüm katmanların doğrulanması

## Analiz Katmanları

| Katman                         | İşlevi                                                                                               | Durum |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- | ----- |
| 1. Statik Bütünlük             | Dosya/blok seviyesinde SHA-256 hash karşılaştırma; eklenen, silinen, değiştirilen dosyaların tespiti | ✅ |
| 2. Entropi Analizi             | Firmware bölümlerinin entropi değerleri hesaplanarak gizlenmiş/şifrelenmiş kötü amaçlı kodun tespiti | ✅ |
| 3. İmza / Pattern Tarama       | YARA kuralları ile bilinen backdoor ve zararlı kod imzalarının taranması                             | ✅ |
| 4. İzin / Yetki Analizi        | SUID/SGID ve yürütme izinlerindeki şüpheli değişikliklerin tespiti                                   | ✅ |
| 5. Skorlama ve Zaman Çizelgesi | Tüm katmanlardan gelen bulguların ağırlıklandırılıp tek bir şüphe skoruna dönüştürülmesi             | ✅ |
| 6. Değerlendirme               | Yöntemin bilinen gerçek CVE örnekleriyle test edilmesi (bkz. `/reports`)                              | ✅ |

Skorlama ağırlıkları kod içine gömülü değildir, `config.json` dosyasından yapılandırılabilir.

## Arayüz Fonksiyonel Gereksinimleri

| Kod  | Gereksinim                                                                                                             | Durum |
| ---- | ---------------------------------------------------------------------------------------------------------------------- | ----- |
| FR-1 | Kullanıcı, orijinal ve şüpheli firmware imajlarını arayüz üzerinden yükleyebilir.                                      | ✅ |
| FR-2 | Arayüz, iki imaj arasındaki SHA-256 hash farklarını karşılaştırıp değişen dosyaları tablo halinde listeler.            | ✅ |
| FR-3 | Entropi bulguları arayüzde şüpheli bölgeler olarak listelenir.                                                         | ✅ |
| FR-4 | Arayüz, YARA kuralları ile zararlı kod izlerini tarayıp risk derecesiyle gösterir.                                     | ✅ |
| FR-5 | Arayüz, SUID/SGID izin değişikliklerini ayrı bir sekmede raporlar.                                                     | ✅ |
| FR-6 | Bulgular kronolojik bir zaman çizelgesinde ve 0-100 arası şüphe skoru olarak gösterilir.                               | ✅ |
| FR-7 | Kullanıcı, tüm bulguları delil zinciriyle birlikte HTML rapor olarak indirebilir.                                      | ✅ |
| FR-8 | Kullanıcı, her analiz katmanının sonuçlarını arayüzde ayrı sekmelerde inceleyebilir.                                   | ✅ |

## Kullanılacak Teknolojiler

- **Dil:** Python
- **Statik analiz:** PySquashfsImage, hashlib (SHA-256)
- **İmza tarama:** YARA (yara-python)
- **Arayüz:** Streamlit
- **Test:** pytest
- **Versiyon kontrolü:** Git / GitHub

## Kullanım

```
# Depoyu klonlayın
git clone https://github.com/zeynepkacar/skipedge-firmware-forensics.git
cd skipedge-firmware-forensics

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Firmware imajını hazırlayın (data/raw_firmware altına .img.gz koyup)
python data/decompress_firmware.py
python data/extract_squashfs.py
python data/tamper_firmware.py

# Analiz katmanlarını tek tek çalıştırmak isterseniz
python layers/static_integrity.py
python layers/entropy_analysis.py
python layers/yara_scan.py
python layers/permission_analysis.py
python layers/scoring.py
python layers/timeline.py

# Web arayüzünü başlatmak için
streamlit run app.py
```

Arayüz açıldığında (`localhost:8501`), orijinal ve şüpheli firmware imajlarını (`.img` veya `.img.gz`) yükleyip "Analizi Başlat" ile sonuçları görebilir, HTML rapor olarak indirebilirsiniz.

## Komut Satırı Kullanımı (CLI)

Web arayüzü yerine doğrudan komut satırından da çalıştırılabilir, örneğin otomasyon senaryoları için:

```
python main.py --original data/original --suspicious data/suspicious
```

İzin manifestlerinin varsayılan konumdan farklı olduğu durumlar için `--original-manifest` ve `--suspicious-manifest` parametreleri de kullanılabilir.

## Testleri Çalıştırma

Proje, 6 analiz katmanının ve skorlama mantığının tamamını kapsayan otomatik bir test paketine sahiptir:

```
pytest tests/ -v
```

## Değerlendirme (Gerçek CVE Örnekleri)

Yöntem, iki gerçek ve güncel CVE ile doğrulanmıştır:

- **CVE-2024-54143** (OpenWrt Attended Sysupgrade, kısaltılmış hash zafiyeti) — bkz. `reports/cve_evaluation.md`
- **CVE-2024-9643** (Four-Faith router, hardcoded credentials) — bkz. `reports/cve_evaluation_2.md`

## Proje Planı (20 İş Günü)

| Hafta    | Başlık                             | Yapılacaklar                                                                 |
| -------- | ---------------------------------- | ---------------------------------------------------------------------------- |
| 1. Hafta | Veri toplama ve temel katman       | Firmware imajlarının toplanması, statik bütünlük ve entropi katmanları       |
| 2. Hafta | İleri analiz katmanları            | YARA imza tarama ve izin/yetki analizi katmanları                            |
| 3. Hafta | Skorlama ve delil zinciri          | Şüphe skoru, zaman çizelgesi, chain of custody belgeleme                     |
| 4. Hafta | Değerlendirme, arayüz ve raporlama | CVE ile test, Streamlit arayüzü, rapor çıktısı, entegrasyon testi, dokümantasyon |

Gerçek ilerleme günlüğü [`daily_log.md`](./daily_log.md) dosyasında tarih bazında tutulmaktadır.

## Literatür Taraması

Ana projeye paralel olarak, akademik bir literatür taraması görevi de yürütülmektedir: proje konusu ve çevresindeki alanlarda 2024–2026 arası yayınlanmış minimum 30 makalenin taranması, değerlendirilmesi ve kodlu/reproduction'a uygun olanların doğrulanması.

Bu çalışmanın tüm çıktıları [`/literature-review`](./literature-review) klasöründe yer almaktadır:

- **30 makale** taranmış ve değerlendirilmiştir (2024–2026 aralığında, USENIX Security, ACM CCS, IEEE S&P, NDSS, DFRWS gibi başlıca konferans/dergilerden)
- Literatür taramasında kodlu/reproduction'a uygun **10 makale** belirlendi. Bunlardan biri (P25, LFwC) aracın kendisi değil bir veri seti olduğu için ayrı değerlendirildi; kalan 9 araçtan 8'i tam, 1'i (ROSA) kısmi olarak doğrulandı, 1 araç (ChkUp) test edilemedi.
- Her makale için doldurulmuş "Makale İnceleme Şablonu" dosyaları `/literature-review/articles/` altında bulunmaktadır
- Kullanılan arama stratejisi ve karşılaştırma tablosu için sırasıyla `arama-stratejisi.md` ve `ozet-karsilastirma-tablosu.md` dosyalarına bakınız.

## Lisans

Bu proje, Spikedge bünyesinde yürütülen staj kapsamında eğitim amaçlı geliştirilmiştir. Ayrıntılar için [`LICENSE`](./LICENSE) dosyasına bakınız.
