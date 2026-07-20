"""squashfs .img dosyasını açıp içindeki dosyaları data/original'a çıkarır."""
import os
from PySquashfsImage import SquashFsImage

image_path = "data/raw_firmware/openwrt-25.12.5-x86-64-generic-squashfs-rootfs.img"
output_dir = "data/original"

os.makedirs(output_dir, exist_ok=True)

image = SquashFsImage.from_file(image_path)

count = 0
for entry in image:
    if entry.is_dir:
        continue
    try:
        relative_path = entry.path.lstrip("/")
        full_output_path = os.path.join(output_dir, relative_path)
        os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
        with open(full_output_path, "wb") as f:
            f.write(entry.read_bytes())
        count += 1
    except Exception as e:
        print(f"Atlandı ({entry.path}): {e}")

print(f"Toplam {count} dosya çıkarıldı → {output_dir}")