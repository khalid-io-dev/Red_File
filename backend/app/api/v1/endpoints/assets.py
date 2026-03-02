from fastapi import APIRouter, Depends, HTTPException
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.asset_manager import asset_manager

router = APIRouter()

class AssetCreate(BaseModel):
    name: str
    type: str
    ip_address: Optional[str] = None
    mac_address: Optional[str] = None
    hostname: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    criticality: Optional[str] = "medium"
    status: Optional[str] = "active"
    services: Optional[List[Dict]] = []
    open_ports: Optional[List[int]] = []
    metadata: Optional[Dict] = {}

class AssetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    ip_address: Optional[str] = None
    hostname: Optional[str] = None
    os: Optional[str] = None
    location: Optional[str] = None
    owner: Optional[str] = None
    criticality: Optional[str] = None
    status: Optional[str] = None

class AssetGroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    asset_ids: List[str] = []

@router.get("/")
async def list_assets(
    type: Optional[str] = None,
    criticality: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    filters = {}
    if type: filters['type'] = type
    if criticality: filters['criticality'] = criticality
    if status: filters['status'] = status
    if location: filters['location'] = location
    
    return await asset_manager.get_assets(filters)

@router.post("/")
async def create_asset(
    asset: AssetCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.add_asset(asset.model_dump())

@router.put("/{asset_id}")
async def update_asset(
    asset_id: str,
    updates: AssetUpdate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.update_asset(asset_id, updates.model_dump(exclude_unset=True))
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.delete("/{asset_id}")
async def delete_asset(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.delete_asset(asset_id)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.post("/discover")
async def discover_assets(
    network_range: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.discover_assets(network_range)

@router.get("/{asset_id}/health")
async def get_asset_health(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.get_asset_health(asset_id)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.get("/{asset_id}/dependencies")
async def get_asset_dependencies(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.get_asset_dependencies(asset_id)

@router.get("/{asset_id}/risk")
async def get_asset_risk(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.calculate_asset_risk(asset_id)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.get("/{asset_id}/timeline")
async def get_asset_timeline(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.get_asset_timeline(asset_id)

@router.post("/{asset_id}/scan")
async def scan_asset(
    asset_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.scan_asset(asset_id)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.post("/{asset_id}/tags")
async def tag_asset(
    asset_id: str,
    tags: List[str],
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    result = await asset_manager.tag_asset(asset_id, tags)
    if 'error' in result:
        raise HTTPException(status_code=404, detail=result['error'])
    return result

@router.get("/statistics")
async def get_statistics(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.get_asset_statistics()

@router.get("/search")
async def search_assets(
    q: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.search_assets(q)

@router.post("/groups")
async def create_asset_group(
    group: AssetGroupCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.create_asset_group(group.model_dump())

@router.get("/groups")
async def list_asset_groups(
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.get_asset_groups()

@router.post("/export")
async def export_inventory(
    format: str = "json",
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.export_inventory(format)

@router.post("/import")
async def import_inventory(
    file_path: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    return await asset_manager.import_inventory(file_path)
