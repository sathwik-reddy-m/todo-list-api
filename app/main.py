from fastapi import FastAPI
from app.database import engine
from app.models import TodoModel
from app.routes import todo

TodoModel.metadata.create_all(bind=engine)

app = FastAPI(title="Todo List API")

app.include_router(todo.router)
