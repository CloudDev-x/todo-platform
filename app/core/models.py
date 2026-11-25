from dataclasses import dataclass


@dataclass
class Todo:
    id: int
    text: str
    done: bool = False
