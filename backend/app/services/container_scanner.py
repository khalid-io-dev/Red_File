import docker
from kubernetes import client, config
from typing import List, Dict
import subprocess
import json

class ContainerScanner:
    """Scan containers and Kubernetes for security issues"""
    
    def __init__(self):
        try:
            self.docker_client = docker.from_env()
        except:
            self.docker_client = None
        
        try:
            config.load_kube_config()
            self.k8s_v1 = client.CoreV1Api()
            self.k8s_rbac = client.RbacAuthorizationV1Api()
        except:
            self.k8s_v1 = None
            self.k8s_rbac = None
    
    # ===== DOCKER SCANNING =====
    
    async def scan_docker_images(self) -> List[Dict]:
        """Scan Docker images for vulnerabilities"""
        findings = []
        
        if not self.docker_client:
            return [{"error": "Docker client not available"}]
        
        try:
            images = self.docker_client.images.list()
            
            for image in images:
                image_name = image.tags[0] if image.tags else image.id
                
                # Check image age
                created = image.attrs['Created']
                findings.append({
                    "resource": image_name,
                    "type": "Docker Image",
                    "severity": "Info",
                    "issue": "Image metadata",
                    "description": f"Image created: {created}"
                })
                
                # Scan with Trivy if available
                trivy_results = await self._scan_with_trivy(image_name)
                findings.extend(trivy_results)
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_docker_containers(self) -> List[Dict]:
        """Scan running Docker containers"""
        findings = []
        
        if not self.docker_client:
            return [{"error": "Docker client not available"}]
        
        try:
            containers = self.docker_client.containers.list()
            
            for container in containers:
                # Check privileged mode
                if container.attrs['HostConfig']['Privileged']:
                    findings.append({
                        "resource": container.name,
                        "type": "Docker Container",
                        "severity": "Critical",
                        "issue": "Privileged container",
                        "description": f"Container {container.name} is running in privileged mode"
                    })
                
                # Check for host network mode
                if container.attrs['HostConfig']['NetworkMode'] == 'host':
                    findings.append({
                        "resource": container.name,
                        "type": "Docker Container",
                        "severity": "High",
                        "issue": "Host network mode",
                        "description": f"Container {container.name} uses host network mode"
                    })
                
                # Check for mounted volumes
                for mount in container.attrs['Mounts']:
                    if mount['Type'] == 'bind' and mount['Source'] == '/':
                        findings.append({
                            "resource": container.name,
                            "type": "Docker Container",
                            "severity": "Critical",
                            "issue": "Root filesystem mounted",
                            "description": f"Container {container.name} has root filesystem mounted"
                        })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_docker_daemon(self) -> Dict:
        """Scan Docker daemon configuration"""
        findings = []
        
        if not self.docker_client:
            return {"error": "Docker client not available"}
        
        try:
            info = self.docker_client.info()
            
            # Check if Docker socket is exposed
            if info.get('DockerRootDir') == '/var/run/docker.sock':
                findings.append({
                    "resource": "Docker Daemon",
                    "type": "Configuration",
                    "severity": "High",
                    "issue": "Docker socket exposed",
                    "description": "Docker socket may be accessible"
                })
            
            # Check for user namespaces
            if not info.get('SecurityOptions', []):
                findings.append({
                    "resource": "Docker Daemon",
                    "type": "Configuration",
                    "severity": "Medium",
                    "issue": "User namespaces not enabled",
                    "description": "User namespace remapping is not configured"
                })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return {"findings": findings}
    
    async def scan_dockerfile(self, path: str) -> List[Dict]:
        """Scan Dockerfile for security issues"""
        findings = []
        
        try:
            with open(path, 'r') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                
                # Check for running as root
                if line.startswith('USER root'):
                    findings.append({
                        "resource": path,
                        "type": "Dockerfile",
                        "severity": "High",
                        "issue": "Running as root",
                        "description": f"Line {i}: Container runs as root user",
                        "line": i
                    })
                
                # Check for latest tag
                if 'FROM' in line and ':latest' in line:
                    findings.append({
                        "resource": path,
                        "type": "Dockerfile",
                        "severity": "Medium",
                        "issue": "Using latest tag",
                        "description": f"Line {i}: Using 'latest' tag is not recommended",
                        "line": i
                    })
                
                # Check for ADD instead of COPY
                if line.startswith('ADD '):
                    findings.append({
                        "resource": path,
                        "type": "Dockerfile",
                        "severity": "Low",
                        "issue": "Using ADD",
                        "description": f"Line {i}: Use COPY instead of ADD",
                        "line": i
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    # ===== KUBERNETES SCANNING =====
    
    async def scan_k8s_pods(self, namespace: str = 'default') -> List[Dict]:
        """Scan Kubernetes pods"""
        findings = []
        
        if not self.k8s_v1:
            return [{"error": "Kubernetes client not available"}]
        
        try:
            pods = self.k8s_v1.list_namespaced_pod(namespace)
            
            for pod in pods.items:
                # Check for privileged containers
                for container in pod.spec.containers:
                    if container.security_context and container.security_context.privileged:
                        findings.append({
                            "resource": f"{pod.metadata.name}/{container.name}",
                            "type": "Kubernetes Pod",
                            "severity": "Critical",
                            "issue": "Privileged container",
                            "description": f"Container {container.name} in pod {pod.metadata.name} is privileged"
                        })
                    
                    # Check for host network
                    if pod.spec.host_network:
                        findings.append({
                            "resource": pod.metadata.name,
                            "type": "Kubernetes Pod",
                            "severity": "High",
                            "issue": "Host network enabled",
                            "description": f"Pod {pod.metadata.name} uses host network"
                        })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_k8s_rbac(self) -> List[Dict]:
        """Scan Kubernetes RBAC"""
        findings = []
        
        if not self.k8s_rbac:
            return [{"error": "Kubernetes RBAC client not available"}]
        
        try:
            # Check cluster roles
            cluster_roles = self.k8s_rbac.list_cluster_role()
            
            for role in cluster_roles.items:
                for rule in role.rules:
                    # Check for wildcard permissions
                    if '*' in rule.verbs or '*' in rule.resources:
                        findings.append({
                            "resource": role.metadata.name,
                            "type": "ClusterRole",
                            "severity": "Critical",
                            "issue": "Wildcard permissions",
                            "description": f"ClusterRole {role.metadata.name} has wildcard permissions"
                        })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_k8s_network_policies(self) -> List[Dict]:
        """Scan Kubernetes network policies"""
        findings = []
        
        if not self.k8s_v1:
            return [{"error": "Kubernetes client not available"}]
        
        try:
            namespaces = self.k8s_v1.list_namespace()
            
            for ns in namespaces.items:
                # Check if network policies exist
                net_client = client.NetworkingV1Api()
                policies = net_client.list_namespaced_network_policy(ns.metadata.name)
                
                if not policies.items:
                    findings.append({
                        "resource": ns.metadata.name,
                        "type": "Namespace",
                        "severity": "Medium",
                        "issue": "No network policies",
                        "description": f"Namespace {ns.metadata.name} has no network policies"
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def scan_k8s_secrets(self, namespace: str = 'default') -> List[Dict]:
        """Scan Kubernetes secrets"""
        findings = []
        
        if not self.k8s_v1:
            return [{"error": "Kubernetes client not available"}]
        
        try:
            secrets = self.k8s_v1.list_namespaced_secret(namespace)
            
            for secret in secrets.items:
                # Check for unencrypted secrets
                if secret.type == 'Opaque':
                    findings.append({
                        "resource": secret.metadata.name,
                        "type": "Secret",
                        "severity": "High",
                        "issue": "Opaque secret",
                        "description": f"Secret {secret.metadata.name} is of type Opaque (base64 encoded only)"
                    })
        
        except Exception as e:
            findings.append({"error": str(e)})
        
        return findings
    
    async def _scan_with_trivy(self, image_name: str) -> List[Dict]:
        """Scan image with Trivy"""
        findings = []
        
        try:
            result = subprocess.run(
                ['trivy', 'image', '--format', 'json', image_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for result_item in data.get('Results', []):
                    for vuln in result_item.get('Vulnerabilities', []):
                        findings.append({
                            "resource": image_name,
                            "type": "Docker Image",
                            "severity": vuln.get('Severity', 'Unknown'),
                            "issue": vuln.get('VulnerabilityID'),
                            "description": vuln.get('Description', 'No description')
                        })
        except:
            pass
        
        return findings

# Singleton instance
container_scanner = ContainerScanner()
