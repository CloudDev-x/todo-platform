from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.api.schemas import TodoCreate, TodoOut
from app.core.service import TodoService

router = APIRouter()


def get_service(request: Request) -> TodoService:
    return request.app.state.todo_service


Service = Annotated[TodoService, Depends(get_service)]


@router.get("/todos", response_model=list[TodoOut])
def list_todos(service: Service):
    return service.list_todos()


@router.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate, service: Service):
    return service.create(payload.text)


@router.patch("/todos/{todo_id}", response_model=TodoOut)
def toggle_todo(todo_id: int, service: Service):
    return service.toggle(todo_id)


@router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, service: Service):
    service.delete(todo_id)
