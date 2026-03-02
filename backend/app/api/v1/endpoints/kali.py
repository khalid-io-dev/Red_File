from fastapi import APIRouter, Depends, BackgroundTasks
from typing import Any, Optional, Dict
from pydantic import BaseModel
from app.api import deps
from app.models.user import User
from app.services.kali_executor import kali_executor
import uuid

router = APIRouter()

class NmapRequest(BaseModel):
    target: str
    scan_type: Optional[str] = "quick"
    ports: Optional[str] = None

class SQLMapRequest(BaseModel):
    url: str
    data: Optional[str] = None
    cookie: Optional[str] = None

class NiktoRequest(BaseModel):
    target: str

class GobusterRequest(BaseModel):
    url: str
    wordlist: Optional[str] = None

class HydraRequest(BaseModel):
    target: str
    service: str
    username: Optional[str] = None
    password_list: Optional[str] = None

class JohnRequest(BaseModel):
    hash_file: str
    format: Optional[str] = None

class HashcatRequest(BaseModel):
    hash: str
    attack_mode: Optional[int] = 0
    hash_type: Optional[int] = 0

# Task storage (in production, use Redis or database)
tasks = {}

@router.post("/nmap")
async def run_nmap(
    request: NmapRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_nmap(request.target, request.scan_type, request.ports)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/sqlmap")
async def run_sqlmap(
    request: SQLMapRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_sqlmap(request.url, request.data, request.cookie)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/nikto")
async def run_nikto(
    request: NiktoRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_nikto(request.target)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/gobuster")
async def run_gobuster(
    request: GobusterRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_gobuster(request.url, request.wordlist)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/hydra")
async def run_hydra(
    request: HydraRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_hydra(request.target, request.service, request.username, request.password_list)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/john")
async def run_john(
    request: JohnRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_john(request.hash_file, request.format)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.post("/hashcat")
async def run_hashcat(
    request: HashcatRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "running", "result": None}
    
    async def execute():
        result = await kali_executor.run_hashcat(request.hash, request.attack_mode, request.hash_type)
        tasks[task_id] = {"status": "completed", "result": result}
    
    background_tasks.add_task(execute)
    return {"task_id": task_id, "status": "running"}

@router.get("/status/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    if task_id not in tasks:
        return {"error": "Task not found"}
    return tasks[task_id]
