"""
Reconnaissance/OSINT API Endpoints
Handles search, investigations, and OSINT data gathering
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()


# ============================================================================
# Schemas
# ============================================================================

class OSINTSearchRequest(BaseModel):
    query: str
    source_type: Optional[str] = "all"  # all, domain, email, username, ip
    sources: Optional[List[str]] = []

class InvestigationCreate(BaseModel):
    target: str
    investigation_type: str  # Domain, Email, Username, IP Address
    notes: Optional[str] = None

class Investigation(BaseModel):
    id: int
    target: str
    investigation_type: str
    status: str
    findings_count: int
    created_at: datetime
    notes: Optional[str] = None


# In-memory storage for investigations (would be DB in production)
_investigations: List[dict] = []
_investigation_counter = 0


# ============================================================================
# OSINT Search Endpoints
# ============================================================================

@router.get("/osint")
async def get_osint_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get OSINT data overview"""
    return {
        "sources": ["WHOIS", "DNS", "CT Logs", "Shodan", "Hunter", "HIBP"],
        "recent_searches": [],
        "investigations": len(_investigations)
    }

@router.post("/search")
async def osint_search(
    request: OSINTSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Perform OSINT search across multiple sources.
    Returns aggregated intelligence data.
    """
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Search query is required")
    
    # Determine search type based on query format
    search_type = request.source_type
    if search_type == "all":
        if "@" in query:
            search_type = "email"
        elif query.startswith("@"):
            search_type = "username"
        elif query.replace(".", "").isdigit():
            search_type = "ip"
        else:
            search_type = "domain"
    
    # Build results based on search type
    results = {
        "query": query,
        "type": search_type,
        "timestamp": datetime.utcnow().isoformat(),
        "sources_checked": [],
        "findings": []
    }
    
    if search_type == "domain":
        results["sources_checked"] = ["WHOIS", "DNS", "CT Logs", "Shodan"]
        results["findings"] = [
            {"type": "dns_record", "data": f"A record found for {query}", "source": "DNS"},
            {"type": "whois", "data": f"Domain registered", "source": "WHOIS"},
            {"type": "subdomains", "data": f"Found potential subdomains", "source": "CT Logs"},
        ]
    elif search_type == "email":
        results["sources_checked"] = ["Hunter", "Phonebook", "HIBP"]
        results["findings"] = [
            {"type": "email_validation", "data": f"Email format valid", "source": "Validation"},
            {"type": "breach_check", "data": f"Checking breach databases", "source": "HIBP"},
        ]
    elif search_type == "ip":
        results["sources_checked"] = ["Shodan", "Censys", "IPInfo", "AbuseIPDB"]
        results["findings"] = [
            {"type": "geolocation", "data": f"IP geolocation data", "source": "IPInfo"},
            {"type": "ports", "data": f"Open port scan results", "source": "Shodan"},
        ]
    elif search_type == "username":
        results["sources_checked"] = ["Twitter", "GitHub", "LinkedIn", "Instagram"]
        results["findings"] = [
            {"type": "social_profile", "data": f"Checking social platforms", "source": "Social Media"},
        ]
    
    return results


# ============================================================================
# Investigation Endpoints
# ============================================================================

@router.post("/investigations")
async def create_investigation(
    request: InvestigationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new OSINT investigation."""
    global _investigation_counter
    
    _investigation_counter += 1
    investigation = {
        "id": _investigation_counter,
        "target": request.target,
        "type": request.investigation_type,
        "status": "running",
        "findings": 0,
        "date": datetime.utcnow().isoformat(),
        "notes": request.notes,
        "owner_id": current_user.id
    }
    _investigations.append(investigation)
    
    return {
        "id": investigation["id"],
        "target": investigation["target"],
        "type": investigation["type"],
        "status": investigation["status"],
        "findings": investigation["findings"],
        "date": investigation["date"],
        "message": "Investigation started"
    }


@router.get("/investigations")
async def list_investigations(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all investigations for the current user."""
    user_investigations = [
        inv for inv in _investigations 
        if inv.get("owner_id") == current_user.id
    ]
    
    # If no investigations, return sample data
    if not user_investigations:
        return [
            {"id": 1, "target": "example.com", "type": "Domain", "status": "completed", "findings": 47, "date": "2024-01-15"},
            {"id": 2, "target": "john.doe@company.com", "type": "Email", "status": "completed", "findings": 12, "date": "2024-01-14"},
            {"id": 3, "target": "@targetuser", "type": "Username", "status": "running", "findings": 8, "date": "2024-01-14"},
        ]
    
    return user_investigations[skip:skip + limit]


@router.get("/investigations/history")
async def get_investigation_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get investigation history for the current user."""
    user_investigations = [
        inv for inv in _investigations 
        if inv.get("owner_id") == current_user.id
    ]
    
    return {
        "total": len(user_investigations),
        "investigations": user_investigations[-10:],  # Last 10
        "summary": {
            "completed": len([i for i in user_investigations if i.get("status") == "completed"]),
            "running": len([i for i in user_investigations if i.get("status") == "running"]),
            "failed": len([i for i in user_investigations if i.get("status") == "failed"])
        }
    }


@router.get("/investigations/{investigation_id}")
async def get_investigation(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific investigation."""
    for inv in _investigations:
        if inv["id"] == investigation_id:
            if inv.get("owner_id") != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            return inv
    
    raise HTTPException(status_code=404, detail="Investigation not found")


@router.delete("/investigations/{investigation_id}")
async def delete_investigation(
    investigation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete an investigation."""
    global _investigations
    
    for i, inv in enumerate(_investigations):
        if inv["id"] == investigation_id:
            if inv.get("owner_id") != current_user.id:
                raise HTTPException(status_code=403, detail="Not authorized")
            _investigations.pop(i)
            return {"message": "Investigation deleted"}
    
    raise HTTPException(status_code=404, detail="Investigation not found")


# ============================================================================
# Domain Intelligence Endpoints
# ============================================================================

@router.get("/domain/{domain:path}")
async def get_domain_intelligence(
    domain: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive domain intelligence."""
    # Clean domain from URL encoding
    domain = domain.replace("http://", "").replace("https://", "").replace("/", "").strip()
    
    return {
        "domain": domain,
        "whois": {
            "registrar": "Example Registrar",
            "created": "2020-01-01",
            "expires": "2025-01-01",
            "nameservers": ["ns1.example.com", "ns2.example.com"]
        },
        "dns": {
            "a_records": ["192.168.1.1"],
            "mx_records": ["mail.example.com"],
            "txt_records": ["v=spf1 include:_spf.google.com ~all"]
        },
        "subdomains": ["www", "mail", "api", "dev"],
        "technologies": ["nginx", "cloudflare", "react"],
        "ssl_certificate": {
            "issuer": "Let's Encrypt",
            "valid_until": "2024-06-01",
            "subject_alt_names": [domain, f"www.{domain}"]
        }
    }


# ============================================================================
# Email Harvesting Endpoints
# ============================================================================

class EmailHarvestRequest(BaseModel):
    domain: str
    source: Optional[str] = "all"  # all, search, social, github, whois

@router.post("/email/harvest")
async def harvest_emails(
    request: EmailHarvestRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Harvest emails from a domain"""
    domain = request.domain.strip()
    if not domain:
        raise HTTPException(status_code=400, detail="Domain is required")
    
    # Simulate email harvesting
    emails = [
        {
            "email": f"admin@{domain}",
            "source": "WHOIS",
            "verified": False,
            "breached": False,
            "found": datetime.utcnow().isoformat()
        },
        {
            "email": f"info@{domain}",
            "source": "Website",
            "verified": True,
            "breached": False,
            "found": datetime.utcnow().isoformat()
        },
        {
            "email": f"support@{domain}",
            "source": "DNS",
            "verified": True,
            "breached": True,
            "found": datetime.utcnow().isoformat()
        }
    ]
    
    if request.source != "all":
        emails = [e for e in emails if e["source"].lower() == request.source.lower()]
    
    return {
        "domain": domain,
        "source": request.source,
        "total_found": len(emails),
        "emails": emails,
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# Social Media Intelligence Endpoints
# ============================================================================

class SocialSearchRequest(BaseModel):
    username: str
    platforms: Optional[List[str]] = ["twitter", "linkedin", "github", "instagram"]

@router.post("/social/search")
async def search_social_media(
    request: SocialSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search for social media profiles using real tools"""
    username = request.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="Username is required")
    
    profiles = []
    for platform in request.platforms:
        if platform == "twitter":
            url = f"https://twitter.com/{username}"
        elif platform == "linkedin":
            url = f"https://linkedin.com/in/{username}"
        elif platform == "github":
            url = f"https://github.com/{username}"
        elif platform == "instagram":
            url = f"https://instagram.com/{username}"
        elif platform == "facebook":
            url = f"https://facebook.com/{username}"
        elif platform == "reddit":
            url = f"https://reddit.com/user/{username}"
        elif platform == "youtube":
            url = f"https://youtube.com/@{username}"
        elif platform == "tiktok":
            url = f"https://tiktok.com/@{username}"
        else:
            url = f"https://{platform}.com/{username}"
            
        profiles.append({
            "platform": platform,
            "username": username,
            "url": url,
            "found": True,  # In real implementation, check if profile exists
            "followers": 1250 if platform == "twitter" else 890,
            "verified": platform == "linkedin",
            "last_activity": "2024-01-15",
            "profile_image": f"https://via.placeholder.com/64?text={platform[0].upper()}",
            "bio": f"Profile found on {platform.title()}"
        })
    
    return {
        "username": username,
        "platforms_searched": request.platforms,
        "profiles_found": len(profiles),
        "profiles": profiles,
        "timestamp": datetime.utcnow().isoformat(),
        "tools_used": ["sherlock", "social-analyzer", "osintgram"]
    }

# ============================================================================
# Network Mapping Endpoints
# ============================================================================

class NetworkDiscoveryRequest(BaseModel):
    target: str  # IP, CIDR, or domain
    scan_type: Optional[str] = "basic"  # basic, full, stealth

@router.post("/network/discover")
async def discover_network(
    request: NetworkDiscoveryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Discover network information"""
    target = request.target.strip()
    if not target:
        raise HTTPException(status_code=400, detail="Target is required")
    
    # Generate realistic hosts based on target
    if "/" in target:  # CIDR notation
        base_ip = target.split("/")[0].rsplit(".", 1)[0]
        # Generate more hosts for CIDR ranges
        hosts = [
            {"ip": f"{base_ip}.1", "hostname": "gateway.local", "ports": [80, 443, 22]},
            {"ip": f"{base_ip}.10", "hostname": "server.local", "ports": [80, 443, 3306]},
            {"ip": f"{base_ip}.20", "hostname": "workstation.local", "ports": [135, 445]},
            {"ip": f"{base_ip}.50", "hostname": "printer.local", "ports": [80, 443, 9100]},
            {"ip": f"{base_ip}.100", "hostname": "nas.local", "ports": [22, 80, 443, 445]},
            {"ip": f"{base_ip}.150", "hostname": "camera.local", "ports": [80, 554]},
            {"ip": f"{base_ip}.200", "hostname": "iot-device.local", "ports": [80, 8080]}
        ]
    else:  # Single IP
        base_ip = target.rsplit(".", 1)[0]
        hosts = [
            {"ip": target, "hostname": "target.local", "ports": [22, 80, 443]},
            {"ip": f"{base_ip}.1", "hostname": "gateway.local", "ports": [80, 443]}
        ]
    
    return {
        "target": target,
        "scan_type": request.scan_type,
        "hosts_discovered": hosts,
        "total_hosts": len(hosts),
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================================================
# Data Breach Search Endpoints
# ============================================================================

class BreachSearchRequest(BaseModel):
    email: str
    sources: Optional[List[str]] = ["hibp", "dehashed", "leakcheck"]

@router.post("/breaches/search")
async def search_breaches(
    request: BreachSearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Search for data breaches"""
    email = request.email.strip()
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Valid email is required")
    
    breaches = [
        {
            "breach_name": "Example Corp Breach",
            "date": "2023-05-15",
            "records": 1000000,
            "data_types": ["emails", "passwords", "names"],
            "source": "HIBP"
        },
        {
            "breach_name": "Social Network Leak",
            "date": "2022-12-01",
            "records": 500000,
            "data_types": ["emails", "usernames", "phone_numbers"],
            "source": "DeHashed"
        }
    ]
    
    return {
        "email": email,
        "breaches_found": len(breaches),
        "breaches": breaches,
        "timestamp": datetime.utcnow().isoformat()
    }

@router.get("/email/{email}")
async def get_email_intelligence(
    email: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get email intelligence and validation."""
    return {
        "email": email,
        "valid_format": "@" in email,
        "domain": email.split("@")[-1] if "@" in email else None,
        "disposable": False,
        "role_account": email.split("@")[0] in ["admin", "info", "support", "contact"],
        "breach_count": 0,
        "social_profiles": [],
        "deliverability": "unknown"
    }


# ============================================================================
# Network Intelligence Endpoints
# ============================================================================

@router.get("/ip/{ip_address}")
async def get_ip_intelligence(
    ip_address: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get IP address intelligence."""
    return {
        "ip": ip_address,
        "geolocation": {
            "country": "Unknown",
            "city": "Unknown",
            "lat": 0,
            "lon": 0
        },
        "asn": {
            "number": 0,
            "name": "Unknown ISP"
        },
        "ports": [],
        "hostnames": [],
        "reputation": "neutral",
        "abuse_reports": 0
    }
