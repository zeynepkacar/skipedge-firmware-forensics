# CVE Evaluation: CVE-2024-9643 (Four-Faith F3x36 Industrial Router)

## Summary

CVE-2024-9643 is a critical authentication bypass vulnerability in Four-Faith
F3x36 industrial cellular routers. The firmware ships with hard-coded
administrative credentials embedded directly in the code - a fixed username
and password that cannot be changed by the device owner and is identical
across every unit of the affected model.

The vulnerability entered mass exploitation in May 2026: attackers use the
publicly known credentials to log in with full administrative privileges,
with no exploit code required beyond the credentials themselves. CrowdSec
observed the campaign folding compromised routers into a botnet.

## Relevance to This Project

This is a textbook example of CWE-798 (Use of Hard-coded Credentials) - a
vulnerability class this project's YARA layer (`layers/yara_scan.py`) was
explicitly designed to catch. The `Hardcoded_Credentials` rule in
`rules/backdoor_rules.yar` searches firmware files for patterns such as
`password=`, `admin:admin`, and `root:root`, which are exactly the kind of
static strings a hard-coded credential like the one in CVE-2024-9643 would
leave behind in a configuration file or binary.

## Practical Test

To confirm the YARA layer would flag this class of vulnerability, a
credential string matching the CVE-2024-9643 pattern (a fixed
username/password pair embedded in a config file) was added to
`data/suspicious` and scanned. See `data/hardcoded_credential_test.py` for
the test script and its output.

## Observed Limitation (from earlier testing)

During the initial YARA layer testing (Day 2, 21.07.2026), the
`Hardcoded_Credentials` rule also matched legitimate OpenWrt configuration
files (e.g. `pppd`, several `.js` files) that contain the string `password=`
as normal, non-malicious code. This is an honest limitation: a simple
string-matching rule cannot fully distinguish a genuinely hard-coded,
exploitable credential (like CVE-2024-9643) from ordinary code that merely
references the word "password". In a production system, this would need to
be combined with the scoring layer's comparative logic (only flag NEW matches
relative to the original firmware) - which this project's `scoring.py`
already implements - to reduce false positives to a manageable level.

## Conclusion

This project's YARA layer is capable of detecting the specific vulnerability
pattern behind CVE-2024-9643 (hard-coded credentials), but the evaluation
also surfaced a real precision limitation of simple signature matching. This
is documented honestly rather than overstated, and is mitigated (not fully
solved) by the comparative scoring approach already built into this project.

## Source

- CVE-2024-9643, Four-Faith F3x36 industrial routers
- Mass exploitation observed from May 12, 2026 (CrowdSec)
- Reference: https://secureiot.house/four-faith-router-cve-2024-9643-botnet-hardcoded-password-2026/