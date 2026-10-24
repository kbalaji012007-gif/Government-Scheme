from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # MongoDB Settings
    MONGODB_URI: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "ruralconnect_karnataka"

    # Authentication Settings
    SECRET_KEY: str = "ruralconnect_karnataka_super_secret_jwt_development_key_change_in_prod_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # CORS Settings
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.FRONTEND_ORIGINS.split(",") if origin.strip()]


settings = Settings()
