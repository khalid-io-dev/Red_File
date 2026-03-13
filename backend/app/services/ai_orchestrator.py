import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from .kali_executor import kali_executor

class AIOrchestrator:
    """Mega-framework AI orchestration with autonomous decision-making"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            "planner": "huihui_ai/glm-4.7-flash-abliterated:q4_K",
            "coder": "qwen2.5-coder:7b-instruct",
            "analyst": "deepseek-coder:6.7b-instruct"
        }
        self.tools = self._register_tools()
        self.execution_history = []
    
    def _register_tools(self) -> Dict:
        """Register available tools for AI to use"""
        return {
            "nmap_scan": {"cmd": "nmap -sV {target}", "desc": "Port and service scan"},
            "sqlmap": {"cmd": "sqlmap -u {url} --batch", "desc": "SQL injection testing"},
            "nikto": {"cmd": "nikto -h {target}", "desc": "Web vulnerability scan"},
            "gobuster": {"cmd": "gobuster dir -u {url} -w /usr/share/wordlists/dirb/common.txt", "desc": "Directory enumeration"},
            "wpscan": {"cmd": "wpscan --url {url}", "desc": "WordPress security scan"},
            "bloodhound": {"cmd": "bloodhound-python -d {domain} -u {user} -p {pass} -c all", "desc": "AD enumeration"},
            "mimikatz": {"cmd": "impacket-secretsdump {user}:{pass}@{target}", "desc": "Credential dumping"},
            "kerberoast": {"cmd": "impacket-GetUserSPNs {domain}/{user}:{pass} -request", "desc": "Kerberoasting attack"},
            "responder": {"cmd": "responder -I eth0 -wrf", "desc": "NTLM hash capture"},
            "crackmapexec": {"cmd": "crackmapexec smb {target} -u {user} -p {pass}", "desc": "SMB enumeration"},
            "radare2": {"cmd": "r2 -q -c 'aaa; pdf @ main' {binary}", "desc": "Binary analysis"},
            "strings": {"cmd": "strings {binary}", "desc": "Extract strings from binary"},
            "zap_scan": {"cmd": "zap-cli quick-scan {url}", "desc": "OWASP ZAP scan"},
            "jwt_decode": {"cmd": "python3 -c 'import jwt; print(jwt.decode(\"{token}\", verify=False))'", "desc": "JWT token decode"}
        }
    
    async def query_model(self, prompt: str, model_key: str = "planner", temperature: float = 0.7) -> str:
        """Query Ollama model with enhanced prompting"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.models[model_key],
                    "prompt": prompt,
                    "stream": False,
                    "temperature": temperature,
                    "options": {
                        "num_predict": 2000,
                        "top_k": 40,
                        "top_p": 0.9
                    }
                }
                async with session.post(self.ollama_url, json=payload, timeout=aiohttp.ClientTimeout(total=120)) as resp:
                    result = await resp.json()
                    return result.get("response", "")
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def autonomous_assessment(self, target: str, assessment_type: str = "full") -> Dict:
        """Autonomous security assessment with AI decision-making"""
        
        # Phase 1: Planning
        plan_prompt = f"""You are an expert penetration tester. Create a detailed attack plan for target: {target}
        
Available tools: {json.dumps(list(self.tools.keys()), indent=2)}

Assessment type: {assessment_type}

Generate a JSON plan with this structure:
{{
    "phases": [
        {{
            "name": "reconnaissance",
            "tools": ["nmap_scan", "nikto"],
            "params": {{"target": "{target}"}},
            "reason": "Initial enumeration"
        }}
    ],
    "success_criteria": "What indicates successful completion",
    "fallback_strategy": "What to do if primary approach fails"
}}

Respond ONLY with valid JSON, no other text."""

        plan_response = await self.query_model(plan_prompt, "planner", temperature=0.3)
        
        try:
            plan = json.loads(plan_response.strip())
        except:
            # Fallback plan
            plan = {
                "phases": [
                    {"name": "recon", "tools": ["nmap_scan"], "params": {"target": target}, "reason": "Basic scan"}
                ]
            }
        
        results = {"target": target, "plan": plan, "execution": []}
        
        # Phase 2: Execution with adaptive decision-making
        for phase in plan.get("phases", []):
            phase_results = {"phase": phase["name"], "tools": []}
            
            for tool_name in phase.get("tools", []):
                if tool_name not in self.tools:
                    continue
                
                # Execute tool
                tool_result = await self._execute_tool(tool_name, phase.get("params", {}))
                phase_results["tools"].append(tool_result)
                
                # AI analyzes result and decides next action
                decision = await self._analyze_and_decide(tool_result, target, phase["name"])
                
                if decision.get("action") == "escalate":
                    # AI suggests escalation
                    escalation_tools = decision.get("suggested_tools", [])
                    for esc_tool in escalation_tools:
                        if esc_tool in self.tools:
                            esc_result = await self._execute_tool(esc_tool, decision.get("params", {}))
                            phase_results["tools"].append(esc_result)
                
                elif decision.get("action") == "pivot":
                    # AI suggests pivoting strategy
                    phase_results["pivot_strategy"] = decision.get("strategy")
            
            results["execution"].append(phase_results)
        
        # Phase 3: Generate comprehensive report
        report = await self._generate_report(results)
        results["report"] = report
        
        return results
    
    async def _execute_tool(self, tool_name: str, params: Dict) -> Dict:
        """Execute tool with parameter substitution"""
        tool = self.tools.get(tool_name)
        if not tool:
            return {"tool": tool_name, "error": "Tool not found"}
        
        cmd = tool["cmd"]
        for key, value in params.items():
            cmd = cmd.replace(f"{{{key}}}", str(value))
        
        result = await kali_executor.execute_command(cmd)
        result["tool"] = tool_name
        result["description"] = tool["desc"]
        
        self.execution_history.append({"tool": tool_name, "result": result})
        
        return result
    
    async def _analyze_and_decide(self, tool_result: Dict, target: str, phase: str) -> Dict:
        """AI analyzes tool output and decides next action"""
        
        analysis_prompt = f"""Analyze this security tool output and decide next action:

Tool: {tool_result.get('tool')}
Output: {tool_result.get('output', '')[:2000]}
Error: {tool_result.get('error', 'None')}
Target: {target}
Current Phase: {phase}

Available actions:
1. "continue" - Current approach working, continue
2. "escalate" - Found vulnerability, escalate attack
3. "pivot" - Current approach not working, try different strategy
4. "complete" - Phase objectives achieved

Respond with JSON:
{{
    "action": "escalate|pivot|continue|complete",
    "reason": "Why this action",
    "suggested_tools": ["tool1", "tool2"],
    "params": {{"key": "value"}},
    "findings": ["finding1", "finding2"]
}}

Respond ONLY with valid JSON."""

        decision_response = await self.query_model(analysis_prompt, "analyst", temperature=0.5)
        
        try:
            return json.loads(decision_response.strip())
        except:
            return {"action": "continue", "reason": "Default action"}
    
    async def _generate_report(self, results: Dict) -> Dict:
        """Generate comprehensive assessment report"""
        
        report_prompt = f"""Generate a comprehensive penetration testing report:

Target: {results.get('target')}
Execution Results: {json.dumps(results.get('execution', []), indent=2)[:3000]}

Generate JSON report:
{{
    "executive_summary": "High-level findings for executives",
    "technical_details": "Detailed technical analysis",
    "vulnerabilities": [
        {{"severity": "critical|high|medium|low", "title": "...", "description": "...", "remediation": "..."}}
    ],
    "attack_paths": ["path1", "path2"],
    "recommendations": ["rec1", "rec2"],
    "risk_score": 0-100
}}

Respond ONLY with valid JSON."""

        report_response = await self.query_model(report_prompt, "planner", temperature=0.4)
        
        try:
            return json.loads(report_response.strip())
        except:
            return {"executive_summary": "Report generation failed", "risk_score": 0}
    
    async def generate_exploit_code(self, vulnerability: str, target_info: Dict) -> Dict:
        """AI generates exploit code for discovered vulnerability"""
        
        code_prompt = f"""Generate Python exploit code for this vulnerability:

Vulnerability: {vulnerability}
Target Info: {json.dumps(target_info, indent=2)}

Requirements:
1. Working exploit code
2. Error handling
3. Comments explaining each step
4. Safe execution (no destructive actions)

Generate complete Python code with proper structure."""

        code = await self.query_model(code_prompt, "coder", temperature=0.3)
        
        # AI reviews its own code
        review_prompt = f"""Review this exploit code for security and correctness:

{code}

Provide JSON feedback:
{{
    "issues": ["issue1", "issue2"],
    "improvements": ["improvement1"],
    "security_concerns": ["concern1"],
    "rating": 0-10
}}"""

        review = await self.query_model(review_prompt, "analyst", temperature=0.4)
        
        try:
            review_data = json.loads(review.strip())
        except:
            review_data = {"rating": 5}
        
        return {
            "code": code,
            "review": review_data,
            "language": "python"
        }
    
    async def fix_failed_command(self, failed_cmd: str, error: str) -> Dict:
        """AI fixes failed commands automatically"""
        
        fix_prompt = f"""This command failed. Fix it:

Command: {failed_cmd}
Error: {error}

Provide JSON response:
{{
    "fixed_command": "corrected command",
    "explanation": "what was wrong and how you fixed it",
    "alternative_approaches": ["approach1", "approach2"]
}}

Respond ONLY with valid JSON."""

        fix_response = await self.query_model(fix_prompt, "coder", temperature=0.3)
        
        try:
            fix_data = json.loads(fix_response.strip())
            
            # Try executing fixed command
            result = await kali_executor.execute_command(fix_data.get("fixed_command", ""))
            fix_data["execution_result"] = result
            
            return fix_data
        except:
            return {"error": "Could not fix command"}
    
    async def suggest_next_steps(self, current_results: List[Dict]) -> Dict:
        """AI suggests next steps based on current findings"""
        
        suggestion_prompt = f"""Based on these security assessment results, suggest next steps:

Results: {json.dumps(current_results, indent=2)[:3000]}

Provide JSON response:
{{
    "immediate_actions": ["action1", "action2"],
    "tools_to_use": ["tool1", "tool2"],
    "attack_vectors": ["vector1", "vector2"],
    "priority": "critical|high|medium|low",
    "estimated_time": "time estimate",
    "success_probability": 0-100
}}

Respond ONLY with valid JSON."""

        suggestion = await self.query_model(suggestion_prompt, "planner", temperature=0.6)
        
        try:
            return json.loads(suggestion.strip())
        except:
            return {"immediate_actions": ["Continue reconnaissance"]}
    
    async def multi_model_consensus(self, question: str) -> Dict:
        """Get consensus from all three AI models"""
        
        tasks = {
            "planner": self.query_model(question, "planner"),
            "coder": self.query_model(question, "coder"),
            "analyst": self.query_model(question, "analyst")
        }
        
        responses = await asyncio.gather(*tasks.values())
        
        # Synthesize consensus
        synthesis_prompt = f"""Synthesize these three expert opinions into one recommendation:

Planner: {responses[0][:500]}
Coder: {responses[1][:500]}
Analyst: {responses[2][:500]}

Question: {question}

Provide final recommendation with confidence score (0-100)."""

        consensus = await self.query_model(synthesis_prompt, "planner", temperature=0.3)
        
        return {
            "question": question,
            "individual_responses": {
                "planner": responses[0],
                "coder": responses[1],
                "analyst": responses[2]
            },
            "consensus": consensus
        }

ai_orchestrator = AIOrchestrator()
