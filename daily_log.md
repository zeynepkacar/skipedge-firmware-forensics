# Günlük Çalışma Kaydı (Daily Log)

Bu dosya, staj süresince her gün yapılan çalışmaları tarih bazında kayıt altına almak için kullanılmaktadır.

---

## 17.07.2026

**Yapılanlar:**
- Proje konusu ve kapsamı netleştirildi: "Gömülü Sistem Firmware'lerinde Çok Katmanlı Bütünlük İhlali Tespiti ve Adli Bilişim Analizi"
- Proje önerisi dokümanı (amaç, kapsam, analiz katmanları, yöntem/araçlar, 20 iş günlük plan) hazırlandı
- Arayüz tasarımı planlandı (özet kartları, katman bazlı sekmeler, olay zaman çizelgesi, delil zinciri paneli, rapor dışa aktarma)
- Arayüz fonksiyonel gereksinimleri (FR-1 – FR-8) belirlendi
- GitHub reposu oluşturuldu, README.md ve daily_log.md eklendi

**Notlar / Sonraki Adımlar:**
- Açık kaynak firmware imajlarının (OpenWrt / Yocto örnek build) toplanmasına başlanacak
- Statik bütünlük (hash karşılaştırma) katmanının geliştirilmesine geçilecek

---
## 20.07.2026

**Yapılanlar:**
- Proje klasör yapısı oluşturuldu (data, layers, scoring, ui, reports)
- Statik bütünlük katmanı (static_integrity.py) yazıldı — SHA-256 tabanlı hash karşılaştırma
- Test verisiyle doğrulandı: eklenen, değiştirilen, silinen dosya tespiti başarıyla çalıştı
- Entropi analizi katmanı (entropy_analysis.py) yazıldı — Shannon entropi hesaplama ile dosyaları 256 byte'lık bloklara bölüp analiz eden yapı kuruldu
- Test verisi üretimi için generate_test_data.py yazıldı (rastgele/yüksek entropili dosya oluşturuyor)
- İlk testte eşik değeri (7.5) çok sıkı çıktı, gerçek ölçümlere göre 6.8'e kalibre edildi
- Test sonucu doğrulandı: rastgele veri içeren dosya (hidden_payload.bin) başarıyla "şüpheli" olarak tespit edildi, normal metin dosyalarında yanlış alarm çıkmadı

