import json
import os
import re
import subprocess
from typing import Dict, List
from datetime import datetime
from collections import Counter

# Docker container paths - adjust based on your setup
DOCKER_COWRIE_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "honeypots", "cowrie", "logs")
LOCAL_COWRIE_JSON = os.path.join(DOCKER_COWRIE_LOGS, "cowrie.json")


def check_docker_container_status(container_name: str) -> bool:
    """Check if a Docker container is running"""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return container_name in result.stdout
    except Exception as e:
        print(f"Error checking Docker container {container_name}: {e}")
        return False


def get_docker_logs(container_name: str, lines: int = 50) -> List[Dict]:
    """Get logs from a Docker container and parse them"""
    try:
        result = subprocess.run(
            ["docker", "logs", "--tail", str(lines), container_name],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Parse the plain text logs
        attacks = []
        for line in result.stdout.split('\n'):
            # Look for login attempts
            if 'login attempt' in line or 'login failed' in line or 'login succeeded' in line:
                # Extract IP address
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                src_ip = ip_match.group(1) if ip_match else 'unknown'
                
                # Extract username and password
                username_match = re.search(r"b'([^']+)'/b'([^']+)'", line)
                if username_match:
                    username = username_match.group(1)
                    password = username_match.group(2)
                else:
                    username = 'unknown'
                    password = 'unknown'
                
                # Determine if success
                success = 'succeeded' in line
                
                attacks.append({
                    'eventid': 'cowrie.login.' + ('success' if success else 'failed'),
                    'src_ip': src_ip,
                    'username': username,
                    'password': password,
                    'timestamp': datetime.now().isoformat()
                })
            
            # Look for commands
            elif 'CMD:' in line:
                ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                src_ip = ip_match.group(1) if ip_match else 'unknown'
                cmd_match = re.search(r'CMD: (.+)', line)
                cmd = cmd_match.group(1) if cmd_match else 'unknown'
                
                attacks.append({
                    'eventid': 'cowrie.command.success',
                    'src_ip': src_ip,
                    'input': cmd,
                    'timestamp': datetime.now().isoformat()
                })
        
        return attacks
    except Exception as e:
        print(f"Error getting Docker logs for {container_name}: {e}")
        return []


def start_honeypot(honeypot_type: str) -> Dict:
    """Start a honeypot container using docker-compose"""
    try:
        honeypot_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "honeypots")
        container_name = f"securesight_{honeypot_type}"
        
        # Check if already running
        if check_docker_container_status(container_name):
            return {"success": True, "message": f"{honeypot_type} is already running"}
        
        # Start the container
        result = subprocess.run(
            ["docker", "start", container_name],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=honeypot_dir
        )
        
        if result.returncode == 0:
            return {"success": True, "message": f"{honeypot_type} started successfully"}
        else:
            return {"success": False, "message": f"Failed to start {honeypot_type}: {result.stderr}"}
    except Exception as e:
        return {"success": False, "message": f"Error starting {honeypot_type}: {str(e)}"}


def stop_honeypot(honeypot_type: str) -> Dict:
    """Stop a honeypot container"""
    try:
        container_name = f"securesight_{honeypot_type}"
        
        # Check if running
        if not check_docker_container_status(container_name):
            return {"success": True, "message": f"{honeypot_type} is not running"}
        
        # Stop the container
        result = subprocess.run(
            ["docker", "stop", container_name],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return {"success": True, "message": f"{honeypot_type} stopped successfully"}
        else:
            return {"success": False, "message": f"Failed to stop {honeypot_type}: {result.stderr}"}
    except Exception as e:
        return {"success": False, "message": f"Error stopping {honeypot_type}: {str(e)}"}


class HoneypotManager:
    """Manage Dionaea and Cowrie honeypots"""
    
    def __init__(self):
        self.cowrie_log = LOCAL_COWRIE_JSON
        self.dionaea_log = "/var/log/dionaea/dionaea.log"
        self.attack_history = []
    
    def _read_json_log(self, file_path: str) -> List[Dict]:
        """Read and parse JSON log file"""
        attacks = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            attacks.append(entry)
                        except json.JSONDecodeError:
                            continue
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        return attacks
    
    async def parse_dionaea_logs(self, log_path: str = None) -> Dict:
        """Parse Dionaea honeypot logs"""
        attacks = []
        
        # Try to read from Docker volume or use sample data
        dionaea_path = log_path or self.dionaea_log
        
        # Check for Docker volume mount
        docker_dionaea = "/var/lib/dionaea/iso-images"
        if os.path.exists(docker_dionaea):
            attacks = self._read_json_log("/var/log/dionaea/dionaea.log")
        
        # If no real data, return empty
        if not attacks:
            attacks = []
        
        return {
            "honeypot": "dionaea",
            "attacks": attacks,
            "total_attacks": len(attacks),
            "unique_ips": len(set(a.get("src_ip", a.get("remote_ip", "")) for a in attacks))
        }
    
    async def parse_cowrie_logs(self, log_path: str = None) -> Dict:
        """Parse Cowrie SSH honeypot logs"""
        cowrie_path = log_path or self.cowrie_log
        
        attacks = []
        credentials_tried = []
        
        # First try to read from Docker logs directly
        if check_docker_container_status("securesight_cowrie"):
            attacks = get_docker_logs("securesight_cowrie", 100)
        # Fallback to reading from JSON file if it exists
        elif os.path.exists(cowrie_path):
            attacks = self._read_json_log(cowrie_path)
        
        # Extract credentials from attacks
        for attack in attacks:
            if attack.get("eventid") == "cowrie.login.failed":
                credentials_tried.append({
                    "username": attack.get("username", ""),
                    "password": attack.get("password", ""),
                    "src_ip": attack.get("src_ip", "")
                })
            elif attack.get("eventid") == "cowrie.login.success":
                credentials_tried.append({
                    "username": attack.get("username", ""),
                    "password": attack.get("password", ""),
                    "src_ip": attack.get("src_ip", ""),
                    "success": True
                })
        
        return {
            "honeypot": "cowrie",
            "attacks": attacks,
            "total_attempts": len(attacks),
            "unique_ips": len(set(a.get("src_ip", "") for a in attacks)),
            "credentials_tried": credentials_tried
        }
    
    async def get_honeypot_status(self) -> Dict:
        """Get status of honeypots by checking Docker container status"""
        # Check Docker container status directly
        cowrie_running = check_docker_container_status("securesight_cowrie")
        dionaea_running = check_docker_container_status("securesight_dionaea")
        
        return {
            "cowrie": {
                "status": "running" if cowrie_running else "stopped",
                "log_path": self.cowrie_log,
                "port": 2222
            },
            "dionaea": {
                "status": "running" if dionaea_running else "stopped",
                "port": "21,80,443,445,1433,3306"
            }
        }
    
    async def start_honeypot(self, honeypot_type: str) -> Dict:
        """Start a honeypot container"""
        return start_honeypot(honeypot_type)
    
    async def stop_honeypot(self, honeypot_type: str) -> Dict:
        """Stop a honeypot container"""
        return stop_honeypot(honeypot_type)
    
    async def get_attack_analytics(self) -> Dict:
        """Get attack analytics across all honeypots"""
        
        dionaea = await self.parse_dionaea_logs()
        cowrie = await self.parse_cowrie_logs()
        
        all_ips = []
        all_ips.extend([a.get("src_ip", a.get("remote_ip", "")) for a in dionaea.get("attacks", [])])
        all_ips.extend([a.get("src_ip", "") for a in cowrie.get("attacks", [])])
        
        # Filter empty IPs
        all_ips = [ip for ip in all_ips if ip]
        
        return {
            "total_attacks": dionaea["total_attacks"] + cowrie["total_attempts"],
            "unique_attackers": len(set(all_ips)),
            "top_attackers": Counter(all_ips).most_common(10),
            "dionaea_stats": dionaea,
            "cowrie_stats": cowrie,
            "attack_timeline": self._generate_timeline(dionaea, cowrie)
        }
    
    def _generate_timeline(self, dionaea: Dict, cowrie: Dict) -> List[Dict]:
        """Generate attack timeline"""
        timeline = []
        
        for attack in dionaea.get("attacks", []):
            timeline.append({
                "timestamp": attack.get("timestamp", attack.get("time", "")),
                "honeypot": "dionaea",
                "src_ip": attack.get("src_ip", attack.get("remote_ip", "")),
                "target_port": attack.get("dst_port", "")
            })
        
        for attack in cowrie.get("attacks", []):
            timeline.append({
                "timestamp": attack.get("timestamp", attack.get("time", "")),
                "honeypot": "cowrie",
                "src_ip": attack.get("src_ip", ""),
                "credentials": f"{attack.get('username', '')}:{attack.get('password', '')}"
            })
        
        return sorted(timeline, key=lambda x: x.get("timestamp", ""), reverse=True)[:50]

honeypot_manager = HoneypotManager()
