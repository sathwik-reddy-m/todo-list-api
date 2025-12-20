from fastapi import FastAPI, HTTPException
from typing import List
from app.schemas import Todo, TodoCreate
from app.database import engine
from app.models import TodoModel
from app.database import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends

app= FastAPI(title="Todo List API")

TodoModel.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = TodoModel(
        title = todo.title,
        completed = todo.completed
    )

    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return new_todo

@app.get("/todos",response_model=List[Todo])
def get_all_nodes(db: Session = Depends(get_db)):
    return db.query(TodoModel).all()

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo= db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}",response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db)):
    todo= db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    todo.title = updated_todo.title
    todo.completed = updated_todo.completed
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message":"Todo deleted successfully"}
