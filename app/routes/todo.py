from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import Todo, TodoCreate
from app.crud import todo as crud_todo
from app.deps import get_db

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=Todo)
def create(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud_todo.create_todo(db, todo)


@router.get("/", response_model=List[Todo])
def read_all(db: Session = Depends(get_db)):
    return crud_todo.get_all_todos(db)


@router.get("/{todo_id}", response_model=Todo)
def read(todo_id: int, db: Session = Depends(get_db)):
    todo = crud_todo.get_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    updated = crud_todo.update_todo(db, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    deleted = crud_todo.delete_todo(db, todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}
