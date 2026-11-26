from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.config import load_settings
from app.core.errors import InvalidTodoError, TodoNotFoundError
from app.core.service import TodoService
from app.storage.memory import InMemoryTodoRepository

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


def _build_repo(settings):
    if settings.storage_backend == "postgres":
        from app.storage.postgres import PostgresRepository
        return PostgresRepository(settings.database_url)
    return InMemoryTodoRepository()


def create_app(service=None):
    settings = load_settings()

    if service is None:
        repo = _build_repo(settings)
        service = TodoService(repo)

    app = FastAPI(title="Todo Platform")
    app.state.todo_service = service

    @app.exception_handler(InvalidTodoError)
    async def invalid_todo(request: Request, exc: InvalidTodoError):
        return JSONResponse(status_code=400, content={"detail": str(exc)})

    @app.exception_handler(TodoNotFoundError)
    async def todo_not_found(request: Request, exc: TodoNotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.get("/healthz")
    async def healthz():
        return {"status": "ok"}

    app.include_router(router, prefix="/api")
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="static")

    return app


app = create_app()
