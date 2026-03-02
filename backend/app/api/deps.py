from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core import security
from app.core.config import settings
from app.crud import crud_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

import logging

logger = logging.getLogger(__name__)

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    logger.info(f"[get_current_user] Validating token...")
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        logger.info(f"[get_current_user] Token decoded successfully, user_id: {token_data.sub}")
    except (JWTError, ValidationError) as e:
        logger.error(f"[get_current_user] Token validation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud_user.user.get(db, id=int(token_data.sub))
    if not user:
        logger.error(f"[get_current_user] User not found for id: {token_data.sub}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"[get_current_user] User authenticated: {user.id}, email: {user.email}")
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
