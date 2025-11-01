from functools import lru_cache
from pathlib import Path

from environs import Env
from pydantic_settings import BaseSettings, SettingsConfigDict

env = Env()
env.read_env(".env")

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    PROJECT_NAME: str = env.str("PROJECT_NAME")
    SECRET_KEY: str = env.str("SECRET_KEY")

    DB_BACKEND: str = env.str("DB_BACKEND")
    DB_ECHO: bool = env.bool("DB_ECHO")
    DB_NAME: str = env.str("DB_NAME")
    DB_USER: str = env.str("DB_USER", "")
    DB_PASSWORD: str = env.str("DB_PASSWORD", "")
    DB_HOST: str = env.str("DB_HOST", "")
    DB_PORT: int = env.int("DB_PORT", 0)

    SERVER_ADDRESS: str = env.str("SERVER_ADDRESS")
    SERVER_PORT: int = env.int("SERVER_PORT")

    STORAGE_DIR: str = "uploads"
    STORAGE_URL: str = "/uploads"
    STATIC_DIR: str = "static"
    TEMPLATES_DIR: str = "app/templates"
    STATIC_URL: str = "/static"

    ADMIN_PREFIX: str = env.str("ADMIN_PREFIX")
    ADMIN_SITE_NAME: str = env.str("ADMIN_SITE_NAME")
    ADMIN_PRIMARY_COLOR: str = env.str("ADMIN_PRIMARY_COLOR")
    ADMIN_SITE_LOGO: str = env.str("ADMIN_SITE_LOGO")
    ADMIN_SITE_FAVICON: str = env.str("ADMIN_SITE_FAVICON")
    DEBUG: bool = True

    API_KEY: str = env.str("API_KEY", "sk-your-default-api-key-2024")

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_BACKEND == "sqlite":
            db_path = BASE_DIR / self.DB_NAME
            return f"sqlite+aiosqlite:///{db_path}"
        elif self.DB_BACKEND == "postgresql":
            return (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        elif self.DB_BACKEND == "mysql":
            return (
                f"mysql+aiomysql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

        raise ValueError(f"Unsupported DB_BACKEND: {self.DB_BACKEND}")



    @property
    def SYNC_DATABASE_URL(self) -> str:
        if self.DB_BACKEND == "sqlite":
            db_path = BASE_DIR / self.DB_NAME
            return f"sqlite:///{db_path}"
        elif self.DB_BACKEND == "postgresql":
            return (
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        elif self.DB_BACKEND == "mysql":
            return (
                f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )

        raise ValueError(f"Unsupported DB_BACKEND: {self.DB_BACKEND}")


    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
