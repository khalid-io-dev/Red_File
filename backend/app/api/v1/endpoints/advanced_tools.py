from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import logging

from app.api import deps
from app.services.reverse_engineering import reverse_engineering_service
from app.services.advanced_web_tools import advanced_web_tools_service
from app.services.network_tools import network_tools_service

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter()

# Request Models
class BinaryAnalysisRequest(BaseModel):
    binary_path: str
    analysis_type: str = "full"  # full, strings, radare2, ghidra, checksec

class WebScanRequest(BaseModel):
    target_url: str
    scan_type: str = "full"  # full, zap, nosql, jwt, xss, ssrf

class JWTAnalysisRequest(BaseModel):
    token: str
    crack: bool = False
    wordlist: Optional[str] = None

class ADAssessmentRequest(BaseModel):
    domain: str
    username: str
    password: str
    assessment_type: str = "full"  # full, bloodhound, mimikatz, kerberoast

class NetworkScanRequest(BaseModel):
    target: str
    scan_type: str = "vuln"  # vuln, smb, openvas

# Reverse Engineering Endpoints
@router.post("/reverse-engineering/analyze")
async def analyze_binary(
    request: BinaryAnalysisRequest,
    current_user = Depends(deps.get_current_user)
):
    """Analyze binary with reverse engineering tools"""
    logger.info(f"[analyze_binary] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[analyze_binary] Binary path: {request.binary_path}, Analysis type: {request.analysis_type}")
    try:
        if request.analysis_type == "full":
            result = await reverse_engineering_service.full_binary_analysis(request.binary_path)
        elif request.analysis_type == "strings":
            result = await reverse_engineering_service.strings_analysis(request.binary_path)
        elif request.analysis_type == "radare2":
            result = await reverse_engineering_service.radare2_analyze(request.binary_path)
        elif request.analysis_type == "ghidra":
            result = await reverse_engineering_service.ghidra_analyze(request.binary_path)
        elif request.analysis_type == "checksec":
            result = await reverse_engineering_service.checksec_analyze(request.binary_path)
        else:
            raise HTTPException(status_code=400, detail="Invalid analysis type")

        logger.info(f"[analyze_binary] Analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"[analyze_binary] Error during analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reverse-engineering/upload")
async def upload_binary(
    file: UploadFile = File(...),
    current_user = Depends(deps.get_current_user)
):
    """Upload binary for analysis"""
    logger.info(f"[upload_binary] Upload request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[upload_binary] File: {file.filename if file else 'None'}")
    try:
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        logger.info(f"[upload_binary] File saved to {file_path}, starting analysis...")

        result = await reverse_engineering_service.full_binary_analysis(file_path)
        logger.info(f"[upload_binary] Analysis completed successfully")
        return {"file_path": file_path, "analysis": result}
    except Exception as e:
        logger.error(f"[upload_binary] Error during upload/analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Advanced Web Tools Endpoints
@router.post("/web-tools/scan")
async def web_security_scan(
    request: WebScanRequest,
    current_user = Depends(deps.get_current_user)
):
    """Advanced web application security testing"""
    logger.info(f"[web_security_scan] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[web_security_scan] Target URL: {request.target_url}, Scan type: {request.scan_type}")
    try:
        if request.scan_type == "full":
            result = await advanced_web_tools_service.full_web_assessment(request.target_url)
        elif request.scan_type == "zap":
            result = await advanced_web_tools_service.zap_active_scan(request.target_url)
        elif request.scan_type == "nosql":
            result = await advanced_web_tools_service.nosqlmap_scan(request.target_url)
        elif request.scan_type == "xss":
            result = await advanced_web_tools_service.xsstrike_scan(request.target_url)
        elif request.scan_type == "ssrf":
            result = await advanced_web_tools_service.ssrf_test(request.target_url)
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        logger.info(f"[web_security_scan] Scan completed successfully")
        return result
    except Exception as e:
        logger.error(f"[web_security_scan] Error during scan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/web-tools/jwt/analyze")
async def analyze_jwt(
    request: JWTAnalysisRequest,
    current_user = Depends(deps.get_current_user)
):
    """Analyze JWT token"""
    logger.info(f"[analyze_jwt] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[analyze_jwt] Crack: {request.crack}")
    try:
        if request.crack:
            result = await advanced_web_tools_service.jwt_crack(request.token, request.wordlist)
        else:
            result = await advanced_web_tools_service.jwt_analyze(request.token)

        logger.info(f"[analyze_jwt] JWT analysis completed successfully")
        return result
    except Exception as e:
        logger.error(f"[analyze_jwt] Error during JWT analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/web-tools/wfuzz")
async def web_fuzzing(
    target_url: str,
    wordlist: Optional[str] = None,
    current_user = Depends(deps.get_current_user)
):
    """Web fuzzing with wfuzz"""
    logger.info(f"[web_fuzzing] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[web_fuzzing] Target URL: {target_url}")
    try:
        result = await advanced_web_tools_service.wfuzz_scan(target_url, wordlist)
        logger.info(f"[web_fuzzing] Fuzzing completed successfully")
        return result
    except Exception as e:
        logger.error(f"[web_fuzzing] Error during fuzzing: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Network Tools Endpoints
@router.post("/network-tools/ad-assessment")
async def active_directory_assessment(
    request: ADAssessmentRequest,
    current_user = Depends(deps.get_current_user)
):
    """Active Directory penetration testing"""
    logger.info(f"[ad_assessment] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[ad_assessment] Domain: {request.domain}, Type: {request.assessment_type}")
    try:
        if request.assessment_type == "full":
            result = await network_tools_service.full_ad_assessment(
                request.domain, request.username, request.password
            )
        elif request.assessment_type == "bloodhound":
            result = await network_tools_service.bloodhound_collect(
                request.domain, request.username, request.password
            )
        elif request.assessment_type == "mimikatz":
            result = await network_tools_service.mimikatz_dump_creds(
                request.domain, request.username, request.password
            )
        elif request.assessment_type == "kerberoast":
            result = await network_tools_service.kerberoast_attack(
                request.domain, request.username, request.password
            )
        else:
            raise HTTPException(status_code=400, detail="Invalid assessment type")

        logger.info(f"[ad_assessment] Assessment completed successfully")
        return result
    except Exception as e:
        logger.error(f"[ad_assessment] Error during assessment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network-tools/scan")
async def network_scan(
    request: NetworkScanRequest,
    current_user = Depends(deps.get_current_user)
):
    """Network vulnerability scanning"""
    logger.info(f"[network_scan] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[network_scan] Target: {request.target}, Type: {request.scan_type}")
    try:
        if request.scan_type == "vuln":
            result = await network_tools_service.nmap_vuln_scan(request.target)
        elif request.scan_type == "smb":
            result = await network_tools_service.crackmapexec_scan(request.target)
        elif request.scan_type == "openvas":
            result = await network_tools_service.openvas_scan(request.target)
        else:
            raise HTTPException(status_code=400, detail="Invalid scan type")

        logger.info(f"[network_scan] Scan completed successfully")
        return result
    except Exception as e:
        logger.error(f"[network_scan] Error during scan: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network-tools/responder")
async def capture_hashes(
    interface: str = "eth0",
    duration: int = 60,
    current_user = Depends(deps.get_current_user)
):
    """Capture NTLM hashes with Responder"""
    logger.info(f"[capture_hashes] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[capture_hashes] Interface: {interface}, Duration: {duration}")
    try:
        result = await network_tools_service.responder_capture(interface, duration)
        logger.info(f"[capture_hashes] Capture completed successfully")
        return result
    except Exception as e:
        logger.error(f"[capture_hashes] Error during capture: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/network-tools/kerbrute")
async def kerberos_enumeration(
    domain: str,
    userlist: Optional[str] = None,
    current_user = Depends(deps.get_current_user)
):
    """Kerberos user enumeration"""
    logger.info(f"[kerberos_enumeration] Request received from user: {current_user.id if current_user else 'None'}")
    logger.info(f"[kerberos_enumeration] Domain: {domain}")
    try:
        result = await network_tools_service.kerbrute_enum(domain, userlist)
        logger.info(f"[kerberos_enumeration] Enumeration completed successfully")
        return result
    except Exception as e:
        logger.error(f"[kerberos_enumeration] Error during enumeration: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/reverse-engineering/tools")
async def get_reverse_engineering_tools(current_user = Depends(deps.get_current_user)):
    """Get available reverse engineering tools"""
    logger.info(f"[get_reverse_engineering_tools] Request from user: {current_user.id if current_user else 'None'}")
    return {
        "tools": ["ghidra", "radare2", "binwalk", "strings", "checksec", "objdump", "strace"],
        "ai_models": ["qwen2.5-coder:7b", "deepseek-coder:6.7b", "glm-4.7-flash"]
    }

@router.get("/tools/status")
async def get_tools_status(current_user = Depends(deps.get_current_user)):
    """Get status of all advanced tools"""
    logger.info(f"[get_tools_status] Request from user: {current_user.id if current_user else 'None'}")
    return {
        "reverse_engineering": {
            "available": ["ghidra", "radare2", "binwalk", "strings", "checksec", "objdump", "strace"],
            "ai_models": ["qwen2.5-coder:7b", "deepseek-coder:6.7b", "glm-4.7-flash"]
        },
        "web_tools": {
            "available": ["zap", "nosqlmap", "jwt-tools", "wfuzz", "commix", "xsstrike"],
            "ai_models": ["qwen2.5-coder:7b", "deepseek-coder:6.7b", "glm-4.7-flash"]
        },
        "network_tools": {
            "available": ["bloodhound", "mimikatz", "crackmapexec", "responder", "kerbrute", "openvas"],
            "ai_models": ["qwen2.5-coder:7b", "deepseek-coder:6.7b", "glm-4.7-flash"]
        }
    }
