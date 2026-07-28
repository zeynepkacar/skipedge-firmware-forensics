"""
Practical test for CVE-2024-9643 relevance: adds a hard-coded credential
string (matching the CVE's pattern) to data/suspicious, then runs the YARA
layer to confirm it is detected as a new finding relative to data/original.
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from layers.yara_scan import scan_directory

suspicious_dir = "data/suspicious"
target_file = os.path.join(suspicious_dir, "etc/support_access.conf")

# Simulates a hard-coded credential left in a config file, similar in
# pattern to the fixed admin account behind CVE-2024-9643
with open(target_file, "w") as f:
    f.write("# support access\nadmin:admin\npassword=support123\n")

print(f"Hard-coded credential test file created: {target_file}\n")

print("=== YARA scan: data/original ===")
original_findings = scan_directory("data/original")
print(f"Files with matches: {len(original_findings)}")

print("\n=== YARA scan: data/suspicious ===")
suspicious_findings = scan_directory(suspicious_dir)
print(f"Files with matches: {len(suspicious_findings)}")

target_relative_path = os.path.join("etc", "support_access.conf")
if target_relative_path in suspicious_findings:
    print(f"\nDetected: {suspicious_findings[target_relative_path]}")
else:
    print("\nNot detected - check the YARA rule pattern.")