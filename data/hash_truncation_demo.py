"""
Demonstrates why CVE-2024-54143's use of a truncated (12-character) SHA-256
hash is dramatically weaker than the full-length hash used in this project's
static integrity layer.
"""
import hashlib


def full_hash(data: bytes) -> str:
    """Full-length SHA-256 hash (64 hex characters / 256 bits), as used in
    this project's static_integrity.py."""
    return hashlib.sha256(data).hexdigest()


def truncated_hash(data: bytes, length: int = 12) -> str:
    """Truncated hash, matching the vulnerable pattern in CVE-2024-54143."""
    return hashlib.sha256(data).hexdigest()[:length]


def possible_values(hex_length: int) -> int:
    """Number of possible distinct hash values for a given hex string length."""
    return 16 ** hex_length


if __name__ == "__main__":
    sample_data = b"example firmware build request"

    full = full_hash(sample_data)
    truncated = truncated_hash(sample_data)

    print("=== Hash Truncation Comparison (CVE-2024-54143 context) ===\n")
    print(f"Full SHA-256 hash:      {full}")
    print(f"  Length: {len(full)} hex characters ({len(full) * 4} bits)")
    print(f"  Possible values: {possible_values(len(full)):.3e}\n")

    print(f"Truncated hash (CVE):   {truncated}")
    print(f"  Length: {len(truncated)} hex characters ({len(truncated) * 4} bits)")
    print(f"  Possible values: {possible_values(len(truncated)):.3e}\n")

    ratio = possible_values(len(full)) / possible_values(len(truncated))
    print(f"The full hash search space is {ratio:.3e} times larger than the truncated one.")
    print("This project's static_integrity.py always uses the full, untruncated hash.")