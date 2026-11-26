from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from app.api.schemas import TodoCreate, TodoOut
from app.core.service import TodoService

router = APIRouter()


def get_service(request: Request) -> TodoService:
    return request.app.state.todo_service


Service = Annotated[TodoService, Depends(get_service)]


@router.get("/todos", response_model=list[TodoOut])
async def list_todos(service: Service):
    return service.list_todos()


@router.post("/todos", response_model=TodoOut, status_code=201)
async def create_todo(body: TodoCreate, service: Service):
    return service.create(body.text, due_date=body.due_date)


@router.patch("/todos/{todo_id}", response_model=TodoOut)
async def toggle_todo(todo_id: int, service: Service):
    return service.toggle(todo_id)


@router.delete("/todos/{todo_id}", status_code=204)
async def delete_todo(todo_id: int, service: Service):
    service.delete(todo_id)
    return Response(status_code=204)
