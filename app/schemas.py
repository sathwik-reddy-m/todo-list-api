from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    completed: str

class Todo(TodoCreate):
    id: int

