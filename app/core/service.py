from app.core.errors import InvalidTodoError, TodoNotFoundError
from app.core.models import Todo
from app.storage.base import TodoRepository

MAX_TEXT_LENGTH = 200


class TodoService:
    def __init__(self, repo: TodoRepository):
        self._repo = repo

    def list_todos(self) -> list[Todo]:
        return self._repo.all()

    def create(self, text: str) -> Todo:
        text = text.strip()
        if not text:
            raise InvalidTodoError("text must not be empty")
        if len(text) > MAX_TEXT_LENGTH:
            raise InvalidTodoError(f"text must be {MAX_TEXT_LENGTH} characters or fewer")
        return self._repo.add(text)

    def toggle(self, todo_id: int) -> Todo:
        todo = self._repo.get(todo_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        todo.done = not todo.done
        return self._repo.save(todo)

    def delete(self, todo_id: int) -> None:
        if not self._repo.delete(todo_id):
            raise TodoNotFoundError(todo_id)
