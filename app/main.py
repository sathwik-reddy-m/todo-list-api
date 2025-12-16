from fastapi import FastAPI, HTTPException
from typing import List
from app.schemas import Todo, TodoCreate

app= FastAPI(title="Todo List API")

# In-memory storage(temporary)
todos: List[Todo] = []
todo_id_counter = 1

@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    global todo_id_counter

    new_todo = Todo(
        id = todo_id_counter,
        title = todo.title,
        completed = todo.completed
    )

    todos.append(new_todo)
    todo_id_counter+=1

    return new_todo

@app.get("/todos",response_model=List[Todo])
def get_all_nodes():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}",response_model=Todo)
def update_todo(todo_id: int, update_todo: TodoCreate):
    for index, todo in enumerate(todos):
        if todo.id == todo_id:
            todos[index]= Todo(
                id= todo_id,
                title= update_todo.title,
                completed= update_todo.completed
            )
            return todos[index]
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index,todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(index)
            return {"message":"Todo deleted successfully"}
    raise HTTPException(status_code=404,detail="Todo not found")
