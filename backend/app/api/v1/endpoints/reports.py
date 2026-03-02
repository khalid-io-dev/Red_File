from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any, Dict, List, Optional
from app.db.session import get_db
from app.services.pdf_exporter import pdf_exporter
from app.models.user import User
from app.models.report import Report, ReportTypeEnum, ReportFormatEnum
from app.models.finding import Finding
from app.models.credential import Credential
from app.api.deps import get_current_user
from pydantic import BaseModel
from datetime import datetime
import json
import os

router = APIRouter()

class ReportGenerate(BaseModel):
    title: Optional[str] = None
    report_type: str = "technical"
    format: str = "json"
    campaign_id: Optional[int] = None
    scan_id: Optional[int] = None
    campaign_ids: Optional[List[int]] = None
    scan_ids: Optional[List[int]] = None
    finding_ids: Optional[List[int]] = None
    options: Optional[Dict[str, Any]] = None

@router.post("/generate")
async def generate_report(
    request: ReportGenerate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report_type = (request.report_type or "technical").lower()
    report_format = (request.format or "json").lower()

    scan_ids: List[int] = []
    if request.scan_ids:
        scan_ids.extend([sid for sid in request.scan_ids if sid is not None])
    if request.scan_id is not None:
        scan_ids.append(request.scan_id)
    scan_ids = list(dict.fromkeys(scan_ids))

    campaign_ids: List[int] = []
    if request.campaign_ids:
        campaign_ids.extend([cid for cid in request.campaign_ids if cid is not None])
    if request.campaign_id is not None:
        campaign_ids.append(request.campaign_id)
    campaign_ids = list(dict.fromkeys(campaign_ids))
    campaign_ids_str = [str(cid) for cid in campaign_ids]

    findings_query = select(Finding).where(Finding.owner_id == current_user.id)
    if scan_ids:
        findings_query = findings_query.where(Finding.scan_id.in_(scan_ids))
    if campaign_ids_str:
        findings_query = findings_query.where(Finding.campaign_id.in_(campaign_ids_str))
    if request.finding_ids:
        findings_query = findings_query.where(Finding.id.in_(request.finding_ids))

    findings_result = await db.execute(findings_query)
    findings = findings_result.scalars().all()

    creds_query = select(Credential).where(Credential.owner_id == current_user.id)
    if scan_ids:
        creds_query = creds_query.where(Credential.scan_id.in_(scan_ids))
    if campaign_ids_str:
        creds_query = creds_query.where(Credential.campaign_id.in_(campaign_ids_str))

    creds_result = await db.execute(creds_query)
    credentials = creds_result.scalars().all()

    findings_data = [
        {
            "id": f.id,
            "title": f.title,
            "severity": f.severity.value if getattr(f, "severity", None) is not None else None,
            "status": f.status.value if getattr(f, "status", None) is not None else None,
            "target": f.target,
            "tool": f.tool,
            "description": f.description,
            "cve_id": f.cve_id,
            "cvss_score": f.cvss_score,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in findings
    ]

    credentials_data = [
        {
            "id": c.id,
            "username": c.username,
            "service": c.service,
            "target": c.target,
            "is_valid": c.is_valid,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in credentials
    ]

    severity_counts: Dict[str, int] = {}
    for f in findings_data:
        sev = (f.get("severity") or "info").lower()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    title = request.title or f"{report_type.title()} Report - {datetime.now().strftime('%Y-%m-%d')}"

    report_payload: Dict[str, Any] = {
        "title": title,
        "report_type": report_type,
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "total_findings": len(findings_data),
            "severity": severity_counts,
            "total_credentials": len(credentials_data),
        },
        "filters": {
            "scan_ids": scan_ids,
            "campaign_ids": campaign_ids,
            "finding_ids": request.finding_ids or [],
        },
        "findings": findings_data,
        "credentials": credentials_data,
        "options": request.options or {},
    }

    content: Optional[str] = None
    file_path: Optional[str] = None

    if report_format == "pdf":
        summary_text = (
            f"Total findings: {len(findings_data)}. "
            f"Critical: {severity_counts.get('critical', 0)}, High: {severity_counts.get('high', 0)}, "
            f"Medium: {severity_counts.get('medium', 0)}, Low: {severity_counts.get('low', 0)}."
        )
        pdf_data = {
            "title": title,
            "type": report_type,
            "target": "Multiple" if findings_data else "N/A",
            "summary": summary_text,
            "findings": findings_data,
            "credentials": credentials_data,
        }
        file_path = pdf_exporter.generate_report(pdf_data, f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    elif report_format == "markdown":
        lines: List[str] = []
        lines.append(f"# {title}")
        lines.append("")
        lines.append(f"**Type:** {report_type}")
        lines.append(f"**Generated:** {report_payload['generated_at']}")
        lines.append("")
        lines.append("## Summary")
        lines.append(f"- Total findings: {report_payload['summary']['total_findings']}")
        lines.append(f"- Total credentials: {report_payload['summary']['total_credentials']}")
        lines.append("")
        lines.append("### Severity")
        for k, v in sorted(severity_counts.items(), key=lambda x: x[0]):
            lines.append(f"- {k}: {v}")
        lines.append("")
        lines.append("## Findings")
        for f in findings_data[:100]:
            lines.append(f"### {f.get('title')}")
            lines.append(f"- Severity: {f.get('severity')}")
            if f.get("target"):
                lines.append(f"- Target: {f.get('target')}")
            if f.get("tool"):
                lines.append(f"- Tool: {f.get('tool')}")
            if f.get("cve_id"):
                lines.append(f"- CVE: {f.get('cve_id')}")
            if f.get("cvss_score"):
                lines.append(f"- CVSS: {f.get('cvss_score')}")
            if f.get("description"):
                lines.append("")
                lines.append(f"{f.get('description')}")
            lines.append("")
        content = "\n".join(lines)
    elif report_format == "html":
        content = f"<html><body><pre>{json.dumps(report_payload, indent=2)}</pre></body></html>"
    else:
        content = json.dumps(report_payload, indent=2)

    report_type_enum = ReportTypeEnum.TECHNICAL
    if report_type in ["executive", "executive_summary"]:
        report_type_enum = ReportTypeEnum.EXECUTIVE
    elif report_type == "compliance":
        report_type_enum = ReportTypeEnum.COMPLIANCE

    try:
        format_enum = ReportFormatEnum[report_format.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid report format: {request.format}")

    db_report = Report(
        title=title,
        report_type=report_type_enum,
        format=format_enum,
        content=content,
        file_path=file_path,
        campaign_id=campaign_ids[0] if len(campaign_ids) == 1 else None,
        scan_id=scan_ids[0] if len(scan_ids) == 1 else None,
        owner_id=current_user.id,
    )

    db.add(db_report)
    await db.commit()
    await db.refresh(db_report)

    return {
        "id": db_report.id,
        "title": db_report.title,
        "format": db_report.format.value,
        "status": "completed",
        "created_at": db_report.created_at.isoformat() if db_report.created_at else None,
        "file_path": db_report.file_path,
    }

@router.get("/")
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Report).where(Report.owner_id == current_user.id).order_by(Report.created_at.desc())
    )
    reports = result.scalars().all()

    return [
        {
            "id": r.id,
            "title": r.title,
            "format": r.format.value,
            "status": "completed",
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "file_path": r.file_path,
        }
        for r in reports
    ]

@router.get("/{report_id}")
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.owner_id == current_user.id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return {
        "id": report.id,
        "title": report.title,
        "format": report.format.value,
        "status": "completed",
        "created_at": report.created_at.isoformat() if report.created_at else None,
        "file_path": report.file_path,
        "content": report.content,
    }

@router.get("/{report_id}/download")
async def download_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.owner_id == current_user.id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    safe_name = f"report-{report.id}"
    if report.title:
        safe_name = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in report.title]).strip("_") or safe_name

    if report.format == ReportFormatEnum.PDF:
        if not report.file_path:
            raise HTTPException(status_code=404, detail="Report file not available")
        if not os.path.exists(report.file_path):
            raise HTTPException(status_code=404, detail="Report file not found")
        return FileResponse(
            report.file_path,
            media_type="application/pdf",
            filename=f"{safe_name}.pdf",
        )

    if report.format == ReportFormatEnum.MARKDOWN:
        return Response(
            content=report.content or "",
            media_type="text/markdown",
            headers={"Content-Disposition": f'attachment; filename="{safe_name}.md"'},
        )

    if report.format == ReportFormatEnum.HTML:
        return Response(
            content=report.content or "",
            media_type="text/html",
            headers={"Content-Disposition": f'attachment; filename="{safe_name}.html"'},
        )

    return Response(
        content=report.content or "{}",
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{safe_name}.json"'},
    )
