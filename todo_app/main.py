from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI()
FILE_PATH = "todos.json"

def save_to_file():
    with open(FILE_PATH, "w") as f:
        json.dump([todo.dict() for todo in todo_list], f)

def load_from_file():
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
            return [Todo(**item) for item in data]
    except FileNotFoundError:
        return []

#pydantic model

class Todo(BaseModel):
    title: str
    completed: bool = False

#in-memoy database
todo_list: List[Todo] = load_from_file()

# create a to-do

@app.post("/todos")
def create_todo(todo: Todo):
    new_id = 1 if not todo_list else todo_list[-1].id + 1
    new_todo = Todo(id = new_id, title = todo.title, completed = todo.completed)
    todo_list.append(new_todo)
    save_to_file()
    return {"message" : "To-do created", "todo": new_todo}

@app.get("/todos", response_model = List[Todo])
def get_todos():
    return todo_list

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for index, item in enumerate(todo_list):
        if item.id == todo_id:
            todo_list[index] = updated_todo
            save_to_file()
            return {"message": "To-do updated", "todo": updated_todo}
    return HTTPException(status_code = 404, detail = "To-do not found")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, item in enumerate(todo_list):
        if item.id == todo_id:
            deleted = todo_list.pop(index)
            save_to_file()
            return {"message": "To-do deleted", "todo": deleted}
    
    raise HTTPException(status_code = 404, detail = "To-do not found")

