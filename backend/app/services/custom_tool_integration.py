from typing import Dict, List, Callable
import asyncio

class CustomToolIntegration:
    """Framework for integrating custom security tools"""
    
    def __init__(self):
        self.registered_tools = {}
        self.tool_categories = {
            "scanner": [],
            "exploit": [],
            "recon": [],
            "post_exploit": [],
            "analysis": []
        }
    
    def register_tool(self, name: str, category: str, executor: Callable, config: Dict = None):
        """Register a custom tool"""
        tool = {
            "name": name,
            "category": category,
            "executor": executor,
            "config": config or {},
            "enabled": True
        }
        
        self.registered_tools[name] = tool
        if category in self.tool_categories:
            self.tool_categories[category].append(name)
        
        return tool
    
    async def execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Execute registered tool"""
        if tool_name not in self.registered_tools:
            return {"error": "Tool not found"}
        
        tool = self.registered_tools[tool_name]
        if not tool["enabled"]:
            return {"error": "Tool disabled"}
        
        try:
            result = await tool["executor"](params)
            return {"success": True, "tool": tool_name, "result": result}
        except Exception as e:
            return {"success": False, "tool": tool_name, "error": str(e)}
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get tools in category"""
        return self.tool_categories.get(category, [])
    
    def get_all_tools(self) -> Dict:
        """Get all registered tools"""
        return {
            name: {
                "category": tool["category"],
                "enabled": tool["enabled"],
                "config": tool["config"]
            }
            for name, tool in self.registered_tools.items()
        }
    
    def enable_tool(self, tool_name: str):
        """Enable tool"""
        if tool_name in self.registered_tools:
            self.registered_tools[tool_name]["enabled"] = True
    
    def disable_tool(self, tool_name: str):
        """Disable tool"""
        if tool_name in self.registered_tools:
            self.registered_tools[tool_name]["enabled"] = False

# Example tool executors
async def example_scanner(params: Dict) -> Dict:
    """Example scanner tool"""
    target = params.get("target")
    return {"scanned": target, "findings": []}

async def example_exploit(params: Dict) -> Dict:
    """Example exploit tool"""
    target = params.get("target")
    return {"exploited": target, "success": True}

# Initialize and register example tools
custom_tool_integration = CustomToolIntegration()
custom_tool_integration.register_tool("example_scanner", "scanner", example_scanner)
custom_tool_integration.register_tool("example_exploit", "exploit", example_exploit)
