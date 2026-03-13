from typing import List, Dict, Any, AsyncGenerator, Optional
from .llm_service import OllamaLLMService
from .tools import registry
from .prompts.system import SECURITY_AGENT_PROMPT
from .memory import ConversationMemory
from .parallel_executor import ParallelExecutor
from .error_recovery import ErrorRecovery
from .tool_parser import ToolResultParser
import json
import logging

logger = logging.getLogger(__name__)

class SecurityAgent:
    def __init__(self, model: str = "huihui_ai/glm-4.7-flash-abliterated:q4_K"):
        self.llm = OllamaLLMService(model)
        self.tools = registry
        self.max_iterations = 10
        self.memory = ConversationMemory()
        self.parallel_executor = ParallelExecutor(max_concurrent=3)
        self.error_recovery = ErrorRecovery(max_retries=2)
    
    async def execute_task(
        self,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        stream: bool = False
    ) -> AsyncGenerator[Dict[str, Any], None]:
        self.memory.add_message("user", task)
        messages = self.memory.get_context_window()
        
        if context:
            context_str = f"\n\nContext:\n{json.dumps(context, indent=2)}"
            messages[0]["content"] += context_str
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            yield {"type": "iteration", "iteration": iteration}
            
            response = await self.llm.chat_with_tools(
                messages=messages,
                tools=self.tools.get_ollama_tools(),
                system=SECURITY_AGENT_PROMPT
            )
            
            logger.info(f"LLM Response: {response}")
            
            # Parse tool calls from text if not in structured format
            tool_calls = response.get('tool_calls')
            if not tool_calls and response.get('content'):
                # Try to extract JSON tool calls from content
                import re
                content = response['content'].strip()
                
                # Extract all JSON code blocks
                json_blocks = re.findall(r'```json\s*(.+?)\s*```', content, re.DOTALL)
                
                tool_calls = []
                for block in json_blocks:
                    # Handle multiple JSON objects in one block
                    for line in block.split('\n'):
                        line = line.strip()
                        if line and line.startswith('{'):
                            try:
                                tool_data = json.loads(line)
                                if 'name' in tool_data and 'arguments' in tool_data:
                                    tool_calls.append({
                                        'function': {
                                            'name': tool_data['name'],
                                            'arguments': tool_data['arguments']
                                        }
                                    })
                            except json.JSONDecodeError:
                                continue
                
                if tool_calls:
                    logger.info(f"Extracted {len(tool_calls)} tool calls from {len(json_blocks)} code blocks")
                else:
                    # Try raw JSON as fallback
                    json_match = re.search(r'^({.*})$', content, re.DOTALL)
                    if json_match:
                        try:
                            tool_data = json.loads(json_match.group(1))
                            if 'name' in tool_data and 'arguments' in tool_data:
                                tool_calls = [{
                                    'function': {
                                        'name': tool_data['name'],
                                        'arguments': tool_data['arguments']
                                    }
                                }]
                                logger.info(f"Extracted tool call from raw JSON")
                        except json.JSONDecodeError as e:
                            logger.error(f"Failed to parse tool JSON: {e}")
            
            if response.get('content'):
                yield {"type": "message", "content": response['content']}
                messages.append({"role": "assistant", "content": response['content']})
                self.memory.add_message("assistant", response['content'])
            
            if not tool_calls:
                logger.info("No tool calls detected, completing task")
                yield {"type": "complete", "message": "Task completed"}
                break
            
            for tool_call in tool_calls:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                
                yield {
                    "type": "tool_call",
                    "tool": tool_name,
                    "arguments": tool_args
                }
                
                tool = self.tools.get_tool(tool_name)
                if not tool:
                    logger.error(f"Tool {tool_name} not found")
                    yield {"type": "error", "error": f"Tool {tool_name} not found"}
                    continue
                
                logger.info(f"Executing tool {tool_name} with args: {tool_args}")
                result = await tool.execute(**tool_args)
                logger.info(f"Tool {tool_name} result: success={result.success}")
                
                parsed = ToolResultParser.parse(tool_name, result.output if result.success else "")
                
                self.memory.add_message("tool", result.output if result.success else result.error, {
                    "tool": tool_name,
                    "success": result.success,
                    "parsed": parsed
                })
                
                yield {
                    "type": "tool_result",
                    "tool": tool_name,
                    "success": result.success,
                    "output": result.output,
                    "error": result.error,
                    "parsed": parsed
                }
                
                messages.append({
                    "role": "tool",
                    "content": result.output if result.success else f"Error: {result.error}"
                })
            
            if iteration >= self.max_iterations:
                yield {"type": "max_iterations", "message": "Maximum iterations reached"}
                break
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = True
    ) -> AsyncGenerator[str, None]:
        if stream:
            async for chunk in self.llm.stream(
                messages=messages,
                system=SECURITY_AGENT_PROMPT,
                tools=self.tools.get_ollama_tools()
            ):
                yield chunk
        else:
            response = await self.llm.chat_with_tools(
                messages=messages,
                tools=self.tools.get_ollama_tools(),
                system=SECURITY_AGENT_PROMPT
            )
            yield response.get('content', '')
