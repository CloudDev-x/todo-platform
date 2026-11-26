from dataclasses import dataclass, field
from datetime import date


@dataclass
class Todo:
    id: int
    text: str
    done: bool = False
    due_date: date | None = None
