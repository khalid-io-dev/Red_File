"""Security Tools Configuration - 50 Tools Total"""

SECURITY_TOOLS = {
    # Network Scanning (5)
    "nmap": {"name": "Nmap", "category": "network_scanning", "mitre": ["T1046"]},
    "masscan": {"name": "Masscan", "category": "network_scanning", "mitre": ["T1046"]},
    "portscan": {"name": "Port Scanner", "category": "network_scanning", "mitre": ["T1046"]},
    "responder": {"name": "Responder", "category": "network_scanning", "mitre": ["T1557"]},
    "crackmapexec": {"name": "CrackMapExec", "category": "network_scanning", "mitre": ["T1021"]},
    
    # Web Application (9)
    "sqlmap": {"name": "SQLMap", "category": "web_application", "mitre": ["T1190"]},
    "nikto": {"name": "Nikto", "category": "web_application", "mitre": ["T1190"]},
    "gobuster": {"name": "Gobuster", "category": "web_application", "mitre": ["T1083"]},
    "wpscan": {"name": "WPScan", "category": "web_application", "mitre": ["T1190"]},
    "wfuzz": {"name": "Wfuzz", "category": "web_application", "mitre": ["T1190"]},
    "ffuf": {"name": "Ffuf", "category": "web_application", "mitre": ["T1083"]},
    "commix": {"name": "Commix", "category": "web_application", "mitre": ["T1059"]},
    "nuclei": {"name": "Nuclei", "category": "web_application", "mitre": ["T1190"]},
    "webrecon": {"name": "Web Recon", "category": "web_application", "mitre": ["T1595"]},
    
    # Password Attacks (3)
    "hydra": {"name": "Hydra", "category": "password_attacks", "mitre": ["T1110"]},
    "john": {"name": "John the Ripper", "category": "password_attacks", "mitre": ["T1110"]},
    "hashcat": {"name": "Hashcat", "category": "password_attacks", "mitre": ["T1110"]},
    
    # OSINT (6)
    "theharvester": {"name": "theHarvester", "category": "osint", "mitre": ["T1589"]},
    "dnsenum": {"name": "DNSenum", "category": "osint", "mitre": ["T1590"]},
    "amass": {"name": "Amass", "category": "osint", "mitre": ["T1590"]},
    "sublist3r": {"name": "Sublist3r", "category": "osint", "mitre": ["T1590"]},
    "sherlock": {"name": "Sherlock", "category": "osint", "mitre": ["T1593"]},
    "searchsploit": {"name": "SearchSploit", "category": "osint", "mitre": ["T1588"]},
    
    # Exploitation (2)
    "metasploit": {"name": "Metasploit", "category": "exploitation", "mitre": ["T1203"]},
    "custom_exploit": {"name": "Custom Exploit", "category": "exploitation", "mitre": ["T1203"]},
    
    # SSL/TLS (2)
    "testssl": {"name": "TestSSL", "category": "ssl_tls", "mitre": ["T1040"]},
    "ssl_analyzer": {"name": "SSL Analyzer", "category": "ssl_tls", "mitre": ["T1040"]},
    
    # SMB/Windows (1)
    "enum4linux": {"name": "Enum4linux", "category": "smb_windows", "mitre": ["T1087"]},
    
    # Cloud Security (3)
    "aws_scanner": {"name": "AWS Scanner", "category": "cloud_security", "mitre": ["T1580"]},
    "azure_scanner": {"name": "Azure Scanner", "category": "cloud_security", "mitre": ["T1580"]},
    "gcp_scanner": {"name": "GCP Scanner", "category": "cloud_security", "mitre": ["T1580"]},
    
    # Container Security (2)
    "docker_scanner": {"name": "Docker Scanner", "category": "container_security", "mitre": ["T1610"]},
    "kubernetes_scanner": {"name": "Kubernetes Scanner", "category": "container_security", "mitre": ["T1610"]},
    
    # Network Analysis (3) - NEW
    "wireshark": {"name": "Wireshark", "category": "network_analysis", "mitre": ["T1040"]},
    "snort": {"name": "Snort", "category": "network_analysis", "mitre": ["T1040"]},
    "suricata": {"name": "Suricata", "category": "network_analysis", "mitre": ["T1040"]},
    
    # Wireless (1) - NEW
    "aircrack": {"name": "Aircrack-ng", "category": "wireless", "mitre": ["T1557"]},
    
    # Forensics (2) - NEW
    "volatility": {"name": "Volatility", "category": "forensics", "mitre": ["T1005"]},
    "autopsy": {"name": "Autopsy", "category": "forensics", "mitre": ["T1005"]},
    
    # Malware Analysis (2) - NEW
    "yara": {"name": "YARA", "category": "malware_analysis", "mitre": ["T1027"]},
    "cuckoo": {"name": "Cuckoo Sandbox", "category": "malware_analysis", "mitre": ["T1497"]},
    
    # Reverse Engineering (4) - NEW
    "radare2": {"name": "Radare2", "category": "reverse_engineering", "mitre": ["T1140"]},
    "ghidra": {"name": "Ghidra", "category": "reverse_engineering", "mitre": ["T1140"]},
    "frida": {"name": "Frida", "category": "reverse_engineering", "mitre": ["T1059"]},
    "binwalk": {"name": "Binwalk", "category": "reverse_engineering", "mitre": ["T1027"]},
}

TOOL_CATEGORIES = {
    "network_scanning": "Network Scanning",
    "web_application": "Web Application",
    "password_attacks": "Password Attacks",
    "osint": "OSINT",
    "exploitation": "Exploitation",
    "ssl_tls": "SSL/TLS",
    "smb_windows": "SMB/Windows",
    "cloud_security": "Cloud Security",
    "container_security": "Container Security",
    "network_analysis": "Network Analysis",
    "wireless": "Wireless",
    "forensics": "Forensics",
    "malware_analysis": "Malware Analysis",
    "reverse_engineering": "Reverse Engineering",
}
