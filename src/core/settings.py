from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    postgres_user: str = Field(env="POSTGRES_USER")
    postgres_password: str = Field(env="POSTGRES_PASSWORD")
    postgres_db: str = Field(env="POSTGRES_DB")
    postgres_port: str = Field(env="POSTGRES_PORT")
    postgres_service: str = Field(env="POSTGRES_SERVICE")
    uvicorn_workers: str = Field(env="UVICORN_WORKERS")

    root_path: str = Field(default="/")
    active_schema: str = Field(default="test")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # Ignore extra fields from environment
    )
