class InvalidTodoError(Exception):
    """Raised when a todo's input breaks a business rule."""


class TodoNotFoundError(Exception):
    def __init__(self, todo_id: int):
        super().__init__(f"Todo {todo_id} not found")
        self.todo_id = todo_id
