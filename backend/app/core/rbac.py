from functools import wraps
from fastapi import HTTPException, Depends
from app.models.user import User
from app.api.deps import get_current_user

PERMISSIONS = {
    "admin": [
        "scans:read", "scans:write", "scans:delete",
        "campaigns:read", "campaigns:write", "campaigns:delete",
        "findings:read", "findings:write", "findings:delete",
        "credentials:read", "credentials:write", "credentials:delete",
        "reports:read", "reports:write", "reports:delete",
        "users:manage", "settings:manage", "teams:manage"
    ],
    "analyst": [
        "scans:read", "scans:write",
        "campaigns:read", "campaigns:write",
        "findings:read", "findings:write",
        "credentials:read", "credentials:write",
        "reports:read", "reports:write"
    ],
    "viewer": [
        "scans:read",
        "campaigns:read",
        "findings:read",
        "credentials:read",
        "reports:read"
    ]
}

def has_permission(user: User, permission: str) -> bool:
    role = getattr(user, 'role', 'viewer')
    return permission in PERMISSIONS.get(role, [])

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            if not has_permission(current_user, permission):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

def require_role(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
            user_role = getattr(current_user, 'role', 'viewer')
            if user_role != role and user_role != 'admin':
                raise HTTPException(status_code=403, detail="Insufficient role")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
