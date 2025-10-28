import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from ..models import User
from ..schemas import UserCreate, Token, UserOut
from ..utils.security import get_password_hash, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

ALGORITHM = "HS256"


def _get_jwt_secret() -> str:
    secret = os.getenv("JWT_SECRET", "devsecret")
    return secret


def _get_access_token_expires_minutes() -> int:
    try:
        return int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    except Exception:
        return 60


def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=_get_access_token_expires_minutes()))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _get_jwt_secret(), algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/register", response_model=UserOut, summary="Register a new user")
async def register(payload: UserCreate, session: AsyncSession = Depends(get_async_session)):
    # Check if user exists
    result = await session.execute(select(User).where(User.email == payload.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(email=str(payload.email), hashed_password=get_password_hash(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.post("/login", response_model=Token, summary="Login and obtain JWT")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    # OAuth2PasswordRequestForm has username, password
    email: EmailStr = EmailStr(form_data.username)
    result = await session.execute(select(User).where(User.email == str(email)))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = _create_access_token({"sub": str(user.id), "email": user.email})
    return Token(access_token=token, token_type="bearer")


# PUBLIC_INTERFACE
async def get_current_user(token: str = Depends(...), session: AsyncSession = Depends(get_async_session)) -> User:
    """
    Resolve current user from Authorization bearer token.
    NOTE: This function is intended to be used via get_current_user_dep in deps.py
    """
    try:
        payload = jwt.decode(token, _get_jwt_secret(), algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
