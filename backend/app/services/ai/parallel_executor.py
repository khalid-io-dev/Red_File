import asyncio
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ParallelExecutor:
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def execute_parallel(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        async def run_task(task: Dict[str, Any]) -> Dict[str, Any]:
            async with self.semaphore:
                try:
                    tool = task['tool']
                    args = task['args']
                    result = await tool.execute(**args)
                    return {
                        'tool_name': tool.name,
                        'success': result.success,
                        'output': result.output,
                        'error': result.error,
                        'metadata': result.metadata
                    }
                except Exception as e:
                    logger.error(f"Task execution failed: {str(e)}")
                    return {
                        'tool_name': task.get('tool', {}).name if hasattr(task.get('tool'), 'name') else 'unknown',
                        'success': False,
                        'output': '',
                        'error': str(e),
                        'metadata': {}
                    }
        
        results = await asyncio.gather(*[run_task(task) for task in tasks])
        return results
