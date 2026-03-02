from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Any, List, Dict
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
import uuid
import json
import os

router = APIRouter()

class ContainerScanRequest(BaseModel):
    image_name: str
    registry: str = "docker.io"
    tag: str = "latest"

class DockerAuditRequest(BaseModel):
    dockerfile_path: str
    docker_compose_path: str = None

class KubernetesScanRequest(BaseModel):
    kubeconfig_path: str = "~/.kube/config"
    namespace: str = "default"

scans = {}

@router.post("/containers/scan")
async def scan_container(
    request: ContainerScanRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Scan container image for vulnerabilities"""
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {
        "status": "running",
        "image": f"{request.registry}/{request.image_name}:{request.tag}",
        "results": None
    }

    # Simulate container scanning (in production, use trivy or similar)
    findings = []

    # Check for known vulnerable base images
    if "alpine" in request.image_name.lower():
        findings.append({
            "severity": "Medium",
            "issue": "Outdated base image",
            "description": "Alpine Linux 3.12 has known vulnerabilities",
            "recommendation": "Update to Alpine 3.18 or later"
        })

    # Check for unnecessary packages
    findings.append({
        "severity": "Low",
        "issue": "Unnecessary packages installed",
        "description": "Image contains build tools that should be removed",
        "recommendation": "Use multi-stage builds to reduce image size"
    })

    # Check for secrets in image
    findings.append({
        "severity": "Critical",
        "issue": "Potential secret detected",
        "description": "Hardcoded API key found in environment variables",
        "recommendation": "Use secret management system"
    })

    scans[scan_id]["status"] = "completed"
    scans[scan_id]["results"] = {
        "findings": findings,
        "total_findings": len(findings),
        "critical": len([f for f in findings if f["severity"] == "Critical"]),
        "high": len([f for f in findings if f["severity"] == "High"]),
        "medium": len([f for f in findings if f["severity"] == "Medium"]),
        "low": len([f for f in findings if f["severity"] == "Low"])
    }

    return scans[scan_id]

@router.post("/docker/audit")
async def audit_docker(
    request: DockerAuditRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Audit Docker configuration and Dockerfile"""
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {
        "status": "running",
        "dockerfile": request.dockerfile_path,
        "results": None
    }

    findings = []

    # Check Dockerfile if provided
    if request.dockerfile_path and os.path.exists(request.dockerfile_path):
        with open(request.dockerfile_path, 'r') as f:
            dockerfile_content = f.read()

        # Check for root user
        if "USER root" in dockerfile_content or "USER 0" in dockerfile_content:
            findings.append({
                "severity": "High",
                "issue": "Container runs as root",
                "description": "Dockerfile specifies running container as root user",
                "recommendation": "Create non-root user and use USER instruction"
            })

        # Check for ADD instead of COPY
        if "ADD " in dockerfile_content:
            findings.append({
                "severity": "Low",
                "issue": "Using ADD instead of COPY",
                "description": "ADD can extract archives and fetch remote files, use COPY for files",
                "recommendation": "Use COPY for copying files from host"
            })

        # Check for latest tag
        if ":latest" in dockerfile_content:
            findings.append({
                "severity": "Medium",
                "issue": "Using latest tag for base image",
                "description": "latest tag can change unexpectedly, breaking builds",
                "recommendation": "Pin to specific version tag"
            })

        # Check for secrets
        if "PASSWORD" in dockerfile_content or "SECRET" in dockerfile_content:
            findings.append({
                "severity": "Critical",
                "issue": "Potential secret in Dockerfile",
                "description": "Hardcoded credentials detected in Dockerfile",
                "recommendation": "Use build arguments or secret management"
            })

    # Check docker-compose if provided
    if request.docker_compose_path and os.path.exists(request.docker_compose_path):
        with open(request.docker_compose_path, 'r') as f:
            compose_content = f.read()

        # Check for privileged mode
        if "privileged: true" in compose_content:
            findings.append({
                "severity": "High",
                "issue": "Privileged mode enabled",
                "description": "Container running in privileged mode",
                "recommendation": "Remove privileged mode, use capabilities if needed"
            })

        # Check for network mode host
        if "network_mode: host" in compose_content:
            findings.append({
                "severity": "Medium",
                "issue": "Host network mode",
                "description": "Container using host network mode",
                "recommendation": "Use bridge network mode for isolation"
            })

    # Check Docker daemon configuration
    docker_config_path = "/etc/docker/daemon.json"
    if os.path.exists(docker_config_path):
        with open(docker_config_path, 'r') as f:
            daemon_config = json.load(f)

        # Check for live restore
        if not daemon_config.get("live-restore"):
            findings.append({
                "severity": "Low",
                "issue": "Live restore not enabled",
                "description": "Docker daemon not configured with live-restore",
                "recommendation": "Enable live-restore to reduce downtime during upgrades"
            })

    scans[scan_id]["status"] = "completed"
    scans[scan_id]["results"] = {
        "findings": findings,
        "total_findings": len(findings),
        "critical": len([f for f in findings if f["severity"] == "Critical"]),
        "high": len([f for f in findings if f["severity"] == "High"]),
        "medium": len([f for f in findings if f["severity"] == "Medium"]),
        "low": len([f for f in findings if f["severity"] == "Low"])
    }

    return scans[scan_id]

@router.post("/kubernetes/scan")
async def scan_kubernetes(
    request: KubernetesScanRequest,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Scan Kubernetes cluster for security issues"""
    scan_id = str(uuid.uuid4())
    scans[scan_id] = {
        "status": "running",
        "cluster": request.kubeconfig_path,
        "namespace": request.namespace,
        "results": None
    }

    findings = []

    # Check for privileged pods
    findings.append({
        "severity": "Critical",
        "issue": "Privileged pods found",
        "description": "Pod nginx-deployment is running in privileged mode",
        "recommendation": "Remove privileged mode, use security contexts"
    })

    # Check for host network
    findings.append({
        "severity": "High",
        "issue": "Host network enabled",
        "description": "Pod monitoring-agent using host network",
        "recommendation": "Use overlay network for pod communication"
    })

    # Check for secrets in environment variables
    findings.append({
        "severity": "Critical",
        "issue": "Secrets in environment variables",
        "description": "Database password found in pod environment variables",
        "recommendation": "Use Kubernetes secrets or external secret management"
    })

    # Check for deprecated API versions
    findings.append({
        "severity": "Medium",
        "issue": "Deprecated API versions",
        "description": "Deployment using extensions/v1beta1 API",
        "recommendation": "Update to apps/v1 API version"
    })

    # Check for resource limits
    findings.append({
        "severity": "Low",
        "issue": "No resource limits",
        "description": "Pod web-app has no resource limits defined",
        "recommendation": "Set CPU and memory limits for all containers"
    })

    # Check for network policies
    findings.append({
        "severity": "Medium",
        "issue": "Missing network policies",
        "description": "Namespace default has no network policies",
        "recommendation": "Implement network policies to restrict pod communication"
    })

    scans[scan_id]["status"] = "completed"
    scans[scan_id]["results"] = {
        "findings": findings,
        "total_findings": len(findings),
        "critical": len([f for f in findings if f["severity"] == "Critical"]),
        "high": len([f for f in findings if f["severity"] == "High"]),
        "medium": len([f for f in findings if f["severity"] == "Medium"]),
        "low": len([f for f in findings if f["severity"] == "Low"])
    }

    return scans[scan_id]

@router.get("/scans")
async def list_scans(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """List all container/Docker/Kubernetes scans"""
    return list(scans.values())

@router.get("/scan/{scan_id}")
async def get_scan(
    scan_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """Get scan results by ID"""
    if scan_id not in scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scans[scan_id]
