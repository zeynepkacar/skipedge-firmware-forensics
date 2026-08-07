"""Unit tests for the permission analysis layer."""
import json
import os
import stat
import sys
import tempfile

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layers.permission_analysis import compare_permissions, has_suid_or_sgid


def _write_manifest(path, data):
    with open(path, "w") as f:
        json.dump(data, f)


def test_has_suid_or_sgid_true_for_suid_mode():
    mode = stat.S_ISUID | stat.S_IRWXU
    assert has_suid_or_sgid(mode) is True


def test_has_suid_or_sgid_false_for_normal_mode():
    mode = stat.S_IRWXU
    assert has_suid_or_sgid(mode) is False


def test_compare_permissions_detects_new_suid_file():
    with tempfile.TemporaryDirectory() as tmp_dir:
        original_path = os.path.join(tmp_dir, "original.json")
        suspicious_path = os.path.join(tmp_dir, "suspicious.json")

        _write_manifest(original_path, {})
        suid_mode = stat.S_ISUID | stat.S_IRWXU
        _write_manifest(suspicious_path, {
            "usr/bin/backdoor": {
                "mode": suid_mode,
                "filemode": "rws------",
                "uid": 0,
                "gid": 0,
            }
        })

        result = compare_permissions(original_path, suspicious_path)

        assert "usr/bin/backdoor" in result["new_suid_or_sgid_files"]


def test_compare_permissions_no_changes_for_identical_manifests():
    with tempfile.TemporaryDirectory() as tmp_dir:
        original_path = os.path.join(tmp_dir, "original.json")
        suspicious_path = os.path.join(tmp_dir, "suspicious.json")

        manifest = {"bin/ls": {"mode": 0o755, "filemode": "rwxr-xr-x", "uid": 0, "gid": 0}}
        _write_manifest(original_path, manifest)
        _write_manifest(suspicious_path, manifest)

        result = compare_permissions(original_path, suspicious_path)

        assert result["permission_changes"] == {}
        assert result["new_suid_or_sgid_files"] == {}