from fastapi import FastAPI
from app.database import engine
from app.models import TodoModel
from app.routes import todo

TodoModel.metadata.create_all(bind=engine)

app = FastAPI(title="Todo List API")

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "service": "todo-list-api"
    }


app.include_router(todo.router)
