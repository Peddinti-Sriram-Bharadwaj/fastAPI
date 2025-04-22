from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


#pydantic model

class Todo(BaseModel):
    title: str
    completed: bool = False

#in-memoy database
todo_list: List[Todo] = []

# create a to-do

@app.post("/todos")
def create_todo(todo: Todo):
    new_id = 1 if not todo_list else todo_list[-1].id + 1
    new_todo = Todo(id = new_id, title = todo.title, completed = todo.completed)
    todo_list.append(new_todo)
    return {"message" : "To-do created", "todo": new_todo}

@app.get("/todos", response_model = List[Todo])
def get_todos():
    return todo_list

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, item in enumerate(todo_list):
        if item.id == todo_id:
            todo_list[index] = updated_todo
            return {"message": "To-do updated", "todo": updated_todo}
    return HTTPException(status_code = 404, detail = "To-do not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, item in enumerate(todo_list):
        if item.id == todo_id:
            deleted = todo_list.pop(index)
            return {"message": "To-do deleted", "todo": deleted}
    
    raise HTTPException(status_code = 404, detail = "To-do not found")

