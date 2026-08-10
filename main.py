"""
Command-line interface for the firmware forensics toolkit.
Usage:
    python main.py --original data/original --suspicious data/suspicious
"""
import argparse

from layers.scoring import run_all_layers, build_findings_and_score
from layers.timeline import build_timeline, verify_timeline_integrity


def main():
    parser = argparse.ArgumentParser(
        description="Multi-layer firmware integrity violation detection tool."
    )
    parser.add_argument("--original", required=True, help="Path to the original firmware directory")
    parser.add_argument("--suspicious", required=True, help="Path to the suspicious firmware directory")
    parser.add_argument(
        "--original-manifest",
        default=None,
        help="Path to the original permission manifest JSON (default: <original_parent>/original_permissions.json)",
    )
    parser.add_argument(
        "--suspicious-manifest",
        default=None,
        help="Path to the suspicious permission manifest JSON (default: <suspicious_parent>/suspicious_permissions.json)",
    )
    args = parser.parse_args()

    results = run_all_layers(
        args.original, args.suspicious, args.original_manifest, args.suspicious_manifest
    )
    findings, score = build_findings_and_score(results)
    timeline = build_timeline(findings)
    integrity_ok = verify_timeline_integrity(timeline)

    print(f"Suspicion Score: {score}/100")
    print(f"Total Findings: {len(findings)}")
    print(f"Evidence Chain Integrity: {'PASSED' if integrity_ok else 'FAILED'}\n")

    for event in timeline:
        print(f"  [{event['layer']}] {event['file']} -> {event['finding_type']} (+{event['points']})")


if __name__ == "__main__":
    main()