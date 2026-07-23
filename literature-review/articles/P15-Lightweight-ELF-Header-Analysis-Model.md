# Makale İnceleme Şablonu

## 1. Künye ve Meta Veri

| Alan | Bilgi |
| --- | --- |
| Makale ID | P15 |
| Başlık | Lightweight ELF header analysis model for IoT malwares detection based on machine learning |
| Yazarlar | Hattab Guesmi, Ali Khalfallah (Laboratory of Electronics and Microelectronics, Faculty of Sciences of Monastir, Monastir Üniversitesi, Tunus), Belgacem Bouallegue (Department of Computer Engineering, College of Computer Science, King Khalid Üniversitesi, Suudi Arabistan) |
| Yıl | 2025 |
| Yayın Yeri (Venue) | Engineering Research Express (IOP Publishing), Cilt 7, Sayı 2, Makale No: 025213 |
| DOI / Link | 10.1088/2631-8695/adca8a — https://iopscience.iop.org/article/10.1088/2631-8695/adca8a |
| Anahtar Kelimeler | ELF header, entropi, window entropy map (WEM), IoT malware tespiti, makine öğrenmesi, ARM mimarisi |

## 2. Teknik Analiz ve Metodoloji

- **Hedef Mimari:** ARM — gerçek dünya IoT malware örnekleri ARM mimarisini hedefliyor
- **Analiz Türü:** Statik — sadece ELF header üzerinde çalışıyor, tüm binary'yi işlemiyor; header'dan alınan veri uzunluğu 64 ile 1024 byte arasında değiştiriliyor
- **Tespit Edilen Tehdit Türü:** IoT malware tespiti (ikili sınıflandırma: zararlı/zararsız); belirli bir zafiyet türü değil, genel malware varlığı tespiti
- **Kullanılan Ana Teknik/Algoritma:** ELF header'dan entropi ve string tabanlı özellik çıkarma (window entropy map — WEM, byte entropy map — BEM, 2-gram, 2-gram matrisi), ardından bu özelliklerin Random Forest, Extra Trees, AdaBoost ve XGBoost gibi makine öğrenmesi algoritmalarıyla sınıflandırılması; 512 byte veri uzunluğunda %99.98 doğruluk ve %99.99 F1-skoru elde edilmiş

## 3. Veri Seti ve Tekrarlanabilirlik (Reproducibility)

- **Veri Seti:** ARM mimarisini hedefleyen gerçek dünya IoT malware örnekleri (makalede kaynak koleksiyonun tam adı/kökeni netleştirilmemiş)
- **Veri Seti Erişilebilir mi?** Belirtilmemiş — makalede ayrı bir veri seti paylaşım linki bulunamadı
- **Kaynak Kod Açık mı?** Hayır — GitHub veya başka bir kod deposu linki bulunamadı

## 4. Proje Kriterleriyle Karşılaştırma

| Kriter | Var mı? | Not |
| --- | --- | --- |
| Diferansiyel Analiz (A vs B imaj karşılaştırması) | Hayır | Tek dosya (ELF header) sınıflandırması yapıyor, iki imaj karşılaştırması yok |
| Çok Katmanlı Analiz (birden fazla bağımsız yöntem) | Hayır | Tek bir yöntem: ELF header'dan entropi/string özellik çıkarımı + ML sınıflandırma |
| Delil Zinciri (Chain of Custody / kriptografik doğrulama) | Hayır | Adli bilişim bağlamında bir unsur içermiyor |
| Tek Bir Şüphe Skoru ile Özetleme | Kısmen | ML sınıflandırıcısının çıktısı zararlı/zararsız olasılığı olarak yorumlanabilir, ama açık bir "şüphe skoru" tasarımı sunulmuyor |
| Tedarik Zinciri / İç Tehdit Senaryosu Ele Alınmış mı | Hayır | Doğrudan ele alınmıyor |

## 5. Değerlendirme

- **Bu makalenin projeme katkısı:** Sadece ELF header'a bakarak hızlı ve düşük kaynaklı bir ön-tarama fikri, projenin "hafif/hızlı ilk geçiş" katmanına ilham verebilir; entropi tabanlı özellik çıkarımı (WEM/BEM) projenin entropi analiz katmanı için referans olabilir.
- **Eksik bıraktığı nokta (Gap):** Sadece ELF header'a odaklanıyor, dosyanın geri kalanı (section'lar, gövde) analiz edilmiyor; adli bilişim unsurları (delil zinciri, raporlama, skorlama) tamamen yok; tek mimari (ARM) üzerinde test edilmiş; kod paylaşılmadığı için tekrarlanabilirlik zayıf; tedarik zinciri/iç tehdit senaryosu ele alınmıyor.
- **Uygunluk Skoru (1–5):** 2
- **Ek Notlar:** Hakemli (IOP Engineering Research Express), 2025'te yayınlanmış. Sonraki bazı çalışmalarda (örn. ELF binary'lerinde adversarial malware üretimi üzerine 2026 tarihli bir çalışma) referans olarak gösterilmiş, bu da makalenin literatürde belirli bir görünürlük kazandığını gösteriyor.
