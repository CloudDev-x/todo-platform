import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    port: int = 8080
    log_level: str = "info"
    storage_backend: str = "memory"
    database_url: str = ""


def load_settings() -> Settings:
    return Settings(
        port=int(os.environ.get("PORT", "8080")),
        log_level=os.environ.get("LOG_LEVEL", "info").lower(),
        storage_backend=os.environ.get("STORAGE_BACKEND", "memory").lower(),
        database_url=os.environ.get("DATABASE_URL", ""),
    )
