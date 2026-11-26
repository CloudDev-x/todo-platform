import uvicorn

from app.config import load_settings

if __name__ == "__main__":
    settings = load_settings()
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        log_level=settings.log_level,
    )
