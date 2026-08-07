"""Unit tests for the scoring layer."""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.scoring import build_findings_and_score, WEIGHTS, MAX_SCORE


def _empty_results():
    return {
        "static": {"added_files": [], "modified_files": [], "deleted_files": []},
        "entropy": {"new_suspicious_files": [], "changed_entropy_files": {}},
        "yara_original": {},
        "yara_suspicious": {},
        "permission": {"new_suid_or_sgid_files": {}, "permission_changes": {}},
    }


def test_build_findings_and_score_with_no_findings():
    findings, score = build_findings_and_score(_empty_results())
    assert findings == []
    assert score == 0


def test_build_findings_and_score_with_added_file():
    results = _empty_results()
    results["static"]["added_files"] = ["backdoor.sh"]

    findings, score = build_findings_and_score(results)

    assert score == WEIGHTS["static_added_file"]
    assert len(findings) == 1
    assert findings[0]["type"] == "added_file"


def test_build_findings_and_score_caps_at_max_score():
    results = _empty_results()
    # Add many findings so the raw sum exceeds MAX_SCORE
    results["static"]["added_files"] = [f"file_{i}.sh" for i in range(20)]

    findings, score = build_findings_and_score(results)

    assert score == MAX_SCORE


def test_build_findings_and_score_ignores_preexisting_yara_matches():
    """YARA matches present in both original and suspicious should not be counted."""
    results = _empty_results()
    match = {"rule_name": "Hardcoded_Credentials", "risk": "medium", "description": "test"}
    results["yara_original"] = {"config.conf": [match]}
    results["yara_suspicious"] = {"config.conf": [match]}

    findings, score = build_findings_and_score(results)

    assert findings == []
    assert score == 0