from datetime import date

from app.core.models import Todo
from app.storage.base import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    def __init__(self) -> None:
        self._items: dict[int, Todo] = {}
        self._next_id = 1

    def all(self) -> list[Todo]:
        return list(self._items.values())

    def get(self, todo_id: int) -> Todo | None:
        return self._items.get(todo_id)

    def add(self, text: str, *, due_date: date | None = None) -> Todo:
        todo = Todo(id=self._next_id, text=text, due_date=due_date)
        self._items[self._next_id] = todo
        self._next_id += 1
        return todo

    def save(self, todo: Todo) -> Todo:
        self._items[todo.id] = todo
        return todo

    def delete(self, todo_id: int) -> bool:
        return self._items.pop(todo_id, None) is not None
