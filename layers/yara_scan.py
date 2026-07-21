"""
YARA Signature/Pattern Scanning Layer
Scans firmware files against known backdoor/malware signatures using YARA rules.
"""

import os
import yara

RULES_PATH = "rules/backdoor_rules.yar"


def load_rules(rules_path=RULES_PATH):
    """Compiles the YARA rules file."""
    return yara.compile(filepath=rules_path)


def scan_file(file_path, rules):
    """Scans a single file against the YARA rules.
    Returns: [{rule_name, description, risk, matched_strings}, ...] list
    """
    matches = rules.match(file_path)
    results = []
    for match in matches:
        results.append({
            "rule_name": match.rule,
            "description": match.meta.get("description", ""),
            "risk": match.meta.get("risk", "unknown"),
            "matched_strings": [str(s.instances[0].matched_data) for s in match.strings],
        })
    return results


def scan_directory(directory_path, rules_path=RULES_PATH):
    """Scans all files in a directory against the YARA rules.
    Returns: {relative_file_path: [match list]} dictionary (matches only)
    """
    rules = load_rules(rules_path)
    findings = {}

    for root, _, files in os.walk(directory_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, directory_path)
            try:
                matches = scan_file(full_path, rules)
                if matches:
                    findings[relative_path] = matches
            except yara.Error:
                continue

    return findings


if __name__ == "__main__":
    print("=== YARA Scan: data/original ===")
    original_findings = scan_directory("data/original")
    print(f"Files with matches: {len(original_findings)}")
    for file_path, matches in original_findings.items():
        print(f"  {file_path}: {matches}")

    print("\n=== YARA Scan: data/suspicious ===")
    suspicious_findings = scan_directory("data/suspicious")
    print(f"Files with matches: {len(suspicious_findings)}")
    for file_path, matches in suspicious_findings.items():
        print(f"  {file_path}: {matches}")