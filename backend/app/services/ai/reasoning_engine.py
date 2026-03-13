from typing import Dict, Any, List, Union
from app.services.ai.llm_service import OllamaLLMService
import json
import logging
import re

logger = logging.getLogger(__name__)

class ReasoningEngine:
    def __init__(self, model: str = "qwen2.5-coder:7b-instruct"):
        self.model = model
        self.llm = OllamaLLMService(model)
        # Use a model that supports JSON better
        self.converter_llm = OllamaLLMService("qwen2.5-coder:7b-instruct")
        self.history = []
    
    def set_model(self, model: str):
        """Change the model dynamically"""
        self.model = model
        self.llm = OllamaLLMService(model)
    
    def _extract_json(self, response: str) -> Any:
        """Extract JSON from LLM response with repair"""
        text = response.strip()
        logger.info(f"Attempting to extract JSON from: {text[:200]}...")
        
        # If response is empty or too short, return None
        if not text or len(text) < 2:
            logger.warning("Response too short for JSON")
            return None
        
        # Remove markdown code blocks
        if '```' in text:
            parts = text.split('```')
            for part in parts:
                clean = part.strip()
                if clean.startswith('json'):
                    clean = clean[4:].strip()
                if clean and clean[0] in '[{':
                    text = clean
                    break
        
        # Find JSON in text
        if not text.startswith(('[', '{')):
            brace = text.find('{')
            bracket = text.find('[')
            if brace != -1 and (bracket == -1 or brace < bracket):
                text = text[brace:]
            elif bracket != -1:
                text = text[bracket:]
            else:
                logger.warning("No JSON structure found in response")
                return None
        
        # Find end of JSON by tracking depth
        if text.startswith('{'):
            depth = 0
            in_string = False
            escape = False
            for i, char in enumerate(text):
                if escape:
                    escape = False
                    continue
                if char == '\\':
                    escape = True
                    continue
                if char == '"' and not escape:
                    in_string = not in_string
                if not in_string:
                    if char == '{':
                        depth += 1
                    elif char == '}':
                        depth -= 1
                        if depth == 0:
                            text = text[:i+1]
                            break
        elif text.startswith('['):
            depth = 0
            in_string = False
            escape = False
            for i, char in enumerate(text):
                if escape:
                    escape = False
                    continue
                if char == '\\':
                    escape = True
                    continue
                if char == '"' and not escape:
                    in_string = not in_string
                if not in_string:
                    if char == '[':
                        depth += 1
                    elif char == ']':
                        depth -= 1
                        if depth == 0:
                            text = text[:i+1]
                            break
        
        # Try to parse
        try:
            result = json.loads(text)
            logger.info(f"Successfully parsed JSON: {type(result)}")
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {str(e)[:100]}")
            
            # Try common fixes
            fixes = [
                text.replace("'", '"'),  # Single to double quotes
                text.replace('True', 'true').replace('False', 'false').replace('None', 'null'),  # Python to JSON
                re.sub(r'(\w+):', r'"\1":', text),  # Unquoted keys
            ]
            
            for fixed in fixes:
                try:
                    result = json.loads(fixed)
                    logger.info(f"Fixed JSON with repair: {type(result)}")
                    return result
                except:
                    continue
            
            logger.error(f"Could not repair JSON")
            return None
        except Exception as e:
            logger.error(f"JSON extraction failed: {str(e)[:100]}")
            return None
    
    async def _convert_to_json(self, text: str, expected_format: str) -> Any:
        """Convert plain text to JSON using Qwen"""
        prompt = f"""Convert the following text to valid JSON format.

Text: {text}

Expected format: {expected_format}

Rules:
- Return ONLY valid JSON, no explanations
- If text contains error messages, wrap in {{"error": "message"}}
- If text is already structured data, convert to proper JSON
- Use the expected format as a guide

JSON:"""
        
        try:
            response = await self.converter_llm.generate(prompt, temperature=0.1)
            result = self._extract_json(response)
            return result if result else {"raw_text": text[:200]}
        except Exception as e:
            logger.error(f"JSON conversion failed: {e}")
            return {"raw_text": text[:200], "error": str(e)}
    
    async def analyze_results(self, results: Union[Dict[str, Any], str]) -> Dict[str, Any]:
        if isinstance(results, str):
            results = await self._convert_to_json(results, '{"tool": "name", "findings": []}')
        
        prompt = f"""Analyze these security scan results and provide structured analysis.

Results:
{json.dumps(results, indent=2)}

Provide analysis in this JSON format:
{{
  "key_findings": ["finding 1", "finding 2"],
  "severity_assessment": "High",
  "next_tools": ["tool1", "tool2"],
  "exploitation_strategy": "strategy description",
  "defense_mechanisms": ["defense 1"]
}}

JSON:"""
        
        try:
            response = await self.llm.generate(prompt, temperature=0.1)
            result = self._extract_json(response)
            return result if result else {
                'key_findings': ['Analysis failed - could not parse response'],
                'severity_assessment': 'Unknown',
                'next_tools': [],
                'exploitation_strategy': 'Manual review required',
                'raw_response': response[:200]
            }
        except Exception as e:
            logger.error(f"Analyze failed: {e}")
            return {'key_findings': [f'Error: {str(e)}'], 'severity_assessment': 'Unknown'}
    
    async def build_attack_strategy(self, target: str, initial_recon: Union[Dict[str, Any], str]) -> List[Dict[str, Any]]:
        if isinstance(initial_recon, str):
            initial_recon = await self._convert_to_json(initial_recon, '{"ports": [], "services": []}')
        
        prompt = f"""You are a penetration testing expert. Build an attack strategy for target: {target}

Reconnaissance data:
{json.dumps(initial_recon, indent=2)}

Create a prioritized attack plan. Respond with ONLY a JSON array like this:
[
  {{
    "phase": "reconnaissance",
    "tool": "nmap",
    "params": "-sV -sC",
    "reason": "Detailed service detection",
    "priority": 9
  }},
  {{
    "phase": "exploitation",
    "tool": "sqlmap",
    "params": "-u http://target/login",
    "reason": "Test for SQL injection",
    "priority": 8
  }}
]

JSON:"""
        
        try:
            response = await self.llm.generate(prompt, temperature=0.1)
            logger.info(f"Strategy response: {response[:200]}...")
            result = self._extract_json(response)
            
            if isinstance(result, list):
                # Sort by priority and return
                result.sort(key=lambda x: x.get('priority', 5) if isinstance(x, dict) else 5, reverse=True)
                return result
            elif result:
                # If we got a dict instead of list, wrap it
                return [result]
            else:
                # Fallback: create basic strategy
                logger.warning("Using fallback strategy")
                return [
                    {"phase": "reconnaissance", "tool": "nmap", "params": "-sV", "reason": "Service detection", "priority": 8},
                    {"phase": "web_scan", "tool": "nikto", "params": "-h " + target, "reason": "Web vulnerability scan", "priority": 7}
                ]
        except Exception as e:
            logger.error(f"Strategy failed: {e}")
            return [{"phase": "error", "tool": "manual", "reason": f"Error: {str(e)}", "priority": 1}]
    
    async def suggest_next_action(self, current_findings: Union[List[Dict], str], tools_used: Union[List[str], str]) -> Dict[str, Any]:
        if isinstance(current_findings, str):
            converted = await self._convert_to_json(current_findings, '[{"type": "", "details": ""}]')
            current_findings = converted if isinstance(converted, list) else [converted]
        
        if isinstance(tools_used, str):
            tools_used = [t.strip() for t in tools_used.split(',') if t.strip()]
        
        prompt = f"""Suggest next action:

Findings: {json.dumps(current_findings, indent=2)}
Tools used: {', '.join(tools_used)}

Return JSON with: next_tool, params, reason, expected_outcome"""
        
        try:
            response = await self.llm.generate(prompt)
            result = self._extract_json(response)
            return result if result else {'next_tool': None, 'reason': 'No suggestion'}
        except Exception as e:
            logger.error(f"Next action failed: {e}")
            return {'next_tool': None, 'reason': 'Error'}
    
    async def identify_attack_path(self, findings: Union[Dict[str, Any], str]) -> List[str]:
        if isinstance(findings, str):
            findings = await self._convert_to_json(findings, '{"vulnerabilities": [], "services": []}')
        
        prompt = f"""Identify attack path based on findings:

{json.dumps(findings, indent=2)}

Return a JSON array of attack steps as strings. Example:
["Step 1: Exploit SQL injection in login form", "Step 2: Escalate privileges using weak sudo config"]

Return ONLY the JSON array, nothing else."""
        
        try:
            response = await self.llm.generate(prompt)
            logger.info(f"Attack path response: {response[:300]}")
            result = self._extract_json(response)
            
            if not result:
                logger.error("Failed to extract JSON from attack path response")
                return ["Error: Could not parse AI response"]
            
            if isinstance(result, list):
                # Filter out numeric-only items
                filtered = [str(item) for item in result if not (isinstance(item, (int, float)) or (isinstance(item, str) and item.isdigit()))]
                return filtered if filtered else ["Error: Invalid response format"]
            
            return ["Error: Expected array response"]
        except Exception as e:
            logger.error(f"Attack path failed: {e}")
            return [f"Error: {str(e)}"]
    
    async def detect_defenses(self, tool_outputs: Union[Dict[str, str], str]) -> Dict[str, Any]:
        if isinstance(tool_outputs, str):
            tool_outputs = await self._convert_to_json(tool_outputs, '{"tool": "output"}')
        
        truncated = {}
        if isinstance(tool_outputs, dict):
            for k, v in tool_outputs.items():
                truncated[k] = str(v)[:500] if isinstance(v, str) else str(v)[:500]
        else:
            truncated = {"data": str(tool_outputs)[:500]}
        
        prompt = f"""You are a cybersecurity expert. Analyze the following tool outputs to detect security defenses.

Tool outputs:
{json.dumps(truncated, indent=2)}

Analyze for:
1. Web Application Firewall (WAF) - Look for blocked requests, security headers, challenge pages
2. Intrusion Detection/Prevention Systems (IDS/IPS) - Look for connection drops, filtered ports
3. Rate limiting - Look for 429 errors, delayed responses, connection limits
4. Other security measures

Respond with ONLY this JSON format:
{{
  "waf_detected": true,
  "waf_type": "cloudflare",
  "ids_ips": false,
  "rate_limiting": true,
  "recommendations": ["Use slower scan rates", "Try different user agents"]
}}

JSON:"""
        
        try:
            response = await self.llm.generate(prompt, temperature=0.1)
            logger.info(f"Defense detection response: {response[:300]}")
            
            # Try to extract JSON
            result = self._extract_json(response)
            
            if not result:
                logger.error("Failed to extract JSON from defense detection response")
                # Try to parse manually if AI gave natural language
                waf_detected = any(word in response.lower() for word in ['waf', 'firewall', 'cloudflare', 'blocked'])
                rate_limit = any(word in response.lower() for word in ['rate', 'limit', '429', 'throttle'])
                
                return {
                    'waf_detected': waf_detected,
                    'waf_type': 'unknown' if waf_detected else None,
                    'ids_ips': False,
                    'rate_limiting': rate_limit,
                    'recommendations': ['Manual analysis required'],
                    'raw_response': response[:200]
                }
            
            # Ensure required fields
            if not isinstance(result, dict):
                return {'waf_detected': False, 'error': 'Invalid response format', 'recommendations': []}
            
            # Set defaults for missing fields
            result.setdefault('waf_detected', False)
            result.setdefault('ids_ips', False)
            result.setdefault('rate_limiting', False)
            result.setdefault('recommendations', [])
            
            return result
        except Exception as e:
            logger.error(f"Detect defenses failed: {e}")
            return {'waf_detected': False, 'error': str(e), 'recommendations': []}

# Global instance
reasoning_engine = ReasoningEngine()
