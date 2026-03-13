from typing import List, Dict, Any
from app.services.ai.llm_service import OllamaLLMService
from app.services.ai.tools import registry
import asyncio
import logging

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, name: str, tools: List[str], model: str = "qwen2.5-coder:7b-instruct"):
        self.name = name
        self.tool_names = tools
        self.llm = OllamaLLMService(model)
        self.results = {}
    
    def get_tools(self):
        return [registry.get_tool(name) for name in self.tool_names if registry.get_tool(name)]
    
    async def run_tool(self, tool_name: str, params: dict) -> Dict[str, Any]:
        tool = registry.get_tool(tool_name)
        if not tool:
            return {'success': False, 'error': 'Tool not found'}
        
        try:
            result = await tool.execute(**params)
            return {'success': result.success, 'output': result.output, 'error': result.error}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    async def parallel_run(self, tasks: List[tuple]) -> Dict[str, Any]:
        results = {}
        
        async def run_task(tool_name, params):
            return tool_name, await self.run_tool(tool_name, params)
        
        task_list = [run_task(tool_name, params) for tool_name, params in tasks]
        completed = await asyncio.gather(*task_list, return_exceptions=True)
        
        for item in completed:
            if isinstance(item, Exception):
                continue
            tool_name, result = item
            results[tool_name] = result
        
        return results
    
    async def execute(self, target: str) -> Dict[str, Any]:
        raise NotImplementedError()
