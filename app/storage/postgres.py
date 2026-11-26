import psycopg
from psycopg.rows import dict_row

from app.core.models import Todo
from app.storage.base import TodoRepository

_INIT_SQL = """
CREATE TABLE IF NOT EXISTS todos (
    id   SERIAL PRIMARY KEY,
    text TEXT    NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);
"""


class PostgresRepository(TodoRepository):
    def __init__(self, conninfo: str) -> None:
        self._conninfo = conninfo
        self._ensure_table()

    def _connect(self) -> psycopg.Connection:
        return psycopg.connect(self._conninfo, row_factory=dict_row)

    def _ensure_table(self) -> None:
        with self._connect() as conn:
            conn.execute(_INIT_SQL)

    def all(self) -> list[Todo]:
        with self._connect() as conn:
            rows = conn.execute("SELECT id, text, done FROM todos ORDER BY id").fetchall()
        return [Todo(**r) for r in rows]

    def get(self, todo_id: int) -> Todo | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT id, text, done FROM todos WHERE id = %s", (todo_id,)
            ).fetchone()
        return Todo(**row) if row else None

    def add(self, text: str) -> Todo:
        with self._connect() as conn:
            row = conn.execute(
                "INSERT INTO todos (text) VALUES (%s) RETURNING id, text, done",
                (text,),
            ).fetchone()
        return Todo(**row)

    def save(self, todo: Todo) -> Todo:
        with self._connect() as conn:
            conn.execute(
                "UPDATE todos SET text = %s, done = %s WHERE id = %s",
                (todo.text, todo.done, todo.id),
            )
        return todo

    def delete(self, todo_id: int) -> bool:
        with self._connect() as conn:
            cur = conn.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        return cur.rowcount > 0
