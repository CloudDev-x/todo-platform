import pytest

from app.core.errors import InvalidTodoError, TodoNotFoundError
from app.core.service import TodoService
from app.storage.memory import InMemoryTodoRepository


@pytest.fixture
def service():
    return TodoService(InMemoryTodoRepository())


def test_create_trims_text(service):
    todo = service.create("  buy milk  ")
    assert todo.text == "buy milk"
    assert todo.done is False
    assert todo.id == 1


def test_create_rejects_empty(service):
    with pytest.raises(InvalidTodoError):
        service.create("   ")


def test_create_rejects_too_long(service):
    with pytest.raises(InvalidTodoError):
        service.create("x" * 201)


def test_toggle_flips_done(service):
    todo = service.create("walk")
    assert service.toggle(todo.id).done is True
    assert service.toggle(todo.id).done is False


def test_toggle_missing_raises(service):
    with pytest.raises(TodoNotFoundError):
        service.toggle(999)


def test_delete_removes_item(service):
    todo = service.create("temp")
    service.delete(todo.id)
    assert service.list_todos() == []


def test_delete_missing_raises(service):
    with pytest.raises(TodoNotFoundError):
        service.delete(999)
