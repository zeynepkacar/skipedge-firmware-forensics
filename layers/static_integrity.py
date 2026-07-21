"""
Static Integrity Layer
Performs SHA-256 based hash comparison between two firmware directories.
Detects added, deleted, and modified files.
"""

import hashlib
import os


def calculate_file_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()


def scan_directory(directory_path):
    """Extracts hashes for all files in a directory.
    Returns: {relative_file_path: hash} dictionary
    """
    file_hashes = {}
    for root, _, files in os.walk(directory_path):
        for filename in files:
            full_path = os.path.join(root, filename)
            relative_path = os.path.relpath(full_path, directory_path)
            file_hashes[relative_path] = calculate_file_hash(full_path)
    return file_hashes


def compare_firmware(original_dir, suspicious_dir):
    """Compares two firmware directories and reports the differences."""
    original_hashes = scan_directory(original_dir)
    suspicious_hashes = scan_directory(suspicious_dir)

    original_files = set(original_hashes.keys())
    suspicious_files = set(suspicious_hashes.keys())

    added_files = suspicious_files - original_files
    deleted_files = original_files - suspicious_files
    common_files = original_files & suspicious_files

    modified_files = [
        f for f in common_files
        if original_hashes[f] != suspicious_hashes[f]
    ]

    return {
        "added_files": sorted(added_files),
        "deleted_files": sorted(deleted_files),
        "modified_files": sorted(modified_files),
        "total_original_files": len(original_files),
        "total_suspicious_files": len(suspicious_files),
    }


if __name__ == "__main__":
    result = compare_firmware("data/original", "data/suspicious")
    print("=== Static Integrity Analysis Results ===")
    print(f"Added files: {result['added_files']}")
    print(f"Deleted files: {result['deleted_files']}")
    print(f"Modified files: {result['modified_files']}")