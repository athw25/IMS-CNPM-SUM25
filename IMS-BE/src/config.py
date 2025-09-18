from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv

def _env(key: str, default: str) -> str:
    return os.getenv(key, default)

@dataclass
class AppConfig:
    SECRET_KEY: str
    JWT_SECRET_KEY: str
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JSON_SORT_KEYS: bool = False
    CORS_ORIGINS: str = "*"
    INIT_DB: str = "0"
    PORT: int = 5000

    @staticmethod
    def load() -> "AppConfig":
        load_dotenv()
        return AppConfig(
            SECRET_KEY=_env("SECRET_KEY", "change-me"),
            JWT_SECRET_KEY=_env("JWT_SECRET_KEY", "change-me-too"),
            SQLALCHEMY_DATABASE_URI=_env("DATABASE_URL", "sqlite:///ims.db"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JSON_SORT_KEYS=False,
            CORS_ORIGINS=_env("CORS_ORIGINS", "*"),
            INIT_DB=_env("INIT_DB", "0"),
            PORT=int(_env("PORT", "5000")),
        )
