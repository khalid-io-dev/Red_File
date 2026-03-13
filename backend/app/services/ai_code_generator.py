import aiohttp
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AICodeGenerator:
    """Generate and fix code using AI models"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.model = "qwen2.5-coder:7b"
    
    async def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate code using AI model"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9
                    }
                }
                
                async with session.post(self.ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=60)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("response", "# Code generation failed")
                    else:
                        logger.error(f"Ollama API error: {response.status}")
                        return self._fallback_code(language)
        except Exception as e:
            logger.error(f"Code generation error: {e}")
            return self._fallback_code(language)
    
    def _fallback_code(self, language: str) -> str:
        """Fallback code when AI is unavailable"""
        templates = {
            "python": '''#!/usr/bin/env python3
import requests
import sys

def exploit(target):
    """Custom exploit implementation"""
    try:
        response = requests.get(f"http://{target}")
        print(f"[+] Target responded: {response.status_code}")
        return True
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python exploit.py <target>")
        sys.exit(1)
    
    target = sys.argv[1]
    exploit(target)
''',
            "ruby": '''#!/usr/bin/env ruby
require 'net/http'

def exploit(target)
  uri = URI("http://#{target}")
  response = Net::HTTP.get_response(uri)
  puts "[+] Target responded: #{response.code}"
rescue => e
  puts "[-] Error: #{e.message}"
end

if ARGV.length < 1
  puts "Usage: ruby exploit.rb <target>"
  exit 1
end

exploit(ARGV[0])
''',
            "javascript": '''const axios = require('axios');

async function exploit(target) {
    try {
        const response = await axios.get(`http://${target}`);
        console.log(`[+] Target responded: ${response.status}`);
        return true;
    } catch (error) {
        console.log(`[-] Error: ${error.message}`);
        return false;
    }
}

if (process.argv.length < 3) {
    console.log('Usage: node exploit.js <target>');
    process.exit(1);
}

exploit(process.argv[2]);
'''
        }
        return templates.get(language, templates["python"])

ai_code_generator = AICodeGenerator()
