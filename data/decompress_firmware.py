"""'.img.gz' dosyasını açıp '.img' dosyasına çevirir."""
import gzip
import shutil

input_path = "data/raw_firmware/openwrt-25.12.5-x86-64-generic-squashfs-rootfs.img.gz"
output_path = "data/raw_firmware/openwrt-25.12.5-x86-64-generic-squashfs-rootfs.img"

with gzip.open(input_path, "rb") as f_in:
    with open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print(f"Açıldı: {output_path}")