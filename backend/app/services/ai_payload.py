import ollama
import logging
import asyncio
from typing import Optional, Dict, List
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
executor = ThreadPoolExecutor(max_workers=2)

class AIPayloadGenerator:
    """Enhanced AI Payload Generator with installed model detection"""
    
    def __init__(self, model_name: str = "f0rc3ps/nu11secur1tyAIRedTeam:latest"):
        self.model_name = model_name
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of actually installed models from Ollama"""
        try:
            logger.info("Fetching models from Ollama...")
            models_response = ollama.list()
            
            installed_models = {}
            models_list = models_response.get('models', [])
            
            for model in models_list:
                model_name = model.get('name', '')
                if model_name:
                    installed_models[model_name] = model_name
            
            if not installed_models:
                logger.warning("No models found, using fallback")
                return {
                    "f0rc3ps/nu11secur1tyAIRedTeam:latest": "f0rc3ps/nu11secur1tyAIRedTeam:latest",
                    "thirdeyeai/DeepSeek-R1-Distill-Qwen-7B-uncensored:Q8_0": "thirdeyeai/DeepSeek-R1-Distill-Qwen-7B-uncensored:Q8_0"
                }
            
            logger.info(f"Returning {len(installed_models)} models")
            return installed_models
            
        except Exception as e:
            logger.error(f"Failed to fetch models: {e}", exc_info=True)
            return {
                "f0rc3ps/nu11secur1tyAIRedTeam:latest": "f0rc3ps/nu11secur1tyAIRedTeam:latest",
                "thirdeyeai/DeepSeek-R1-Distill-Qwen-7B-uncensored:Q8_0": "thirdeyeai/DeepSeek-R1-Distill-Qwen-7B-uncensored:Q8_0"
            }
    
    def _create_system_prompt(self) -> str:
        """Create system prompt for payload generation"""
        return """You are an expert offensive security engineer and exploit developer.
Your task is to generate functional, production-ready payloads for authorized penetration testing.

CRITICAL RULES:
1. Generate ONLY executable code - no explanations, no markdown formatting
2. Code must be syntactically correct and ready to run
3. Handle errors gracefully with try-catch blocks
4. Make code as stealthy as possible
5. Include proper connection handling and retries
6. Use appropriate encoding/obfuscation where needed
7. Follow security best practices for the target platform

Output ONLY the raw code, nothing else."""

    def _create_payload_prompt(self, payload_type: str, platform: str, language: str, 
                               lhost: str, lport: int, encoder: Optional[str] = None) -> str:
        """Create specific prompt for payload generation"""
        
        encoder_instruction = ""
        if encoder and encoder != "none":
            encoder_instruction = f"\nApply {encoder} encoding/obfuscation to evade detection."
        
        prompts = {
            "reverse_shell": f"""Generate a {language} reverse shell for {platform} that:
- Connects to {lhost}:{lport}
- Provides interactive shell access
- Handles connection failures with retry logic
- Runs silently without console windows (if applicable)
- Uses native system calls where possible{encoder_instruction}""",
            
            "bind_shell": f"""Generate a {language} bind shell for {platform} that:
- Listens on port {lport}
- Accepts incoming connections
- Provides interactive shell access
- Handles multiple connection attempts
- Runs as a background service{encoder_instruction}""",
            
            "meterpreter": f"""Generate a {language} meterpreter-style payload for {platform} that:
- Connects to {lhost}:{lport}
- Implements staged payload architecture
- Supports command execution
- Includes file upload/download capabilities
- Has process migration features{encoder_instruction}""",
            
            "web_shell": f"""Generate a {language} web shell for {platform} that:
- Accepts commands via HTTP parameters
- Executes system commands
- Returns output in HTTP response
- Includes authentication (password: admin123)
- Has file management capabilities{encoder_instruction}"""
        }
        
        return prompts.get(payload_type, prompts["reverse_shell"])

    async def generate_payload_async(self, payload_type: str, platform: str, language: str, 
                        lhost: str, lport: int, encoder: Optional[str] = None,
                        model: Optional[str] = None) -> Dict[str, str]:
        """Generate payload using AI model with async timeout"""
        
        model_to_use = model if model else self.model_name
        logger.info(f"Generating {payload_type} with model {model_to_use}")
        
        system_prompt = self._create_system_prompt()
        payload_prompt = self._create_payload_prompt(
            payload_type, platform, language, lhost, lport, encoder
        )
        
        full_prompt = f"{system_prompt}\n\n{payload_prompt}"
        
        try:
            logger.info(f"Calling ollama.generate with model {model_to_use}")
            
            # Run in thread pool with 10 minute timeout
            response = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    executor,
                    lambda: ollama.generate(
                        model=model_to_use,
                        prompt=full_prompt,
                        stream=False,
                        options={"temperature": 0.7, "top_p": 0.9, "top_k": 40}
                    )
                ),
                timeout=600
            )
            
            logger.info(f"Got response from ollama")
            content = response.get('response', '')
            
            if not content:
                logger.error("Empty response from ollama")
                raise ValueError("Empty response from model")
            
            code = self._extract_code(content, language)
            
            if not code or len(code.strip()) < 10:
                logger.error(f"Generated code too short: {len(code)} chars")
                raise ValueError("Generated code is too short")
            
            logger.info(f"Generated {len(code)} chars with {model_to_use}")
            return {"code": code, "model": model_to_use, "language": language, "platform": platform}
            
        except asyncio.TimeoutError:
            logger.error(f"Timeout waiting for {model_to_use} response (>10 min)")
            raise Exception(f"Model {model_to_use} took too long to respond (>10 minutes)")
        except Exception as e:
            logger.error(f"AI generation failed: {e}", exc_info=True)
            raise Exception(f"AI payload generation failed: {str(e)}")
    
    def _extract_code(self, content: str, language: str) -> str:
        """Extract code from AI response, removing markdown formatting"""
        
        if "```" in content:
            parts = content.split("```")
            if len(parts) >= 3:
                code = parts[1]
            elif len(parts) == 2:
                code = parts[1]
            else:
                code = content
            
            lines = code.strip().split('\n')
            if lines and lines[0].strip().lower() in ['python', 'powershell', 'bash', 'c', 'cpp', 'php', 'java', 'javascript']:
                code = '\n'.join(lines[1:])
            else:
                code = '\n'.join(lines)
        else:
            code = content
        
        return code.strip()

# Global instance
ai_payload_generator = AIPayloadGenerator()
