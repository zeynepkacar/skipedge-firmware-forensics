"""Unit tests for the static integrity layer."""
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.static_integrity import calculate_file_hash, compare_firmware


def test_calculate_file_hash_is_deterministic():
    """Same content should always produce the same hash."""
    with tempfile.NamedTemporaryFile(delete=False, mode="w") as f:
        f.write("test content")
        path = f.name

    hash1 = calculate_file_hash(path)
    hash2 = calculate_file_hash(path)
    os.remove(path)

    assert hash1 == hash2
    assert len(hash1) == 64  # SHA-256 hex digest length


def test_compare_firmware_detects_added_file():
    """A file present only in the suspicious dir should be reported as added."""
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        with open(os.path.join(suspicious_dir, "new_file.txt"), "w") as f:
            f.write("backdoor")

        result = compare_firmware(original_dir, suspicious_dir)

        assert "new_file.txt" in result["added_files"]
        assert result["deleted_files"] == []
        assert result["modified_files"] == []


def test_compare_firmware_detects_modified_file():
    """A file with different content in both dirs should be reported as modified."""
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        with open(os.path.join(original_dir, "config.txt"), "w") as f:
            f.write("original content")
        with open(os.path.join(suspicious_dir, "config.txt"), "w") as f:
            f.write("tampered content")

        result = compare_firmware(original_dir, suspicious_dir)

        assert "config.txt" in result["modified_files"]


def test_compare_firmware_detects_deleted_file():
    """A file present only in the original dir should be reported as deleted."""
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        with open(os.path.join(original_dir, "old_file.txt"), "w") as f:
            f.write("will be removed")

        result = compare_firmware(original_dir, suspicious_dir)

        assert "old_file.txt" in result["deleted_files"]


def test_compare_firmware_no_changes():
    """Identical directories should produce no findings."""
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        for target_dir in (original_dir, suspicious_dir):
            with open(os.path.join(target_dir, "same.txt"), "w") as f:
                f.write("identical content")

        result = compare_firmware(original_dir, suspicious_dir)

        assert result["added_files"] == []
        assert result["deleted_files"] == []
        assert result["modified_files"] == []