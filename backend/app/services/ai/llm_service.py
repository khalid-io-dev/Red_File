import ollama
from typing import AsyncGenerator, Optional, Dict, Any, List
import json

class OllamaLLMService:
    def __init__(self, model: str = "huihui_ai/glm-4.7-flash-abliterated:q4_K"):
        self.model = model
        # Set longer timeout for GLM model
        timeout = 600 if 'glm' in model.lower() else 300
        self.client = ollama.AsyncClient(timeout=timeout)
        
        # Models that support function calling
        self.tool_supported_models = [
            "huihui_ai/glm-4.7-flash-abliterated:q4_K",
            "qwen2.5-coder:7b-instruct",
            "llama3.1:8b",
            "mistral:7b"
        ]
        
        self.supports_tools = any(supported in model for supported in self.tool_supported_models)
    
    async def generate(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        response = await self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature, "num_predict": max_tokens}
        )
        return response['message']['content']
    
    async def stream(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[str, None]:
        if system and messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": system})
        
        options = {"temperature": temperature}
        kwargs = {"model": self.model, "messages": messages, "options": options}
        
        if tools:
            kwargs["tools"] = tools
        
        stream = await self.client.chat(**kwargs, stream=True)
        
        async for chunk in stream:
            if chunk['message'].get('content'):
                yield chunk['message']['content']
            elif chunk['message'].get('tool_calls'):
                yield json.dumps({"tool_calls": chunk['message']['tool_calls']})
    
    async def chat_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        system: Optional[str] = None
    ) -> Dict[str, Any]:
        if system and messages[0].get("role") != "system":
            messages.insert(0, {"role": "system", "content": system})
        
        # If model doesn't support tools, fall back to text-based tool calling
        if not self.supports_tools:
            # Add tool descriptions to system prompt
            tool_descriptions = "\n\nAvailable tools:\n"
            for tool in tools:
                tool_descriptions += f"- {tool['function']['name']}: {tool['function']['description']}\n"
            tool_descriptions += "\nTo use a tool, respond with JSON in this format:\n{\"name\": \"tool_name\", \"arguments\": {\"param\": \"value\"}}"
            
            if messages[0].get("role") == "system":
                messages[0]["content"] += tool_descriptions
            else:
                messages.insert(0, {"role": "system", "content": system + tool_descriptions if system else tool_descriptions})
            
            response = await self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']
        
        # Use native tool support
        response = await self.client.chat(
            model=self.model,
            messages=messages,
            tools=tools
        )
        return response['message']
