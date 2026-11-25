from abc import ABC, abstractmethod

from app.core.models import Todo


class TodoRepository(ABC):
    @abstractmethod
    def all(self) -> list[Todo]: ...

    @abstractmethod
    def get(self, todo_id: int) -> Todo | None: ...

    @abstractmethod
    def add(self, text: str) -> Todo: ...

    @abstractmethod
    def save(self, todo: Todo) -> Todo: ...

    @abstractmethod
    def delete(self, todo_id: int) -> bool: ...
