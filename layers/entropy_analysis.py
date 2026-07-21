"""
Entropy Analysis Layer
Splits files into fixed-size blocks and calculates the Shannon entropy of each block.
High-entropy regions may indicate encrypted/obfuscated code.
"""

import math
import os
from collections import Counter

ENTROPY_THRESHOLD = 6.8
BLOCK_SIZE = 256  # bytes


def calculate_entropy(data):
    """Calculates the Shannon entropy of a byte sequence (0-8 range)."""
    if not data:
        return 0.0

    byte_counts = Counter(data)
    length = len(data)
    entropy = 0.0

    for count in byte_counts.values():
        probability = count / length
        entropy -= probability * math.log2(probability)

    return entropy


def analyze_file_entropy(file_path, block_size=BLOCK_SIZE):
    """Splits a file into blocks and calculates the entropy of each block.
    Returns: [{block_index, offset, entropy, suspicious}, ...] list
    """
    results = []
    with open(file_path, "rb") as f:
        block_index = 0
        while True:
            block = f.read(block_size)
            if not block:
                break
            entropy = calculate_entropy(block)
            results.append({
                "block_index": block_index,
                "offset": block_index * block_size,
                "entropy": round(entropy, 3),
                "suspicious": entropy >= ENTROPY_THRESHOLD,
            })
            block_index += 1
    return results


def scan_directory_entropy(directory_path):
    """Runs entropy analysis for all files in a directory.
    Returns: {relative_file_path: [block results]} dictionary
    """
    all_results = {}
    for root, _, files in os.walk(directory_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, directory_path)
            all_results[relative_path] = analyze_file_entropy(full_path)
    return all_results


def summarize_suspicious_blocks(scan_results):
    """Summarizes suspicious (high-entropy) blocks by file."""
    summary = {}
    for file_path, blocks in scan_results.items():
        suspicious_blocks = [b for b in blocks if b["suspicious"]]
        if suspicious_blocks:
            summary[file_path] = {
                "total_blocks": len(blocks),
                "suspicious_block_count": len(suspicious_blocks),
                "suspicious_offsets": [b["offset"] for b in suspicious_blocks],
                "max_entropy": max(b["entropy"] for b in blocks),
            }
    return summary


def compare_entropy(original_dir, suspicious_dir):
    """Compares two firmware directories and detects entropy shifts in shared files."""
    original_results = scan_directory_entropy(original_dir)
    suspicious_results = scan_directory_entropy(suspicious_dir)

    common_files = set(original_results.keys()) & set(suspicious_results.keys())
    only_in_suspicious = set(suspicious_results.keys()) - set(original_results.keys())

    entropy_changes = {}

    for file_path in common_files:
        orig_blocks = original_results[file_path]
        susp_blocks = suspicious_results[file_path]
        if len(orig_blocks) != len(susp_blocks):
            entropy_changes[file_path] = "size changed, block count differs"
            continue
        orig_avg = sum(b["entropy"] for b in orig_blocks) / len(orig_blocks) if orig_blocks else 0
        susp_avg = sum(b["entropy"] for b in susp_blocks) / len(susp_blocks) if susp_blocks else 0
        if abs(orig_avg - susp_avg) > 0.5:
            entropy_changes[file_path] = f"average entropy {orig_avg:.2f} -> {susp_avg:.2f}"

    new_high_entropy_files = {
        f: suspicious_results[f]
        for f in only_in_suspicious
        if any(b["suspicious"] for b in suspicious_results[f])
    }

    return {
        "changed_entropy_files": entropy_changes,
        "new_suspicious_files": list(new_high_entropy_files.keys()),
    }


if __name__ == "__main__":
    print("=== Comparative Entropy Analysis: original vs suspicious ===")
    comparison = compare_entropy("data/original", "data/suspicious")
    print(f"Common files with changed entropy: {comparison['changed_entropy_files']}")
    print(f"New high-entropy files only in suspicious: {comparison['new_suspicious_files']}")