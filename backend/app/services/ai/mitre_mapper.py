from typing import Dict, List, Set
import json

# MITRE ATT&CK Technique Mapping
MITRE_MAPPING = {
    # Reconnaissance
    'nmap': ['T1046', 'T1595.001'],  # Network Service Discovery, Active Scanning
    'portscan': ['T1046'],
    'dnsenum': ['T1590.002'],  # Gather Victim Network Information: DNS
    'theharvester': ['T1589', 'T1590'],  # Gather Victim Identity/Network Information
    'webrecon': ['T1592', 'T1590'],  # Gather Victim Host/Network Information
    'gobuster': ['T1595.003'],  # Wordlist Scanning
    'ssl_analyzer': ['T1590.001'],  # Domain Properties
    
    # Initial Access
    'sqlmap': ['T1190'],  # Exploit Public-Facing Application
    'custom_exploit': ['T1190', 'T1059'],  # Exploit Public-Facing Application, Command Injection
    'hydra': ['T1110.001'],  # Brute Force: Password Guessing
    'wpscan': ['T1190'],
    
    # Execution
    'nuclei': ['T1059'],  # Command and Scripting Interpreter
    'nikto': ['T1190'],
    
    # Credential Access
    'john': ['T1110.002'],  # Brute Force: Password Cracking
    'hashcat': ['T1110.002'],
}

TECHNIQUE_INFO = {
    'T1046': {'name': 'Network Service Discovery', 'tactic': 'Discovery'},
    'T1595.001': {'name': 'Active Scanning: Scanning IP Blocks', 'tactic': 'Reconnaissance'},
    'T1590.002': {'name': 'Gather Victim Network Information: DNS', 'tactic': 'Reconnaissance'},
    'T1589': {'name': 'Gather Victim Identity Information', 'tactic': 'Reconnaissance'},
    'T1590': {'name': 'Gather Victim Network Information', 'tactic': 'Reconnaissance'},
    'T1592': {'name': 'Gather Victim Host Information', 'tactic': 'Reconnaissance'},
    'T1595.003': {'name': 'Active Scanning: Wordlist Scanning', 'tactic': 'Reconnaissance'},
    'T1590.001': {'name': 'Gather Victim Network Information: Domain Properties', 'tactic': 'Reconnaissance'},
    'T1190': {'name': 'Exploit Public-Facing Application', 'tactic': 'Initial Access'},
    'T1059': {'name': 'Command and Scripting Interpreter', 'tactic': 'Execution'},
    'T1110.001': {'name': 'Brute Force: Password Guessing', 'tactic': 'Credential Access'},
    'T1110.002': {'name': 'Brute Force: Password Cracking', 'tactic': 'Credential Access'},
}

class MITREMapper:
    def __init__(self):
        self.mapping = MITRE_MAPPING
        self.technique_info = TECHNIQUE_INFO
        self.used_techniques: Set[str] = set()
    
    def get_technique(self, tool_name: str) -> List[str]:
        return self.mapping.get(tool_name, [])
    
    def get_technique_info(self, technique_id: str) -> Dict:
        return self.technique_info.get(technique_id, {'name': 'Unknown', 'tactic': 'Unknown'})
    
    def track_tool_usage(self, tool_name: str):
        techniques = self.get_technique(tool_name)
        self.used_techniques.update(techniques)
    
    def get_coverage(self, tools_used: List[str]) -> Dict:
        techniques = set()
        tactics = set()
        
        for tool in tools_used:
            tool_techniques = self.get_technique(tool)
            techniques.update(tool_techniques)
            
            for tech in tool_techniques:
                info = self.get_technique_info(tech)
                tactics.add(info['tactic'])
        
        total_techniques = len(self.technique_info)
        coverage_percent = (len(techniques) / total_techniques * 100) if total_techniques > 0 else 0
        
        return {
            'techniques_used': list(techniques),
            'tactics_covered': list(tactics),
            'total_techniques': len(techniques),
            'coverage_percent': round(coverage_percent, 2),
            'technique_details': [
                {
                    'id': tech,
                    'name': self.get_technique_info(tech)['name'],
                    'tactic': self.get_technique_info(tech)['tactic']
                }
                for tech in techniques
            ]
        }
    
    def suggest_next_technique(self, current_techniques: List[str]) -> Dict:
        current_tactics = set()
        for tech in current_techniques:
            info = self.get_technique_info(tech)
            current_tactics.add(info['tactic'])
        
        # Attack kill chain order
        kill_chain = [
            'Reconnaissance',
            'Initial Access',
            'Execution',
            'Persistence',
            'Privilege Escalation',
            'Defense Evasion',
            'Credential Access',
            'Discovery',
            'Lateral Movement',
            'Collection',
            'Exfiltration',
            'Impact'
        ]
        
        # Find next tactic in kill chain
        for tactic in kill_chain:
            if tactic not in current_tactics:
                # Find techniques for this tactic
                suggested = []
                for tech_id, info in self.technique_info.items():
                    if info['tactic'] == tactic:
                        # Find tools that implement this technique
                        tools = [tool for tool, techs in self.mapping.items() if tech_id in techs]
                        if tools:
                            suggested.append({
                                'technique': tech_id,
                                'name': info['name'],
                                'tactic': tactic,
                                'tools': tools
                            })
                
                if suggested:
                    return {
                        'next_tactic': tactic,
                        'suggested_techniques': suggested[:3]  # Top 3
                    }
        
        return {'next_tactic': None, 'suggested_techniques': []}
    
    def generate_attack_matrix(self, tools_used: List[str]) -> Dict:
        matrix = {}
        
        for tool in tools_used:
            techniques = self.get_technique(tool)
            for tech in techniques:
                info = self.get_technique_info(tech)
                tactic = info['tactic']
                
                if tactic not in matrix:
                    matrix[tactic] = []
                
                matrix[tactic].append({
                    'technique': tech,
                    'name': info['name'],
                    'tool': tool
                })
        
        return matrix
    
    def export_navigator_layer(self, tools_used: List[str]) -> Dict:
        """Export ATT&CK Navigator layer JSON"""
        techniques = []
        
        for tool in tools_used:
            tool_techniques = self.get_technique(tool)
            for tech in tool_techniques:
                info = self.get_technique_info(tech)
                techniques.append({
                    'techniqueID': tech,
                    'tactic': info['tactic'].lower().replace(' ', '-'),
                    'color': '#ff6666',
                    'comment': f'Tool: {tool}',
                    'enabled': True
                })
        
        return {
            'name': 'SecureSight Attack Coverage',
            'versions': {'attack': '14', 'navigator': '4.9', 'layer': '4.5'},
            'domain': 'enterprise-attack',
            'description': 'Attack techniques used in SecureSight assessment',
            'techniques': techniques
        }

# Global instance
mitre_mapper = MITREMapper()
