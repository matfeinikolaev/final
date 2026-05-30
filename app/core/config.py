from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """App Settings for Final"""

    # --- Database ---
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "final_db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # --- JWT & Auth ---
    SECRET_KEY: str = "temporary_secret_key_for_development_only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180
    REFRESH_TOKEN_EXPIRE_DAYS: int = 180

    # --- Project Info ---
    DEBUG: bool = True
    PROJECT_NAME: str = "Final API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # --- CORS ---
    CORS_ORIGINS: str = (
        "http://localhost:5173,http://localhost:5175,http://localhost:3000"
    )

    # --- Email (Yandex) ---
    EMAIL_HOST: str = "smtp.yandex.ru"
    EMAIL_PORT: int = 465
    EMAIL_USE_SSL: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = ""

    ADMIN_EMAIL: str = ""

    # Настройки Pydantic v2: объединяем env_file и правила обработки
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )

    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        """Превращаем строку CORS_ORIGINS в список для FastAPI"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
