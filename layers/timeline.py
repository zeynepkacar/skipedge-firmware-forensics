"""
Timeline and Chain of Custody Layer
Converts findings from the scoring layer into a chronological event list,
and hashes each finding record to preserve evidence integrity.
"""

import hashlib
import json
from datetime import datetime, timezone


def hash_finding(finding):
    """Computes a SHA-256 hash of a finding record for chain-of-custody purposes."""
    finding_json = json.dumps(finding, sort_keys=True)
    return hashlib.sha256(finding_json.encode("utf-8")).hexdigest()


def build_timeline(findings):
    """Converts a findings list into a timestamped, hashed event timeline.
    Each event records: timestamp, layer, file, finding type, points, and
    a SHA-256 hash of the record for evidence integrity verification.
    """
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
    """Re-computes hashes for each event and checks they match the stored hash.
    Returns True if the entire timeline is untampered, False otherwise.
    """
    for event in timeline:
        stored_hash = event["evidence_hash"]
        event_copy = {k: v for k, v in event.items() if k != "evidence_hash"}
        recomputed_hash = hash_finding(event_copy)
        if recomputed_hash != stored_hash:
            return False
    return True


if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from layers.scoring import run_all_layers, build_findings_and_score

    print("Running all analysis layers...\n")
    results = run_all_layers("data/original", "data/suspicious")
    findings, final_score = build_findings_and_score(results)

    print(f"Suspicion score: {final_score}/100")
    print(f"Building timeline from {len(findings)} findings...\n")

    timeline = build_timeline(findings)
    output_path = save_timeline(timeline)

    print(f"Timeline saved -> {output_path}\n")
    print("=== Timeline ===")
    for event in timeline:
        print(f"  [{event['event_id']}] {event['layer']} | {event['file']} | {event['finding_type']} (+{event['points']}) | hash: {event['evidence_hash'][:16]}...")

    print(f"\nIntegrity check: {'PASSED' if verify_timeline_integrity(timeline) else 'FAILED'}")