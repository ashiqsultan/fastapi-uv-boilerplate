from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Supports both development and production modes.
    """

    app_name: str = Field(default="backend", description="Application name")
    environment: str = Field(
        default="development", description="Environment: 'development' or 'production'"
    )
    DB_NAME: str = Field()

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Get application settings instance"""
    return Settings()
