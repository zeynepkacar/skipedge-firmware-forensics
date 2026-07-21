rule Suspicious_Backdoor_Keyword
{
    meta:
        description = "Suspicious keywords associated with backdoors"
        risk = "high"
    strings:
        $s1 = "backdoor" nocase
        $s2 = "reverse_shell" nocase
        $s3 = "/bin/sh -i" nocase
        $s4 = "nc -e" nocase
    condition:
        any of them
}

rule Hardcoded_Credentials
{
    meta:
        description = "Suspected hardcoded credentials in code"
        risk = "medium"
    strings:
        $s1 = "password=" nocase
        $s2 = "admin:admin"
        $s3 = "root:root"
    condition:
        any of them
}

rule Suspicious_Network_Command
{
    meta:
        description = "Commands associated with remote access / command and control"
        risk = "high"
    strings:
        $s1 = "wget http" nocase
        $s2 = "curl http" nocase
        $s3 = "chmod 777" nocase
    condition:
        any of them
}