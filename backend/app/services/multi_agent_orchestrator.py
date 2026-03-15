import asyncio
import aiohttp
import json
from typing import Dict, List, Optional
from datetime import datetime
from .kali_executor import kali_executor
from .ai_orchestrator import ai_orchestrator

class SpecializedAgent:
    """Base class for specialized security agents"""
    def __init__(self, name: str, specialty: str, tools: List[str]):
        self.name = name
        self.specialty = specialty
        self.tools = tools
        self.task_history = []
    
    async def execute_task(self, task: Dict) -> Dict:
        """Execute assigned task"""
        result = {"agent": self.name, "task": task, "results": []}
        
        for tool in task.get("tools", []):
            if tool in self.tools:
                tool_result = await kali_executor.execute_command(task.get("command", ""))
                result["results"].append(tool_result)
        
        self.task_history.append(result)
        return result

class ReconAgent(SpecializedAgent):
    """Reconnaissance specialist"""
    def __init__(self):
        super().__init__("ReconAgent", "reconnaissance", 
                        ["nmap", "masscan", "dnsenum", "sublist3r", "amass", "theharvester"])

class ExploitAgent(SpecializedAgent):
    """Exploitation specialist"""
    def __init__(self):
        super().__init__("ExploitAgent", "exploitation",
                        ["sqlmap", "metasploit", "burp", "zap", "commix"])

class PostExploitAgent(SpecializedAgent):
    """Post-exploitation specialist"""
    def __init__(self):
        super().__init__("PostExploitAgent", "post-exploitation",
                        ["mimikatz", "bloodhound", "crackmapexec", "responder"])

class AnalysisAgent(SpecializedAgent):
    """Analysis and reporting specialist"""
    def __init__(self):
        super().__init__("AnalysisAgent", "analysis",
                        ["radare2", "ghidra", "strings", "binwalk"])

class MultiAgentOrchestrator:
    """Advanced multi-agent orchestration system"""
    
    def __init__(self):
        self.agents = {
            "recon": ReconAgent(),
            "exploit": ExploitAgent(),
            "post_exploit": PostExploitAgent(),
            "analysis": AnalysisAgent()
        }
        self.ollama_url = "http://localhost:11434/api/generate"
        self.master_model = "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        self.mission_history = []
    
    async def query_ai(self, prompt: str, temperature: float = 0.7) -> str:
        """Query master AI"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.master_model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature
                }
                async with session.post(self.ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    result = await resp.json()
                    return result.get("response", "")
        except:
            return ""
    
    async def plan_mission(self, objective: str, target: str) -> Dict:
        """Master AI plans multi-agent mission"""
        
        plan_prompt = f"""You are a master penetration testing coordinator. Plan a multi-agent security assessment.

Objective: {objective}
Target: {target}

Available agents:
- ReconAgent: nmap, masscan, dnsenum, sublist3r, amass, theharvester
- ExploitAgent: sqlmap, metasploit, burp, zap, commix
- PostExploitAgent: mimikatz, bloodhound, crackmapexec, responder
- AnalysisAgent: radare2, ghidra, strings, binwalk

Create a mission plan with JSON structure:
{{
    "phases": [
        {{
            "name": "phase1",
            "agents": ["recon"],
            "tasks": [
                {{"agent": "recon", "action": "port_scan", "tools": ["nmap"], "params": {{"target": "{target}"}}}}
            ],
            "success_criteria": "criteria",
            "dependencies": []
        }}
    ],
    "coordination_strategy": "sequential|parallel|adaptive",
    "fallback_plan": "what to do if phase fails"
}}

Respond ONLY with valid JSON."""

        plan_response = await self.query_ai(plan_prompt, temperature=0.3)
        
        try:
            return json.loads(plan_response.strip())
        except:
            return {
                "phases": [{
                    "name": "recon",
                    "agents": ["recon"],
                    "tasks": [{"agent": "recon", "action": "scan", "tools": ["nmap"]}]
                }]
            }
    
    async def execute_mission(self, objective: str, target: str) -> Dict:
        """Execute multi-agent coordinated mission"""
        
        # Phase 1: Planning
        plan = await self.plan_mission(objective, target)
        
        mission = {
            "objective": objective,
            "target": target,
            "plan": plan,
            "execution": [],
            "start_time": datetime.utcnow().isoformat()
        }
        
        # Phase 2: Execution
        for phase in plan.get("phases", []):
            phase_result = {
                "phase": phase["name"],
                "agent_results": [],
                "coordination": []
            }
            
            # Execute tasks based on strategy
            strategy = plan.get("coordination_strategy", "sequential")
            
            if strategy == "parallel":
                # Parallel execution
                tasks = []
                for task in phase.get("tasks", []):
                    agent_name = task.get("agent")
                    if agent_name in self.agents:
                        tasks.append(self.agents[agent_name].execute_task(task))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                phase_result["agent_results"] = [r for r in results if not isinstance(r, Exception)]
            
            else:
                # Sequential execution with coordination
                for task in phase.get("tasks", []):
                    agent_name = task.get("agent")
                    if agent_name in self.agents:
                        result = await self.agents[agent_name].execute_task(task)
                        phase_result["agent_results"].append(result)
                        
                        # AI coordinates next step
                        coordination = await self._coordinate_agents(result, phase)
                        phase_result["coordination"].append(coordination)
                        
                        if coordination.get("action") == "escalate":
                            # Escalate to next agent
                            next_agent = coordination.get("next_agent")
                            if next_agent in self.agents:
                                escalation_task = coordination.get("task")
                                esc_result = await self.agents[next_agent].execute_task(escalation_task)
                                phase_result["agent_results"].append(esc_result)
            
            mission["execution"].append(phase_result)
        
        # Phase 3: Synthesis
        mission["synthesis"] = await self._synthesize_results(mission)
        mission["end_time"] = datetime.utcnow().isoformat()
        
        self.mission_history.append(mission)
        return mission
    
    async def _coordinate_agents(self, agent_result: Dict, phase: Dict) -> Dict:
        """AI coordinates between agents"""
        
        coord_prompt = f"""Analyze agent result and coordinate next action:

Agent: {agent_result.get('agent')}
Results: {json.dumps(agent_result.get('results', []), indent=2)[:2000]}
Phase: {phase.get('name')}

Decide coordination action:
{{
    "action": "continue|escalate|pivot|complete",
    "reason": "why",
    "next_agent": "agent_name",
    "task": {{"action": "...", "tools": [...]}},
    "findings": ["finding1"]
}}

Respond ONLY with valid JSON."""

        coord_response = await self.query_ai(coord_prompt, temperature=0.5)
        
        try:
            return json.loads(coord_response.strip())
        except:
            return {"action": "continue"}
    
    async def _synthesize_results(self, mission: Dict) -> Dict:
        """Synthesize all agent results"""
        
        synth_prompt = f"""Synthesize multi-agent mission results:

Objective: {mission.get('objective')}
Target: {mission.get('target')}
Execution: {json.dumps(mission.get('execution', []), indent=2)[:3000]}

Generate comprehensive report:
{{
    "executive_summary": "high-level findings",
    "agent_contributions": {{"agent": "contribution"}},
    "attack_chain": ["step1", "step2"],
    "vulnerabilities": [{{"severity": "...", "title": "...", "agent": "..."}}],
    "recommendations": ["rec1"],
    "collaboration_effectiveness": 0-100,
    "mission_success": true|false
}}

Respond ONLY with valid JSON."""

        synth_response = await self.query_ai(synth_prompt, temperature=0.4)
        
        try:
            return json.loads(synth_response.strip())
        except:
            return {"executive_summary": "Mission completed", "mission_success": True}
    
    async def adaptive_collaboration(self, agents: List[str], problem: str) -> Dict:
        """Agents collaborate adaptively on complex problem"""
        
        collab_prompt = f"""Coordinate multiple agents to solve complex security problem:

Problem: {problem}
Available Agents: {agents}

Create adaptive collaboration plan:
{{
    "approach": "how agents will collaborate",
    "agent_roles": {{"agent": "role"}},
    "communication_flow": ["agent1 -> agent2"],
    "decision_points": ["when to switch agents"],
    "success_metrics": ["metric1"]
}}

Respond ONLY with valid JSON."""

        plan = await self.query_ai(collab_prompt, temperature=0.6)
        
        try:
            collab_plan = json.loads(plan.strip())
        except:
            collab_plan = {"approach": "sequential"}
        
        # Execute collaborative problem-solving
        results = {"plan": collab_plan, "agent_outputs": []}
        
        for agent_name in agents:
            if agent_name in self.agents:
                task = {"problem": problem, "role": collab_plan.get("agent_roles", {}).get(agent_name)}
                result = await self.agents[agent_name].execute_task(task)
                results["agent_outputs"].append(result)
        
        # Synthesize collaborative solution
        results["solution"] = await self._synthesize_results({"execution": results["agent_outputs"]})
        
        return results

multi_agent_orchestrator = MultiAgentOrchestrator()
