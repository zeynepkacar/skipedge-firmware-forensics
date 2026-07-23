"""
Scoring Layer
Aggregates findings from all analysis layers into a single suspicion score (0-100)
and a chronological list of findings.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.static_integrity import compare_firmware
from layers.entropy_analysis import compare_entropy
from layers.yara_scan import scan_directory as yara_scan_directory
from layers.permission_analysis import compare_permissions

# Weight table: how many points each finding type contributes
WEIGHTS = {
    "static_added_file": 15,
    "static_modified_file": 10,
    "yara_high_risk": 25,
    "yara_medium_risk": 5,
    "entropy_new_suspicious_file": 15,
    "entropy_changed_file": 10,
    "permission_new_suid_sgid": 25,
    "permission_changed": 15,
}

MAX_SCORE = 100


def run_all_layers(original_dir, suspicious_dir):
    """Runs all four analysis layers and collects raw findings."""
    static_result = compare_firmware(original_dir, suspicious_dir)
    entropy_result = compare_entropy(original_dir, suspicious_dir)
    yara_original = yara_scan_directory(original_dir)
    yara_suspicious = yara_scan_directory(suspicious_dir)
    permission_result = compare_permissions(
        "data/original_permissions.json", "data/suspicious_permissions.json"
    )

    return {
        "static": static_result,
        "entropy": entropy_result,
        "yara_original": yara_original,
        "yara_suspicious": yara_suspicious,
        "permission": permission_result,
    }


def build_findings_and_score(results):
    """Converts raw layer results into a unified findings list and a total score."""
    findings = []
    score = 0

    # Static integrity findings
    for f in results["static"]["added_files"]:
        findings.append({"layer": "static_integrity", "file": f, "type": "added_file", "points": WEIGHTS["static_added_file"]})
        score += WEIGHTS["static_added_file"]
    for f in results["static"]["modified_files"]:
        findings.append({"layer": "static_integrity", "file": f, "type": "modified_file", "points": WEIGHTS["static_modified_file"]})
        score += WEIGHTS["static_modified_file"]

    # Entropy findings
    for f in results["entropy"]["new_suspicious_files"]:
        findings.append({"layer": "entropy", "file": f, "type": "new_high_entropy_file", "points": WEIGHTS["entropy_new_suspicious_file"]})
        score += WEIGHTS["entropy_new_suspicious_file"]
    for f in results["entropy"]["changed_entropy_files"]:
        findings.append({"layer": "entropy", "file": f, "type": "entropy_changed", "points": WEIGHTS["entropy_changed_file"]})
        score += WEIGHTS["entropy_changed_file"]

    # YARA findings: only count matches that are NEW in suspicious (not already
    # present in original) — pre-existing matches are normal firmware content,
    # not evidence of tampering
    original_yara_signatures = set()
    for file_path, matches in results["yara_original"].items():
        for match in matches:
            original_yara_signatures.add((file_path, match["rule_name"]))

    for file_path, matches in results["yara_suspicious"].items():
        for match in matches:
            signature = (file_path, match["rule_name"])
            if signature in original_yara_signatures:
                continue  # already present in original, not a new finding
            weight_key = "yara_high_risk" if match["risk"] == "high" else "yara_medium_risk"
            findings.append({
                "layer": "yara",
                "file": file_path,
                "type": f"rule_match:{match['rule_name']}",
                "points": WEIGHTS[weight_key],
            })
            score += WEIGHTS[weight_key]
            
    # Permission findings
    for f in results["permission"]["new_suid_or_sgid_files"]:
        findings.append({"layer": "permission", "file": f, "type": "new_suid_sgid", "points": WEIGHTS["permission_new_suid_sgid"]})
        score += WEIGHTS["permission_new_suid_sgid"]
    for f in results["permission"]["permission_changes"]:
        findings.append({"layer": "permission", "file": f, "type": "permission_changed", "points": WEIGHTS["permission_changed"]})
        score += WEIGHTS["permission_changed"]

    final_score = min(score, MAX_SCORE)

    return findings, final_score


if __name__ == "__main__":
    print("Running all analysis layers...\n")
    results = run_all_layers("data/original", "data/suspicious")
    findings, final_score = build_findings_and_score(results)

    print(f"=== Suspicion Score: {final_score}/100 ===\n")
    print(f"Total findings: {len(findings)}\n")
    for finding in findings:
        print(f"  [{finding['layer']}] {finding['file']} -> {finding['type']} (+{finding['points']})")