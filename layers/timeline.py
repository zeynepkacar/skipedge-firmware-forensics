"""
Timeline and Chain of Custody Layer
Converts findings from the scoring layer into a chronological event list,
and hashes each finding record to preserve evidence integrity.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.logger_config import get_logger

logger = get_logger(__name__)


def hash_finding(finding):
    """Computes a SHA-256 hash of a finding record for chain-of-custody purposes."""
    finding_json = json.dumps(finding, sort_keys=True)
    return hashlib.sha256(finding_json.encode("utf-8")).hexdigest()


def build_timeline(findings):
    """Converts a findings list into a timestamped, hashed event timeline."""
    timeline = []
    generated_at = datetime.now(timezone.utc).isoformat()

    for index, finding in enumerate(findings):
        event = {
            "event_id": index + 1,
            "timestamp": generated_at,
            "layer": finding["layer"],
            "file": finding["file"],
            "finding_type": finding["type"],
            "points": finding["points"],
        }
        event["evidence_hash"] = hash_finding(event)
        timeline.append(event)

    return timeline


def save_timeline(timeline, output_path="reports/timeline.json"):
    """Saves the timeline to a JSON file for later reporting."""
    with open(output_path, "w") as f:
        json.dump(timeline, f, indent=2)
    return output_path


def verify_timeline_integrity(timeline):
    """Re-computes hashes for each event and checks they match the stored hash."""
    for event in timeline:
        stored_hash = event["evidence_hash"]
        event_copy = {k: v for k, v in event.items() if k != "evidence_hash"}
        recomputed_hash = hash_finding(event_copy)
        if recomputed_hash != stored_hash:
            return False
    return True


if __name__ == "__main__":
    from layers.scoring import run_all_layers, build_findings_and_score

    results = run_all_layers("data/original", "data/suspicious")
    findings, final_score = build_findings_and_score(results)

    timeline = build_timeline(findings)
    output_path = save_timeline(timeline)
    logger.info(f"Timeline saved -> {output_path}")

    integrity_ok = verify_timeline_integrity(timeline)
    logger.info(f"Integrity check: {'PASSED' if integrity_ok else 'FAILED'}")