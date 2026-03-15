from typing import List, Dict
import json

class MITREMapper:
    """Map tools and findings to MITRE ATT&CK framework"""
    
    def __init__(self):
        self.attack_data = self._load_attack_data()
    
    def _load_attack_data(self) -> Dict:
        """Load MITRE ATT&CK data"""
        return {
            "tactics": {
                "TA0001": {"name": "Initial Access", "techniques": ["T1190", "T1133", "T1078"]},
                "TA0002": {"name": "Execution", "techniques": ["T1059", "T1203"]},
                "TA0003": {"name": "Persistence", "techniques": ["T1053", "T1136"]},
                "TA0004": {"name": "Privilege Escalation", "techniques": ["T1068", "T1055"]},
                "TA0005": {"name": "Defense Evasion", "techniques": ["T1027", "T1140"]},
                "TA0006": {"name": "Credential Access", "techniques": ["T1110", "T1003"]},
                "TA0007": {"name": "Discovery", "techniques": ["T1046", "T1087"]},
                "TA0008": {"name": "Lateral Movement", "techniques": ["T1021"]},
                "TA0009": {"name": "Collection", "techniques": ["T1005"]},
                "TA0010": {"name": "Exfiltration", "techniques": ["T1041"]},
                "TA0011": {"name": "Command and Control", "techniques": ["T1071"]}
            },
            "techniques": {
                "T1190": {"name": "Exploit Public-Facing Application", "tactic": "TA0001", "tools": ["sqlmap", "nikto", "nuclei"]},
                "T1133": {"name": "External Remote Services", "tactic": "TA0001", "tools": ["hydra", "ssh"]},
                "T1078": {"name": "Valid Accounts", "tactic": "TA0001", "tools": ["hydra", "john", "hashcat"]},
                "T1059": {"name": "Command and Scripting Interpreter", "tactic": "TA0002", "tools": ["metasploit", "custom_exploit"]},
                "T1203": {"name": "Exploitation for Client Execution", "tactic": "TA0002", "tools": ["metasploit"]},
                "T1053": {"name": "Scheduled Task/Job", "tactic": "TA0003", "tools": []},
                "T1136": {"name": "Create Account", "tactic": "TA0003", "tools": []},
                "T1068": {"name": "Exploitation for Privilege Escalation", "tactic": "TA0004", "tools": ["metasploit"]},
                "T1055": {"name": "Process Injection", "tactic": "TA0004", "tools": []},
                "T1027": {"name": "Obfuscated Files or Information", "tactic": "TA0005", "tools": ["payload_generator"]},
                "T1140": {"name": "Deobfuscate/Decode Files or Information", "tactic": "TA0005", "tools": []},
                "T1110": {"name": "Brute Force", "tactic": "TA0006", "tools": ["hydra", "john", "hashcat"]},
                "T1003": {"name": "OS Credential Dumping", "tactic": "TA0006", "tools": []},
                "T1046": {"name": "Network Service Scanning", "tactic": "TA0007", "tools": ["nmap", "masscan"]},
                "T1087": {"name": "Account Discovery", "tactic": "TA0007", "tools": ["enum4linux"]},
                "T1021": {"name": "Remote Services", "tactic": "TA0008", "tools": ["ssh", "rdp"]},
                "T1005": {"name": "Data from Local System", "tactic": "TA0009", "tools": []},
                "T1041": {"name": "Exfiltration Over C2 Channel", "tactic": "TA0010", "tools": []},
                "T1071": {"name": "Application Layer Protocol", "tactic": "TA0011", "tools": []}
            }
        }
    
    def map_technique(self, tool_name: str, output: str = "") -> List[str]:
        """Map tool to MITRE ATT&CK techniques"""
        techniques = []
        
        # Direct tool mapping
        for tech_id, tech_data in self.attack_data["techniques"].items():
            if tool_name.lower() in [t.lower() for t in tech_data["tools"]]:
                techniques.append(tech_id)
        
        # Output-based mapping
        if output:
            if "sql injection" in output.lower():
                techniques.append("T1190")
            if "brute force" in output.lower() or "password" in output.lower():
                techniques.append("T1110")
            if "port" in output.lower() and "open" in output.lower():
                techniques.append("T1046")
        
        return list(set(techniques))
    
    def get_tactics(self) -> List[Dict]:
        """Get all tactics"""
        return [
            {"id": tactic_id, "name": tactic_data["name"], "techniques": tactic_data["techniques"]}
            for tactic_id, tactic_data in self.attack_data["tactics"].items()
        ]
    
    def get_techniques(self, tactic: str = None) -> List[Dict]:
        """Get techniques, optionally filtered by tactic"""
        techniques = []
        
        for tech_id, tech_data in self.attack_data["techniques"].items():
            if tactic is None or tech_data["tactic"] == tactic:
                techniques.append({
                    "id": tech_id,
                    "name": tech_data["name"],
                    "tactic": tech_data["tactic"],
                    "tools": tech_data["tools"]
                })
        
        return techniques
    
    def get_technique_details(self, technique_id: str) -> Dict:
        """Get detailed information about a technique"""
        tech_data = self.attack_data["techniques"].get(technique_id)
        
        if not tech_data:
            return {"error": "Technique not found"}
        
        tactic_id = tech_data["tactic"]
        tactic_name = self.attack_data["tactics"][tactic_id]["name"]
        
        return {
            "id": technique_id,
            "name": tech_data["name"],
            "tactic_id": tactic_id,
            "tactic_name": tactic_name,
            "tools": tech_data["tools"],
            "description": f"MITRE ATT&CK technique {technique_id}: {tech_data['name']}"
        }
    
    def map_finding_to_technique(self, finding: Dict) -> str:
        """Map a finding to MITRE technique"""
        tool = finding.get("tool", "").lower()
        title = finding.get("title", "").lower()
        description = finding.get("description", "").lower()
        
        # Map based on tool
        techniques = self.map_technique(tool)
        if techniques:
            return techniques[0]
        
        # Map based on finding content
        if "sql injection" in title or "sql injection" in description:
            return "T1190"
        elif "brute force" in title or "password" in title:
            return "T1110"
        elif "port" in title and "open" in title:
            return "T1046"
        elif "credential" in title:
            return "T1078"
        elif "privilege" in title:
            return "T1068"
        
        return "T1190"  # Default to exploit public-facing application
    
    def generate_attack_matrix(self, findings: List[Dict]) -> Dict:
        """Generate attack matrix from findings"""
        matrix = {
            "tactics": {},
            "techniques": {},
            "coverage": 0
        }
        
        # Initialize tactics
        for tactic_id, tactic_data in self.attack_data["tactics"].items():
            matrix["tactics"][tactic_id] = {
                "name": tactic_data["name"],
                "techniques_used": [],
                "count": 0
            }
        
        # Map findings to techniques
        for finding in findings:
            tech_id = self.map_finding_to_technique(finding)
            
            if tech_id not in matrix["techniques"]:
                tech_data = self.attack_data["techniques"].get(tech_id, {})
                matrix["techniques"][tech_id] = {
                    "name": tech_data.get("name", "Unknown"),
                    "count": 0,
                    "findings": []
                }
            
            matrix["techniques"][tech_id]["count"] += 1
            matrix["techniques"][tech_id]["findings"].append(finding.get("title", ""))
            
            # Update tactic
            tech_data = self.attack_data["techniques"].get(tech_id, {})
            tactic_id = tech_data.get("tactic")
            if tactic_id and tactic_id in matrix["tactics"]:
                if tech_id not in matrix["tactics"][tactic_id]["techniques_used"]:
                    matrix["tactics"][tactic_id]["techniques_used"].append(tech_id)
                matrix["tactics"][tactic_id]["count"] += 1
        
        # Calculate coverage
        total_techniques = len(self.attack_data["techniques"])
        used_techniques = len(matrix["techniques"])
        matrix["coverage"] = (used_techniques / total_techniques) * 100 if total_techniques > 0 else 0
        
        return matrix
    
    def suggest_next_techniques(self, current_techniques: List[str]) -> List[Dict]:
        """Suggest next techniques based on current position"""
        suggestions = []
        
        # Get tactics of current techniques
        current_tactics = set()
        for tech_id in current_techniques:
            tech_data = self.attack_data["techniques"].get(tech_id, {})
            if tech_data:
                current_tactics.add(tech_data["tactic"])
        
        # Suggest techniques from next logical tactics
        tactic_order = ["TA0001", "TA0002", "TA0003", "TA0004", "TA0005", "TA0006", "TA0007", "TA0008", "TA0009", "TA0010", "TA0011"]
        
        for tactic_id in tactic_order:
            if tactic_id not in current_tactics:
                tactic_data = self.attack_data["tactics"][tactic_id]
                for tech_id in tactic_data["techniques"][:2]:  # Suggest top 2
                    tech_data = self.attack_data["techniques"].get(tech_id, {})
                    suggestions.append({
                        "technique_id": tech_id,
                        "technique_name": tech_data.get("name", ""),
                        "tactic_name": tactic_data["name"],
                        "tools": tech_data.get("tools", [])
                    })
                break
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def export_navigator_layer(self, findings: List[Dict]) -> Dict:
        """Export ATT&CK Navigator layer"""
        matrix = self.generate_attack_matrix(findings)
        
        techniques = []
        for tech_id, tech_data in matrix["techniques"].items():
            techniques.append({
                "techniqueID": tech_id,
                "score": tech_data["count"],
                "color": "#ff6666" if tech_data["count"] > 5 else "#ffaa66",
                "comment": f"Found {tech_data['count']} times"
            })
        
        return {
            "name": "SecureSight Attack Coverage",
            "versions": {
                "attack": "12",
                "navigator": "4.8",
                "layer": "4.4"
            },
            "domain": "enterprise-attack",
            "description": "Attack techniques identified by SecureSight",
            "techniques": techniques
        }

# Singleton instance
mitre_mapper = MITREMapper()
