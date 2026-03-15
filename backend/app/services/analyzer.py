import hashlib
import math
import pefile
import logging
import re
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class StaticAnalyzer:
    def calculate_hashes(self, file_content: bytes) -> Dict[str, str]:
        md5 = hashlib.md5(file_content).hexdigest()
        sha256 = hashlib.sha256(file_content).hexdigest()
        return {"md5": md5, "sha256": sha256}

    def calculate_entropy(self, file_content: bytes) -> float:
        if not file_content:
            return 0.0
        entropy = 0
        for x in range(256):
            p_x = float(file_content.count(x)) / len(file_content)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy
    
    def detect_file_type(self, file_content: bytes, filename: str) -> str:
        """Detect file type based on magic bytes and extension"""
        if len(file_content) < 4:
            return "Unknown"
        
        # Check magic bytes
        if file_content[:2] == b'MZ':
            return "PE32 Executable"
        elif file_content[:4] == b'\x7fELF':
            return "ELF Executable"
        elif file_content[:4] == b'\xca\xfe\xba\xbe':
            return "Mach-O Executable"
        elif file_content[:2] == b'#!':
            return "Shell Script"
        elif file_content[:4] == b'PK\x03\x04':
            return "ZIP Archive"
        elif file_content[:2] == b'\x1f\x8b':
            return "GZIP Archive"
        
        # Check by extension and content
        if filename.endswith('.py'):
            return "Python Script"
        elif filename.endswith('.js'):
            return "JavaScript File"
        elif filename.endswith('.sh'):
            return "Shell Script"
        elif filename.endswith(('.exe', '.dll')):
            return "PE32 Executable"
        
        return "Unknown"

    def analyze_pe(self, file_content: bytes) -> Dict[str, Any]:
        try:
            pe = pefile.PE(data=file_content)
            
            # Extract imports
            imports = []
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    imports.append(entry.dll.decode())
            
            # Extract sections
            sections = []
            for section in pe.sections:
                sections.append({
                    "name": section.Name.decode().strip('\x00'),
                    "virtual_size": section.Misc_VirtualSize,
                    "entropy": section.get_entropy()
                })
            
            return {
                "is_pe": True,
                "sections": sections,
                "section_count": len(pe.sections),
                "imports": imports,
                "import_count": len(imports),
                "entry_point": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
                "machine": hex(pe.FILE_HEADER.Machine),
                "timestamp": pe.FILE_HEADER.TimeDateStamp
            }
        except Exception as e:
            return {"is_pe": False, "error": str(e)}
    
    def analyze_script(self, file_content: bytes, file_type: str) -> Dict[str, Any]:
        """Analyze script files for suspicious patterns"""
        try:
            content = file_content.decode('utf-8', errors='ignore')
        except:
            return {"is_script": False}
        
        suspicious_patterns = {
            "shellcode": [r'\\x[0-9a-fA-F]{2}', r'0x[0-9a-fA-F]{2}'],
            "obfuscation": [r'eval\(', r'exec\(', r'base64\.b64decode'],
            "network": [r'socket\.', r'urllib', r'requests\.', r'http://'],
            "file_ops": [r'open\(', r'write\(', r'os\.system', r'subprocess'],
            "crypto": [r'AES', r'RSA', r'encrypt', r'decrypt'],
            "registry": [r'winreg', r'HKEY_', r'RegOpenKey'],
        }
        
        findings = {}
        for category, patterns in suspicious_patterns.items():
            matches = []
            for pattern in patterns:
                found = re.findall(pattern, content, re.IGNORECASE)
                if found:
                    matches.extend(found[:5])  # Limit to 5 matches per pattern
            if matches:
                findings[category] = matches
        
        return {
            "is_script": True,
            "language": file_type,
            "line_count": content.count('\n'),
            "suspicious_patterns": findings,
            "has_shellcode": "shellcode" in findings,
            "has_obfuscation": "obfuscation" in findings,
            "has_network": "network" in findings
        }

    def scan_yara(self, file_content: bytes) -> List[str]:
        """Scan for malicious patterns"""
        matches = []
        
        # Check for PE files
        if file_content[:2] == b'MZ':
            matches.append("PE_File")
        
        # Check for shellcode patterns
        shellcode_patterns = [b'\x90' * 10, b'\xcc', b'\x31\xc0', b'\x31\xdb']
        for pattern in shellcode_patterns:
            if pattern in file_content:
                matches.append("Shellcode_Pattern")
                break
        
        # Check for suspicious strings
        suspicious_strings = [b'cmd.exe', b'powershell', b'CreateRemoteThread', b'VirtualAlloc']
        for string in suspicious_strings:
            if string in file_content:
                matches.append(f"Suspicious_String_{string.decode()}")
        
        return matches

    def calculate_risk_score(self, features: Dict[str, Any], entropy: float, yara_matches: List[str]) -> int:
        """Calculate risk score from 0-10"""
        score = 0
        
        # High entropy = possible encryption/packing
        if entropy > 7.5:
            score += 3
        elif entropy > 7.0:
            score += 2
        elif entropy > 6.5:
            score += 1
        
        # PE file analysis
        if features.get("is_pe"):
            score += 1
            if features.get("import_count", 0) > 50:
                score += 1
        
        # Script analysis
        if features.get("is_script"):
            if features.get("has_shellcode"):
                score += 3
            if features.get("has_obfuscation"):
                score += 2
            if features.get("has_network"):
                score += 1
        
        # YARA matches
        score += min(len(yara_matches), 3)
        
        return min(10, score)

    def analyze(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        hashes = self.calculate_hashes(file_content)
        entropy = self.calculate_entropy(file_content)
        file_type = self.detect_file_type(file_content, filename)
        
        # Perform appropriate analysis based on file type
        if "PE32" in file_type or "Executable" in file_type:
            static_features = self.analyze_pe(file_content)
        elif "Script" in file_type:
            static_features = self.analyze_script(file_content, file_type)
        else:
            static_features = {"is_pe": False, "is_script": False}
        
        yara_matches = self.scan_yara(file_content)
        risk_score = self.calculate_risk_score(static_features, entropy, yara_matches)
        
        return {
            "filename": filename,
            "md5": hashes["md5"],
            "sha256": hashes["sha256"],
            "file_size": len(file_content),
            "file_type": file_type,
            "entropy": round(entropy, 4),
            "yara_matches": yara_matches,
            "static_features": static_features,
            "risk_score": risk_score
        }

analyzer = StaticAnalyzer()
