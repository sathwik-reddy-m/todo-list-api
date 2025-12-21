from sqlalchemy.orm import Session
from app.models import TodoModel
from app.schemas import TodoCreate

def create_todo(db: Session, todo: TodoCreate):
    new_todo = TodoModel(
        title=todo.title,
        completed=todo.completed
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


def get_all_todos(db: Session):
    return db.query(TodoModel).all()


def get_todo_by_id(db: Session, todo_id: int):
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()


def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = get_todo_by_id(db, todo_id)
    if not db_todo:
        return None

    db_todo.title = todo.title
    db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo_by_id(db, todo_id)
    if not db_todo:
        return None

    db.delete(db_todo)
    db.commit()
    return db_todo
