import asyncio
from typing import Dict, Any
from datetime import datetime
from .base_agent import BaseAgent
from app.services.ai.agent import SecurityAgent

class ReportWriterAgent(BaseAgent):
    """Agent 4: Report Writer - Generates reports from other agents' logs"""
    
    def __init__(self, agent_id: str):
        super().__init__(agent_id)
        self.ai_agent = SecurityAgent()
        self.ai_agent.model = "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        self.reports_generated = 0
    
    async def execute_task(self) -> Dict[str, Any]:
        """Collect logs from all agents and generate report"""
        
        self.log("=" * 60)
        self.log("📊 REPORT GENERATION STARTED")
        self.log("=" * 60)
        
        # Import agent_manager to access other agents
        from .manager import agent_manager
        
        # Collect logs from all agents
        self.log("🔍 Collecting logs from all agents...")
        
        agent1_logs = agent_manager.get_agent_logs("vuln-scanner", limit=50)
        agent2_logs = agent_manager.get_agent_logs("threat-hunter", limit=50)
        agent3_logs = agent_manager.get_agent_logs("exploit-gen", limit=50)
        
        self.log(f"✅ Agent 1 (Vuln Scanner): {len(agent1_logs)} log entries")
        self.log(f"✅ Agent 2 (Threat Hunter): {len(agent2_logs)} log entries")
        self.log(f"✅ Agent 3 (Exploit Gen): {len(agent3_logs)} log entries")
        
        # Check if we have enough data
        total_logs = len(agent1_logs) + len(agent2_logs) + len(agent3_logs)
        
        if total_logs < 5:
            self.log("⚠️ Not enough data to generate report")
            self.log("💡 Start other agents first to collect data")
            return {"status": "insufficient_data", "message": "Start other agents first"}
        
        # Generate report sections
        self.log("=" * 60)
        self.log("🤖 AI ANALYSIS IN PROGRESS")
        self.log("=" * 60)
        
        # Executive Summary
        self.log("📝 Generating executive summary...")
        summary = await self.generate_executive_summary(agent1_logs, agent2_logs, agent3_logs)
        self.log(f"✅ Executive summary generated ({len(summary)} chars)")
        
        # Technical Details
        self.log("🔬 Generating technical details...")
        technical = await self.generate_technical_details(agent1_logs, agent2_logs, agent3_logs)
        self.log(f"✅ Technical details generated ({len(technical)} chars)")
        
        # Recommendations
        self.log("💡 Generating recommendations...")
        recommendations = await self.generate_recommendations(agent1_logs, agent2_logs, agent3_logs)
        self.log(f"✅ Recommendations generated ({len(recommendations)} chars)")
        
        # Risk Assessment
        self.log("⚠️ Generating risk assessment...")
        risk = await self.generate_risk_assessment(agent1_logs, agent2_logs, agent3_logs)
        self.log(f"✅ Risk assessment generated ({len(risk)} chars)")
        
        self.reports_generated += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        self.log("=" * 60)
        self.log(f"📄 REPORT #{self.reports_generated} COMPLETE")
        self.log(f"🕐 Timestamp: {timestamp}")
        self.log("=" * 60)
        self.log("📊 REPORT PREVIEW:")
        self.log("=" * 60)
        self.log(f"Executive Summary:\n{summary[:200]}...")
        self.log("=" * 60)
        self.log(f"Risk Level: {risk[:100]}...")
        self.log("=" * 60)
        
        return {
            "report_id": self.reports_generated,
            "timestamp": timestamp,
            "executive_summary": summary,
            "technical_details": technical,
            "recommendations": recommendations,
            "risk_assessment": risk,
            "data_sources": {
                "vuln_scanner_logs": len(agent1_logs),
                "threat_hunter_logs": len(agent2_logs),
                "exploit_gen_logs": len(agent3_logs)
            }
        }
    
    async def generate_executive_summary(self, agent1_logs, agent2_logs, agent3_logs) -> str:
        """Generate executive summary from all logs"""
        
        logs_combined = "\n".join([
            "=== VULNERABILITY SCANNER ===",
            "\n".join(agent1_logs[-10:]),
            "\n=== THREAT HUNTER ===",
            "\n".join(agent2_logs[-10:]),
            "\n=== EXPLOIT GENERATOR ===",
            "\n".join(agent3_logs[-10:])
        ])
        
        summary = await self.ask_ai(
            f"Generate an executive summary for this security assessment:\n\n{logs_combined[:2000]}\n\n"
            f"Include:\n"
            f"- Overall security posture\n"
            f"- Critical findings\n"
            f"- Risk level (Critical/High/Medium/Low)\n"
            f"- Key statistics\n"
            f"Write for C-level executives in non-technical language."
        )
        
        return summary
    
    async def generate_technical_details(self, agent1_logs, agent2_logs, agent3_logs) -> str:
        """Generate detailed technical report"""
        
        logs_combined = "\n".join([
            "=== VULNERABILITY SCANNER ===",
            "\n".join(agent1_logs[-20:]),
            "\n=== THREAT HUNTER ===",
            "\n".join(agent2_logs[-20:]),
            "\n=== EXPLOIT GENERATOR ===",
            "\n".join(agent3_logs[-20:])
        ])
        
        technical = await self.ask_ai(
            f"Generate detailed technical findings from these security logs:\n\n{logs_combined[:3000]}\n\n"
            f"Include:\n"
            f"- Detailed vulnerability analysis\n"
            f"- Network traffic anomalies\n"
            f"- Exploit possibilities\n"
            f"- CVE references if found\n"
            f"- CVSS scores if applicable\n"
            f"Write for security engineers and penetration testers."
        )
        
        return technical
    
    async def generate_recommendations(self, agent1_logs, agent2_logs, agent3_logs) -> str:
        """Generate actionable recommendations"""
        
        logs_combined = "\n".join([
            "\n".join(agent1_logs[-15:]),
            "\n".join(agent2_logs[-15:]),
            "\n".join(agent3_logs[-15:])
        ])
        
        recommendations = await self.ask_ai(
            f"Generate prioritized security recommendations based on:\n\n{logs_combined[:2500]}\n\n"
            f"Provide:\n"
            f"1. IMMEDIATE actions (within 24 hours)\n"
            f"2. SHORT-TERM fixes (within 1 week)\n"
            f"3. LONG-TERM strategy (within 1 month)\n"
            f"Prioritize by risk and impact. Be specific and actionable."
        )
        
        return recommendations
    
    async def generate_risk_assessment(self, agent1_logs, agent2_logs, agent3_logs) -> str:
        """Generate risk assessment"""
        
        logs_sample = "\n".join([
            "\n".join(agent1_logs[-10:]),
            "\n".join(agent2_logs[-10:]),
            "\n".join(agent3_logs[-10:])
        ])
        
        risk = await self.ask_ai(
            f"Assess the overall security risk based on:\n\n{logs_sample[:2000]}\n\n"
            f"Provide:\n"
            f"- Overall risk level (Critical/High/Medium/Low)\n"
            f"- Top 3 critical risks\n"
            f"- Business impact\n"
            f"- Likelihood of exploitation\n"
            f"Be concise and clear."
        )
        
        return risk
    
    async def ask_ai(self, question: str) -> str:
        """Ask AI for analysis"""
        try:
            messages = [{"role": "user", "content": question}]
            response = ""
            async for chunk in self.ai_agent.chat(messages, stream=False):
                response += chunk
            return response
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
