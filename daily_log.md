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
## 20.07.2026

**Yapılanlar:**
- Proje klasör yapısı oluşturuldu (data, layers, scoring, ui, reports)
- Statik bütünlük katmanı (layers/static_integrity.py) yazıldı — SHA-256 tabanlı dosya/blok hash karşılaştırması
- Entropi analizi katmanı (layers/entropy_analysis.py) yazıldı — Shannon entropi hesaplama
- Gerçek bir OpenWrt 25.12.5 (x86-64, squashfs) firmware imajı indirildi ve 940 gerçek dosya data/original altına çıkarıldı
- Gerçekçi saldırı simülasyonu oluşturuldu (data/tamper_firmware.py): backdoor dosyası eklendi (usr/bin/update_service), bir konfigürasyon dosyası değiştirildi (etc/dnsmasq.conf), şüpheli SUID izni verildi
- Statik bütünlük katmanı gerçek veriyle test edildi: backdoor ve değiştirilen dosya başarıyla tespit edildi
- Entropi analizi katmanında önemli bir bulgu: ham entropi eşiği, gerçek firmware'deki derlenmiş binary dosyaları (.so, .ko) nedeniyle çok sayıda yanlış alarm üretti. Bunun üzerine yöntem karşılaştırmalı entropi analizine (original vs suspicious) çevrildi
- Gözlem: entropi katmanı düz metin backdoor'u yakalayamadı (beklenen bir durum — şifrelenmemiş kod entropiyi yükseltmez), bu da YARA imza tarama katmanının (3. katman) gerekliliğini doğruladı
- .gitignore eklendi (büyük ham firmware dosyaları ve çıkarılmış dosya sistemleri repo dışında tutuluyor)
- Tüm değişiklikler GitHub'a commit ve push edildi

**Notlar / Sonraki Adımlar:**
- YARA imza/pattern tarama katmanına (3. katman) geçilecek
- İzin/yetki (SUID/SGID) analiz katmanına geçilecek