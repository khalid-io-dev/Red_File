import aiohttp
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class AIChatService:
    """AI Chat service with multiple model support and prompt enhancement"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            "qwen2.5-coder:7b-instruct": "Code-focused AI assistant",
            "deepseek-coder:6.7b-instruct": "Advanced coding assistant", 
            "huihui_ai/glm-4.7-flash-abliterated:q4_K": "Fast general-purpose AI"
        }
    
    async def enhance_prompt(self, user_prompt: str) -> str:
        """Enhance user prompt using AI"""
        try:
            enhancement_prompt = f"""Enhance this user prompt to be more specific and effective for an AI assistant:

Original: {user_prompt}

Enhanced version (return only the enhanced prompt):"""

            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": "qwen2.5-coder:7b-instruct",
                    "prompt": enhancement_prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                }
                
                async with session.post(self.ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
                    if response.status == 200:
                        data = await response.json()
                        enhanced = data.get("response", user_prompt).strip()
                        return enhanced if enhanced else user_prompt
                    return user_prompt
        except Exception as e:
            logger.error(f"Prompt enhancement failed: {e}")
            return user_prompt
    
    async def chat_with_model(self, model_name: str, messages: List[Dict[str, str]], enhanced_prompt: Optional[str] = None) -> str:
        """Chat with selected AI model"""
        try:
            # Check if Ollama is available first
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get("http://localhost:11434/api/tags", timeout=aiohttp.ClientTimeout(total=5)) as test_response:
                        if test_response.status != 200:
                            return "Ollama service is not available. Please start Ollama first."
                except:
                    return "Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434"
            
            # Build conversation context
            context = ""
            for msg in messages[:-1]:  # All except last message
                context += f"{msg['role'].title()}: {msg['content']}\n"
            
            # Use enhanced prompt if available, otherwise use original
            final_prompt = enhanced_prompt or messages[-1]['content']
            context += f"User: {final_prompt}\nAssistant:"
            
            # Set timeout to 7 minutes for all models
            timeout = 420
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model_name,
                    "prompt": context,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 2000
                    }
                }
                
                async with session.post(self.ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=timeout)) as response:
                    if response.status == 200:
                        data = await response.json()
                        response_text = data.get("response", "I'm sorry, I couldn't generate a response.")
                        # Clean up HTML entities
                        response_text = response_text.replace("&#39;", "'").replace("&quot;", '"').replace("&amp;", "&")
                        return response_text
                    else:
                        return f"Model returned status {response.status}. Please check if the model '{model_name}' is installed in Ollama."
        except asyncio.TimeoutError:
            return f"Request timed out. The model '{model_name}' is taking too long to respond. Try a simpler question or use a faster model."
        except Exception as e:
            logger.error(f"Chat with model {model_name} failed: {e}")
            return f"Connection error: Please ensure Ollama is running and the model '{model_name}' is available."
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of available models"""
        return self.models

ai_chat_service = AIChatService()