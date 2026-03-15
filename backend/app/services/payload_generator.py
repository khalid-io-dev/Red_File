import requests
import json
from typing import Dict, Optional

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_MODEL = "f0rc3ps/nu11secur1tyAIRedTeam:latest"


class PayloadGenerator:
    """Generate payloads using Ollama AI model"""
    
    def __init__(self):
        self.model = OLLAMA_MODEL
    
    def check_ollama_status(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def generate_payload(
        self,
        payload_type: str,
        lhost: str,
        lport: str,
        format: str = "python"
    ) -> Dict:
        """Generate a payload using Ollama"""
        
        # Build the prompt based on payload type
        prompts = {
            "reverse_tcp": f"""Generate a Python reverse TCP shell payload that connects to {lhost}:{lport}.
Return ONLY the code, no explanations. Use socket, subprocess, and os modules.
The payload should be in {format} format.""",
            
            "reverse_https": f"""Generate a Python reverse HTTPS shell payload that connects to {lhost}:{lport} over HTTPS.
Use requests library with SSL verification disabled.
The payload should be in {format} format.""",
            
            "reverse_http": f"""Generate a Python reverse HTTP shell payload that connects to {lhost}:{lport}.
The payload should be in {format} format.""",
            
            "bind_tcp": f"""Generate a Python bind TCP shell payload that listens on port {lport}.
Return ONLY the code, no explanations.
The payload should be in {format} format.""",
            
            "meterpreter": f"""Generate a Python Meterpreter-like reverse TCP shell that connects to {lhost}:{lport}.
Include basic meterpreter-like commands.
The payload should be in {format} format.""",
            
            "shell": f"""Generate a simple Python shell that connects to {lhost}:{lport}.
Return ONLY the code, no explanations.
The payload should be in {format} format."""
        }
        
        prompt = prompts.get(payload_type, prompts["reverse_tcp"])
        
        try:
            # Call Ollama API
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "payload": result.get("response", ""),
                    "type": payload_type,
                    "format": format,
                    "lhost": lhost,
                    "lport": lport
                }
            else:
                return {
                    "success": False,
                    "error": f"Ollama API error: {response.status_code}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot connect to Ollama. Make sure Ollama is running on localhost:11434"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


payload_generator = PayloadGenerator()
