"""Application settings using Pydantic Settings management."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_parse_none_str="",  # Handle empty strings
    )

    # Application
    app_name: str = "IntelliStack API"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # Security
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "EdDSA"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Database (PostgreSQL only)
    database_url: str = Field(..., alias="DATABASE_URL")
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_pool_timeout: int = 30

    # Redis (required for production)
    redis_url: str = Field(..., alias="REDIS_URL")

    # Qdrant Vector DB
    qdrant_host: str = Field(..., alias="QDRANT_HOST")
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None
    qdrant_collection_name: str = "intellistack_content"

    # OpenAI (optional for basic features, required for AI tutor/RAG)
    openai_api_key: str = Field(default="sk-development-placeholder", alias="OPENAI_API_KEY")
    openai_model: str = "gpt-4-turbo-preview"
    openai_embedding_model: str = "text-embedding-3-small"

    # Cohere (for reranking)
    cohere_api_key: str | None = Field(default=None, alias="COHERE_API_KEY")

    # Rate Limiting
    rate_limit_auth: int = 60  # requests per minute for authenticated users
    rate_limit_unauth: int = 10  # requests per minute for unauthenticated

    # CORS
    cors_origins: list[str] | str = Field(
        default=["http://localhost:3000", "http://localhost:3001"],
        alias="CORS_ORIGINS"
    )
    cors_allow_credentials: bool = True

    # OAuth Providers
    # NOTE: Redirect URIs must point to the BACKEND server (port 8000)
    google_client_id: str | None = Field(default=None, alias="GOOGLE_CLIENT_ID")
    google_client_secret: str | None = Field(default=None, alias="GOOGLE_CLIENT_SECRET")
    google_redirect_uri: str = Field(..., alias="GOOGLE_REDIRECT_URI")

    github_client_id: str | None = Field(default=None, alias="GITHUB_CLIENT_ID")
    github_client_secret: str | None = Field(default=None, alias="GITHUB_CLIENT_SECRET")
    github_redirect_uri: str = Field(..., alias="GITHUB_REDIRECT_URI")

    # Post-Auth Redirect
    post_login_redirect_path: str = Field(default="/learn", alias="POST_LOGIN_REDIRECT_PATH")
    post_logout_redirect_path: str = Field(default="/login", alias="POST_LOGOUT_REDIRECT_PATH")

    # Better-Auth OIDC Server (JWT validation)
    better_auth_url: str = Field(..., alias="BETTER_AUTH_URL")
    better_auth_jwks_url: str = Field(..., alias="BETTER_AUTH_JWKS_URL")
    better_auth_issuer: str | None = Field(default=None, alias="BETTER_AUTH_ISSUER")
    better_auth_audience: str | None = Field(default=None, alias="BETTER_AUTH_AUDIENCE")
    better_auth_session_cookie_name: str = "better-auth.session_token"

    # ChatKit AI Tutor
    chatkit_rate_limit_student: int = 20  # messages per day for students
    chatkit_rate_limit_instructor: int = 0  # unlimited for instructors (0 = no limit)
    chatkit_rate_limit_admin: int = 0  # unlimited for admins

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_format: Literal["json", "console"] = "json"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                # Handle JSON array format
                import json
                return json.loads(v)
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def async_database_url(self) -> str:
        """Return async database URL with asyncpg driver."""
        url = str(self.database_url)
        # Convert PostgreSQL URL to use asyncpg driver
        if "postgresql://" in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://")
        # Remove sslmode from URL as it's handled via connect_args in database.py
        if "?sslmode=" in url:
            url = url.split("?sslmode=")[0]
        elif "&sslmode=" in url:
            url = url.split("&sslmode=")[0]
        return url


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
