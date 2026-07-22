"""Extracts a squashfs .img file's contents into a directory, and saves a
permission manifest (mode/uid/gid) since Windows/NTFS cannot store Unix
permission bits like SUID/SGID.
"""
import json
import os
import sys
from PySquashfsImage import SquashFsImage

image_path = "data/raw_firmware/openwrt-25.12.5-x86-64-generic-squashfs-rootfs.img"
output_dir = "data/original"
manifest_path = "data/original_permissions.json"


def main():
    os.makedirs(output_dir, exist_ok=True)
    image = SquashFsImage.from_file(image_path)

    count = 0
    permissions = {}

    for entry in image:
        if entry.is_dir:
            continue
        relative_path = entry.path.lstrip("/")
        try:
            permissions[relative_path] = {
                "mode": entry.mode,
                "filemode": entry.filemode,
                "uid": entry.uid,
                "gid": entry.gid,
            }
        except Exception as e:
            print(f"Could not read permissions ({entry.path}): {e}")

        try:
            full_output_path = os.path.join(output_dir, relative_path)
            os.makedirs(os.path.dirname(full_output_path), exist_ok=True)
            with open(full_output_path, "wb") as f:
                f.write(entry.read_bytes())
            count += 1
        except Exception as e:
            print(f"Skipped ({entry.path}): {e}")

    with open(manifest_path, "w") as f:
        json.dump(permissions, f, indent=2)

    print(f"Total {count} files extracted -> {output_dir}")
    print(f"Permission manifest saved -> {manifest_path}")


if __name__ == "__main__":
    main()