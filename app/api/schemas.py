from datetime import date

from pydantic import BaseModel


class TodoCreate(BaseModel):
    text: str
    due_date: date | None = None


class TodoOut(BaseModel):
    id: int
    text: str
    done: bool
    due_date: date | None = None
