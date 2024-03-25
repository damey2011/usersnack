import os
from enum import Enum
from typing import Any, Dict, List

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV = os.getenv("ENV", "local")


class Environment(str, Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "prod"
    TEST = "test"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=[f".env.{_ENV}", f".env"])

    ENV: Environment = _ENV

    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    STATIC_BASE_URL: str = "localhost:8002"

    TORTOISE_ORM_MODELS: List[str] = [
        "db_models.snacks",
        "db_models.orders",
        "aerich.models",
    ]

    def get_postgres_dsn(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgres",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USERNAME,
            password=self.POSTGRES_PASSWORD,
            path=f"{self.POSTGRES_DB}",
        )

    def get_tortoise_orm_settings(self) -> Dict[str, Any]:
        return {
            "connections": {"default": str(self.get_postgres_dsn())},
            "apps": {
                "models": {
                    "models": self.TORTOISE_ORM_MODELS,
                    "default_connection": "default",
                },
            },
        }

    @staticmethod
    def get_current_env() -> Environment:
        return Environment(_ENV)


settings = Settings()

TORTOISE_ORM = settings.get_tortoise_orm_settings()
