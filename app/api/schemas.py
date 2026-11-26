from pydantic import BaseModel


class TodoCreate(BaseModel):
    text: str


class TodoOut(BaseModel):
    id: int
    text: str
    done: bool
