"""Unit tests for the YARA signature scanning layer."""
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.yara_scan import scan_directory


def test_scan_directory_detects_backdoor_keyword():
    with tempfile.TemporaryDirectory() as directory:
        with open(os.path.join(directory, "suspicious.sh"), "w") as f:
            f.write("#!/bin/sh\n# backdoor script\nreverse_shell connect\n")

        findings = scan_directory(directory)

        assert "suspicious.sh" in findings
        rule_names = [m["rule_name"] for m in findings["suspicious.sh"]]
        assert "Suspicious_Backdoor_Keyword" in rule_names


def test_scan_directory_detects_hardcoded_credentials():
    with tempfile.TemporaryDirectory() as directory:
        with open(os.path.join(directory, "config.conf"), "w") as f:
            f.write("admin:admin\npassword=test123\n")

        findings = scan_directory(directory)

        assert "config.conf" in findings
        rule_names = [m["rule_name"] for m in findings["config.conf"]]
        assert "Hardcoded_Credentials" in rule_names


def test_scan_directory_no_matches_for_clean_file():
    with tempfile.TemporaryDirectory() as directory:
        with open(os.path.join(directory, "clean.txt"), "w") as f:
            f.write("this is a normal, harmless configuration file\n")

        findings = scan_directory(directory)

        assert findings == {}