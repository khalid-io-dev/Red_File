from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)

class ToolParameter(BaseModel):
    name: str
    type: str
    description: str
    required: bool = True
    enum: Optional[List[str]] = None

class ToolResult(BaseModel):
    success: bool
    output: str
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BaseTool(ABC):
    def __init__(self):
        self.name = self.__class__.__name__.replace("Tool", "").lower()
        self.logger = logging.getLogger(f"tools.{self.name}")
    
    @abstractmethod
    def get_description(self) -> str:
        pass
    
    @abstractmethod
    def get_parameters(self) -> List[ToolParameter]:
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        pass
    
    def to_ollama_tool(self) -> Dict[str, Any]:
        properties = {}
        required = []
        
        for param in self.get_parameters():
            prop = {
                "type": param.type,
                "description": param.description
            }
            if param.enum:
                prop["enum"] = param.enum
            properties[param.name] = prop
            if param.required:
                required.append(param.name)
        
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.get_description(),
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
    
    def validate_params(self, **kwargs) -> bool:
        required_params = [p.name for p in self.get_parameters() if p.required]
        for param in required_params:
            if param not in kwargs:
                raise ValueError(f"Missing required parameter: {param}")
        return True
