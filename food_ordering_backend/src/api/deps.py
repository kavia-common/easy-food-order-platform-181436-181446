from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_async_session
from .models import User
from .routers.auth import get_current_user as _resolve_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# PUBLIC_INTERFACE
async def get_db() -> AsyncSession:
    """Yield AsyncSession for DB operations."""
    async for s in get_async_session():
        return s


# PUBLIC_INTERFACE
async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> User:
    """Resolve the current user given a bearer token."""
    try:
        user = await _resolve_current_user(token=token, session=session)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
