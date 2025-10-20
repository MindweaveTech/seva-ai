"""Application configuration settings."""

from typing import List

from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://seva_user:seva_password@localhost:5432/seva_ai"
    )

    # Weaviate
    WEAVIATE_URL: str = Field(default="http://localhost:8080")
    WEAVIATE_API_KEY: str = Field(default="")

    # Redis
    REDIS_URL: str = Field(default="redis://:redis_password@localhost:6379/0")

    # Security
    SECRET_KEY: str = Field(default="change-this-secret-key-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # API Keys
    ANTHROPIC_API_KEY: str = Field(default="")
    OPENAI_API_KEY: str = Field(default="")

    # Google Cloud
    GOOGLE_APPLICATION_CREDENTIALS: str = Field(default="")
    GOOGLE_CLOUD_PROJECT: str = Field(default="")

    # Application
    ENVIRONMENT: str = Field(default="development")
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")

    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:19006",
            "http://localhost:19000",
        ]
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(default=100)

    # File Upload
    MAX_UPLOAD_SIZE: int = Field(default=10485760)  # 10MB

    # Health Monitoring
    HEALTH_CHECK_INTERVAL_MINUTES: int = Field(default=5)
    ANOMALY_DETECTION_THRESHOLD: float = Field(default=2.0)

    # Email/Notifications (optional)
    SMTP_HOST: str = Field(default="")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    FROM_EMAIL: str = Field(default="noreply@seva-ai.com")

    # Sentry
    SENTRY_DSN: str = Field(default="")

    # Feature Flags
    ENABLE_VOICE: bool = Field(default=True)
    ENABLE_HEALTH_MONITORING: bool = Field(default=True)
    ENABLE_CAREGIVER_ALERTS: bool = Field(default=True)

    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_origins(cls, v):
        """Parse ALLOWED_ORIGINS if provided as comma-separated string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("CORS_ALLOW_METHODS", pre=True)
    def parse_methods(cls, v):
        """Parse CORS_ALLOW_METHODS if provided as comma-separated string."""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [method.strip() for method in v.split(",")]
        return v

    @validator("CORS_ALLOW_HEADERS", pre=True)
    def parse_headers(cls, v):
        """Parse CORS_ALLOW_HEADERS if provided as comma-separated string."""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            return [header.strip() for header in v.split(",")]
        return v


# Create settings instance
settings = Settings()
