from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.errors import InvalidTodoError, TodoNotFoundError
from app.core.service import TodoService
from app.storage.memory import InMemoryTodoRepository

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


def create_app(service: TodoService | None = None) -> FastAPI:
    app = FastAPI(title="Todo Platform")
    app.state.todo_service = service or TodoService(InMemoryTodoRepository())

    @app.exception_handler(InvalidTodoError)
    async def invalid_todo(request: Request, exc: InvalidTodoError):
        return JSONResponse(status_code=400, content={"error": str(exc)})

    @app.exception_handler(TodoNotFoundError)
    async def todo_not_found(request: Request, exc: TodoNotFoundError):
        return JSONResponse(status_code=404, content={"error": str(exc)})

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}

    app.include_router(router, prefix="/api")
    app.mount("/", StaticFiles(directory=WEB_DIR, html=True), name="web")
    return app


app = create_app()
