import asyncio
from typing import Dict, List
from .kali_executor import kali_executor

class NetworkTopologyMapper:
    """Network topology visualization and mapping"""
    
    def __init__(self):
        self.topology = {"nodes": [], "edges": [], "subnets": []}
    
    async def discover_topology(self, target_range: str) -> Dict:
        """Discover network topology"""
        
        # Parallel discovery
        tasks = {
            "hosts": self._discover_hosts(target_range),
            "routes": self._discover_routes(),
            "arp": self._discover_arp()
        }
        
        results = {}
        for key, task in tasks.items():
            results[key] = await task
        
        # Build topology graph
        self.topology = self._build_graph(results)
        return self.topology
    
    async def _discover_hosts(self, target: str) -> List[Dict]:
        """Discover active hosts"""
        result = await kali_executor.execute_command(f"nmap -sn {target}")
        hosts = []
        
        if result.get("success"):
            for line in result.get("output", "").split("\n"):
                if "Nmap scan report for" in line:
                    ip = line.split()[-1].strip("()")
                    hosts.append({"ip": ip, "type": "host", "status": "up"})
        
        return hosts
    
    async def _discover_routes(self) -> List[Dict]:
        """Discover network routes"""
        result = await kali_executor.execute_command("ip route show")
        routes = []
        
        if result.get("success"):
            for line in result.get("output", "").split("\n"):
                if line.strip():
                    routes.append({"route": line, "type": "route"})
        
        return routes
    
    async def _discover_arp(self) -> List[Dict]:
        """Discover ARP table"""
        result = await kali_executor.execute_command("arp -a")
        arp_entries = []
        
        if result.get("success"):
            for line in result.get("output", "").split("\n"):
                if "at" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        arp_entries.append({"ip": parts[1].strip("()"), "mac": parts[3], "type": "arp"})
        
        return arp_entries
    
    def _build_graph(self, discovery_results: Dict) -> Dict:
        """Build topology graph"""
        nodes = []
        edges = []
        
        # Add hosts as nodes
        for host in discovery_results.get("hosts", []):
            nodes.append({
                "id": host["ip"],
                "label": host["ip"],
                "type": "host",
                "status": host["status"]
            })
        
        # Add edges from ARP
        for arp in discovery_results.get("arp", []):
            edges.append({
                "source": "gateway",
                "target": arp["ip"],
                "type": "arp"
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "subnets": self._identify_subnets(nodes),
            "graph_data": {"directed": False, "multigraph": False}
        }
    
    def _identify_subnets(self, nodes: List[Dict]) -> List[str]:
        """Identify subnets from nodes"""
        subnets = set()
        for node in nodes:
            ip = node.get("id", "")
            if ip:
                subnet = ".".join(ip.split(".")[:3]) + ".0/24"
                subnets.add(subnet)
        return list(subnets)

network_topology_mapper = NetworkTopologyMapper()
