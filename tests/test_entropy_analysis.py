"""Unit tests for the entropy analysis layer."""
import os
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.entropy_analysis import calculate_entropy, compare_entropy


def test_calculate_entropy_of_uniform_data_is_low():
    """Repeating a single byte should produce near-zero entropy."""
    data = b"A" * 256
    entropy = calculate_entropy(data)
    assert entropy < 1.0


def test_calculate_entropy_of_random_data_is_high():
    """Random-looking data should produce high entropy."""
    data = bytes(range(256))
    entropy = calculate_entropy(data)
    assert entropy > 7.0


def test_calculate_entropy_of_empty_data_is_zero():
    assert calculate_entropy(b"") == 0.0


def test_compare_entropy_detects_new_high_entropy_file():
    """A new file with random content should appear as a new suspicious file."""
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        with open(os.path.join(suspicious_dir, "payload.bin"), "wb") as f:
            f.write(os.urandom(2048))

        result = compare_entropy(original_dir, suspicious_dir)

        assert "payload.bin" in result["new_suspicious_files"]


def test_compare_entropy_no_changes_for_identical_files():
    with tempfile.TemporaryDirectory() as original_dir, \
         tempfile.TemporaryDirectory() as suspicious_dir:

        for target_dir in (original_dir, suspicious_dir):
            with open(os.path.join(target_dir, "same.txt"), "w") as f:
                f.write("identical content" * 20)

        result = compare_entropy(original_dir, suspicious_dir)

        assert result["changed_entropy_files"] == {}
        assert result["new_suspicious_files"] == []