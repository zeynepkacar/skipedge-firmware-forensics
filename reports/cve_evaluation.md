# CVE Evaluation: CVE-2024-54143 (OpenWrt Attended Sysupgrade Server)

## Summary

CVE-2024-54143 is a critical vulnerability (CVSS 9.3) disclosed in December 2024
by Flatt Security researcher RyotaK. It affects OpenWrt's Attended Sysupgrade
(ASU) service, which builds and serves custom firmware images on demand.

The vulnerability combines two issues:
1. A command injection flaw in the imagebuilder process
2. A weak hash vulnerability (CWE-328): the SHA-256 hash used to verify build
   requests was truncated to only 12 characters

The truncated hash significantly reduces the hash space, making it feasible for
an attacker to engineer a hash collision. This allows an attacker to "poison"
the artifact cache: a malicious firmware image can be served in place of a
legitimate one, and the integrity check will not detect the substitution.

## Relevance to This Project

This CVE is a direct real-world instance of the exact threat model this project
was designed to detect: a firmware integrity check that can be silently
bypassed, allowing a compromised image to reach a device undetected.

## How This Project's Method Relates to the Vulnerability

The static integrity layer of this project (`layers/static_integrity.py`) uses
**full-length SHA-256 hashes** (64 hexadecimal characters / 256 bits) for every
file comparison, with no truncation.

This matters directly: the vulnerability in CVE-2024-54143 exists specifically
*because* the hash was shortened to 12 characters. A 12-character hex hash has
16^12 (~2.8 x 10^14) possible values, while a full SHA-256 hash has
16^64 (~1.16 x 10^77) possible values. The dramatically smaller space of a
truncated hash makes deliberate collisions computationally realistic; a full
256-bit hash does not share this weakness.

See `data/hash_truncation_demo.py` for a numerical illustration of this
difference in collision resistance.

## Conclusion

This project's static integrity layer, by design, avoids the specific class of
weakness exploited by CVE-2024-54143. This does not mean the tool is immune to
all integrity-check bypass techniques, but it demonstrates that a foundational
design choice (full-length, untruncated cryptographic hashing) directly
addresses a real, recently disclosed, critical-severity vulnerability in a
widely used firmware ecosystem (OpenWrt).

## Source

- CVE-2024-54143, disclosed December 2024
- Reported by RyotaK (Flatt Security)
- Reference: https://www.theregister.com/2024/12/09/openwrt_firmware_vulnerabilities/