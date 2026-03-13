import asyncio
import aiohttp
import json
import base64
import jwt as pyjwt
from typing import Dict, List, Optional
from .kali_executor import kali_executor

class AdvancedWebToolsService:
    """Advanced web application security testing with AI analysis"""
    
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.models = {
            "code": "qwen2.5-coder:7b-instruct",
            "analysis": "deepseek-coder:6.7b-instruct",
            "advanced": "huihui_ai/glm-4.7-flash-abliterated:q4_K"
        }
    
    async def analyze_with_ai(self, prompt: str, model_key: str = "code") -> str:
        """Query Ollama model"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {"model": self.models[model_key], "prompt": prompt, "stream": False}
                async with session.post(self.ollama_url, json=payload) as resp:
                    result = await resp.json()
                    return result.get("response", "")
        except:
            return ""
    
    async def zap_spider(self, target_url: str) -> Dict:
        """OWASP ZAP spider scan"""
        cmd = f"zap-cli quick-scan --self-contained --spider -r {target_url}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze ZAP spider results and identify attack surface:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def zap_active_scan(self, target_url: str) -> Dict:
        """OWASP ZAP active scan"""
        cmd = f"zap-cli quick-scan --self-contained --ajax-spider -r {target_url}"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze ZAP active scan vulnerabilities and prioritize by severity:\n{result['output'][:4000]}",
                "advanced"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def nosqlmap_scan(self, target_url: str) -> Dict:
        """NoSQL injection testing"""
        cmd = f"python3 /opt/NoSQLMap/nosqlmap.py --url {target_url} --scan"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze NoSQL injection findings and suggest remediation:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def jwt_crack(self, token: str, wordlist: str = "/usr/share/wordlists/rockyou.txt") -> Dict:
        """JWT token cracking"""
        cmd = f"jwt-cracker '{token}' {wordlist}"
        result = await kali_executor.execute_command(cmd)
        
        # Also decode JWT locally
        try:
            decoded = pyjwt.decode(token, options={"verify_signature": False})
            result["decoded_payload"] = decoded
            
            ai_analysis = await self.analyze_with_ai(
                f"Analyze this JWT payload for security issues:\n{json.dumps(decoded, indent=2)}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        except:
            pass
        
        return result
    
    async def jwt_analyze(self, token: str) -> Dict:
        """Comprehensive JWT analysis"""
        try:
            header = pyjwt.get_unverified_header(token)
            payload = pyjwt.decode(token, options={"verify_signature": False})
            
            analysis = {
                "header": header,
                "payload": payload,
                "issues": []
            }
            
            # Check for common issues
            if header.get("alg") == "none":
                analysis["issues"].append("CRITICAL: Algorithm set to 'none'")
            if "exp" not in payload:
                analysis["issues"].append("WARNING: No expiration claim")
            if header.get("alg") == "HS256":
                analysis["issues"].append("INFO: Symmetric algorithm, check key strength")
            
            ai_analysis = await self.analyze_with_ai(
                f"Analyze JWT security:\nHeader: {header}\nPayload: {payload}\nIssues: {analysis['issues']}",
                "advanced"
            )
            analysis["ai_insights"] = ai_analysis
            
            return {"success": True, "analysis": analysis}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def wfuzz_scan(self, url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> Dict:
        """Web fuzzing with wfuzz"""
        cmd = f"wfuzz -c -z file,{wordlist} --hc 404 {url}/FUZZ"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze wfuzz results and identify interesting endpoints:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def commix_scan(self, url: str) -> Dict:
        """Command injection testing"""
        cmd = f"commix --url='{url}' --batch --level=2"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze command injection findings:\n{result['output'][:4000]}",
                "analysis"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def xsstrike_scan(self, url: str) -> Dict:
        """XSS vulnerability testing"""
        cmd = f"python3 /opt/XSStrike/xsstrike.py -u {url} --crawl"
        result = await kali_executor.execute_command(cmd)
        
        if result["success"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze XSS vulnerabilities and suggest fixes:\n{result['output'][:4000]}",
                "code"
            )
            result["ai_insights"] = ai_analysis
        
        return result
    
    async def ssrf_test(self, url: str) -> Dict:
        """SSRF vulnerability testing"""
        payloads = [
            "http://localhost",
            "http://127.0.0.1",
            "http://169.254.169.254/latest/meta-data/",
            "file:///etc/passwd"
        ]
        
        results = {"tested_payloads": [], "potential_ssrf": []}
        
        for payload in payloads:
            test_url = f"{url}?url={payload}"
            cmd = f"curl -s -o /dev/null -w '%{{http_code}}' '{test_url}'"
            result = await kali_executor.execute_command(cmd)
            
            results["tested_payloads"].append({
                "payload": payload,
                "response_code": result.get("output", "").strip()
            })
            
            if result.get("output", "").strip() == "200":
                results["potential_ssrf"].append(payload)
        
        if results["potential_ssrf"]:
            ai_analysis = await self.analyze_with_ai(
                f"Analyze potential SSRF vulnerabilities:\n{json.dumps(results, indent=2)}",
                "advanced"
            )
            results["ai_insights"] = ai_analysis
        
        return {"success": True, "results": results}
    
    async def full_web_assessment(self, target_url: str) -> Dict:
        """Comprehensive web application assessment"""
        results = {
            "target": target_url,
            "scans": {}
        }
        
        # Run scans in parallel
        tasks = {
            "zap_spider": self.zap_spider(target_url),
            "wfuzz": self.wfuzz_scan(target_url),
            "ssrf": self.ssrf_test(target_url),
            "xsstrike": self.xsstrike_scan(target_url)
        }
        
        completed = await asyncio.gather(*tasks.values(), return_exceptions=True)
        
        for key, result in zip(tasks.keys(), completed):
            if not isinstance(result, Exception):
                results["scans"][key] = result
        
        # Generate comprehensive report
        summary = "\n\n".join([
            f"{k}: {str(v)[:500]}" 
            for k, v in results["scans"].items()
        ])
        
        final_report = await self.analyze_with_ai(
            f"Generate executive summary of web application security assessment:\n{summary}",
            "advanced"
        )
        
        results["executive_summary"] = final_report
        return results

advanced_web_tools_service = AdvancedWebToolsService()
