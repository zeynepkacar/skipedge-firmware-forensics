"""
Permission Analysis Layer
Detects SUID/SGID permission changes and suspicious permission grants between
two firmware permission manifests (JSON files produced at extraction/tamper time).

Uses manifests instead of live filesystem stat() because Windows/NTFS does not
preserve Unix permission bits like SUID/SGID.
"""
import json
import stat


def load_manifest(manifest_path):
    """Loads a permission manifest JSON file.
    Returns: {relative_file_path: {mode, filemode, uid, gid}} dictionary
    """
    with open(manifest_path, "r") as f:
        return json.load(f)


def has_suid_or_sgid(mode):
    """Checks whether a numeric mode value has the SUID or SGID bit set."""
    return bool(mode & stat.S_ISUID) or bool(mode & stat.S_ISGID)


def compare_permissions(original_manifest_path, suspicious_manifest_path):
    """Compares two permission manifests.
    Flags: newly SUID/SGID files, and permission changes on shared files.
    """
    original_perms = load_manifest(original_manifest_path)
    suspicious_perms = load_manifest(suspicious_manifest_path)

    common_files = set(original_perms.keys()) & set(suspicious_perms.keys())
    only_in_suspicious = set(suspicious_perms.keys()) - set(original_perms.keys())

    permission_changes = {}
    for file_path in common_files:
        orig = original_perms[file_path]
        susp = suspicious_perms[file_path]
        if orig["mode"] != susp["mode"] or orig["uid"] != susp["uid"] or orig["gid"] != susp["gid"]:
            permission_changes[file_path] = {
                "original": orig,
                "suspicious": susp,
            }

    new_suid_or_sgid_files = {
        f: suspicious_perms[f]
        for f in only_in_suspicious
        if has_suid_or_sgid(suspicious_perms[f]["mode"])
    }

    return {
        "permission_changes": permission_changes,
        "new_suid_or_sgid_files": new_suid_or_sgid_files,
    }


if __name__ == "__main__":
    print("=== Permission Analysis: original vs suspicious ===")
    result = compare_permissions("data/original_permissions.json", "data/suspicious_permissions.json")

    print(f"\nFiles with changed permissions: {len(result['permission_changes'])}")
    for file_path, change in result["permission_changes"].items():
        print(f"  {file_path}: {change['original']['filemode']} -> {change['suspicious']['filemode']}")

    print(f"\nNew SUID/SGID files (only in suspicious): {len(result['new_suid_or_sgid_files'])}")
    for file_path, perms in result["new_suid_or_sgid_files"].items():
        print(f"  {file_path}: {perms['filemode']}")