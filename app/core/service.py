from datetime import date

from app.core.errors import InvalidTodoError, TodoNotFoundError
from app.storage.base import TodoRepository

MAX_TEXT_LENGTH = 200


class TodoService:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    def list_todos(self) -> list:
        return self._repo.all()

    def create(self, text: str, due_date: date | None = None):
        text = text.strip()
        if not text:
            raise InvalidTodoError("text must not be empty")
        if len(text) > MAX_TEXT_LENGTH:
            raise InvalidTodoError(f"text must be {MAX_TEXT_LENGTH} characters or fewer")
        return self._repo.add(text, due_date=due_date)

    def toggle(self, todo_id: int):
        todo = self._repo.get(todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        todo.done = not todo.done
        return self._repo.save(todo)

    def delete(self, todo_id: int) -> None:
        if not self._repo.delete(todo_id):
            raise TodoNotFoundError(todo_id)
