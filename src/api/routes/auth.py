"""
Authentication API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from src.auth.database import UserDB, UsageDB
from src.auth.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/auth", tags=["authentication"])
security = HTTPBearer()


# Request/Response Models
class UserRegister(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "secret123"
            }
        }


class UserLogin(BaseModel):
    """User login request"""
    username: str
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "secret123"
            }
        }


class Token(BaseModel):
    """Token response"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    tier: str


class UserProfile(BaseModel):
    """User profile response"""
    id: int
    username: str
    email: str
    tier: str
    created_at: str
    total_queries: int


# Dependency to get current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = UserDB.get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user

    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (minimum 6 characters)

    Returns JWT access token for immediate login.
    """
    # Check if username exists
    if UserDB.get_user_by_username(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    if UserDB.get_user_by_email(user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password and create user
    hashed_pwd = hash_password(user_data.password)
    user_id = UserDB.create_user(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_pwd,
        tier="free"
    )

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user_id)})

    logger.info(f"New user registered: {user_data.username}")

    return Token(
        access_token=access_token,
        user_id=user_id,
        username=user_data.username,
        tier="free"
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login with username and password

    - **username**: Your username
    - **password**: Your password

    Returns JWT access token for API authentication.
    """
    # Get user
    user = UserDB.get_user_by_username(credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Verify password
    if not verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # Check if active
    if not user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user["id"])})

    logger.info(f"User logged in: {credentials.username}")

    return Token(
        access_token=access_token,
        user_id=user["id"],
        username=user["username"],
        tier=user["tier"]
    )


@router.get("/me", response_model=UserProfile)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """
    Get current user profile

    Requires authentication token in header:
    `Authorization: Bearer <token>`
    """
    # Get usage stats
    usage_stats = UsageDB.get_total_usage(current_user["id"])
    total_queries = usage_stats.get("chat", 0)

    return UserProfile(
        id=current_user["id"],
        username=current_user["username"],
        email=current_user["email"],
        tier=current_user["tier"],
        created_at=current_user["created_at"],
        total_queries=total_queries
    )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """
    Logout current user

    Note: JWT tokens are stateless, so logout is handled client-side
    by discarding the token. This endpoint is provided for completeness.
    """
    logger.info(f"User logged out: {current_user['username']}")
    return {"message": "Logged out successfully"}
