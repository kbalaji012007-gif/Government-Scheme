from typing import Dict, Any
from fastapi import APIRouter, Depends
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse, TokenResponse
from app.services.auth_service import AuthService
from app.core.security import get_current_user_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()


@router.post("/register", response_model=TokenResponse)
async def register(payload: UserRegisterRequest):
    return auth_service.register_user(payload)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest):
    return auth_service.login_user(payload)


@router.get("/me", response_model=UserResponse)
async def get_me(current_token: Dict[str, Any] = Depends(get_current_user_token)):
    user_id = current_token.get("sub", "")
    return auth_service.get_current_user_profile(user_id)
