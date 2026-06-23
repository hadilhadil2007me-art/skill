from typing import List, Union
from pydantic import AnyHttpUrl, BeforeValidator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SkillUp API"
    
    # JWT Security settings
    # Provide a development default so the app can run out-of-the-box.
    # Replace in production via .env or environment variables.
    SECRET_KEY: str = "dev_secret_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    # Default to a local SQLite file for quick demos / local runs.
    # In production override with a proper Postgres URL in `.env`.
    DATABASE_URL: str = "sqlite:///./skillup.db"

    # First Superuser Settings
    FIRST_SUPERUSER_EMAIL: str = "admin@skillup.dz"
    FIRST_SUPERUSER_PASSWORD: str = "admin_secure_password"
    # Production flag - set to true in production to enable secure cookies, stricter defaults
    PRODUCTION: bool = False


settings = Settings()
