import uuid
from datetime import datetime, timezone
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import (
    UserRegisterRequest,
    UserLoginRequest,
    GoogleAuthRequest,
    UserResponse,
    TokenResponse,
)
from app.core.security import hash_password, verify_password, create_access_token

user_repo = UserRepository()


class AuthService:
    def register_user(self, data: UserRegisterRequest) -> TokenResponse:
        existing_user = user_repo.find_by_email(data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email address already exists",
            )

        user_id = f"user_{uuid.uuid4().hex[:12]}"
        hashed = hash_password(data.password)

        new_user = {
            "id": user_id,
            "email": data.email.lower().strip(),
            "hashed_password": hashed,
            "full_name": data.full_name.strip(),
            "role": "citizen",
            "preferred_language": data.preferred_language or "kn",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        created = user_repo.create(new_user)
        user_response = UserResponse(
            id=created["id"],
            email=created["email"],
            full_name=created["full_name"],
            role=created["role"],
            preferred_language=created["preferred_language"],
        )

        token = create_access_token(
            subject=user_response.id,
            extra_data={"email": user_response.email, "role": user_response.role},
        )

        return TokenResponse(access_token=token, token_type="bearer", user=user_response)

    def login_user(self, data: UserLoginRequest) -> TokenResponse:
        user = user_repo.find_by_email(data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not verify_password(data.password, user.get("hashed_password", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            preferred_language=user.get("preferred_language", "kn"),
        )

        token = create_access_token(
            subject=user_response.id,
            extra_data={"email": user_response.email, "role": user_response.role},
        )

        return TokenResponse(access_token=token, token_type="bearer", user=user_response)

    def get_current_user_profile(self, user_id: str) -> UserResponse:
        user = user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User account not found",
            )
        return UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user["role"],
            preferred_language=user.get("preferred_language", "kn"),
        )

    def google_auth(self, data: "GoogleAuthRequest") -> TokenResponse:
        user = user_repo.find_by_email(data.email)
        if not user:
            # Register new citizen from Google profile
            user_id = f"google_{data.uid}" if data.uid else f"user_{uuid.uuid4().hex[:12]}"
            new_user = {
                "id": user_id,
                "email": data.email.lower().strip(),
                "full_name": (data.full_name or "Citizen").strip(),
                "role": "citizen",
                "preferred_language": data.preferred_language or "kn",
                "auth_provider": "google",
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            user = user_repo.create(new_user)

        user_response = UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            role=user.get("role", "citizen"),
            preferred_language=user.get("preferred_language", "kn"),
        )

        token = create_access_token(
            subject=user_response.id,
            extra_data={"email": user_response.email, "role": user_response.role},
        )

        return TokenResponse(access_token=token, token_type="bearer", user=user_response)
