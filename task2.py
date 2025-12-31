from fastapi import FastAPI, HTTPException, Path
from typing import Optional
import uvicorn
from pydantic import BaseModel, Field

app = FastAPI()

todos = []

class Todo(BaseModel):
    id: int = None
    title: str = Field(..., description="Title of the todo", max_length=100)
    description: str = None
    completed: bool = False
    created_at: str = None

class updated_todo(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    created_at: Optional[str] = None
@app.get("/")
def home():
    return {"message": "Welcome to the Todo API!"}

@app.post("/todos")
def create_todo(*,id: int = Path(...,description="ID of the todo",gt =0), todo: Todo ):
    if id not in [t.id for t in todos]:
        todos.append(todo)
        raise HTTPException(status_code=201, detail="Todo created successfully")
    else:
        raise HTTPException(status_code=400, detail="id already exists heheheh")
    
@app.get("/todos")
def get_todos():
    return {"todos": todos}

@app.get("/todos/{id}")
def get_todo_by_id(id:int):
    if id in [t.id for t in todos]:
        todo = next(t for t in todos if t.id == id)
        raise HTTPException(status_code=200, detail=todo)    
    else:
        raise HTTPException(status_code=404, detail="id not found")
        
    
@app.put("/todos/{id}")
def update_todo(id : int, updated_todo: updated_todo):
     if id in [t.id for t in todos]:
         for index, todo in enumerate(todos):
               if todo.id == id:
                   if updated_todo.id is not None:
                       todo.id = updated_todo.id
                   if updated_todo.title is not None:
                       todo.title = updated_todo.title
                   if updated_todo.description is not None:
                       todo.description = updated_todo.description
                   if updated_todo.completed is not None:
                       todo.completed = updated_todo.completed
                   if updated_todo.created_at is not None:
                       todo.created_at = updated_todo.created_at                   
                   raise HTTPException(status_code=200, detail="Todo updated successfully")
     else:
         raise HTTPException(status_code=404, detail="id not found")

@app.delete("/todos/{id}")
def delete_todo(id: int):
    if id in [t.id for t in todos]:
        for index, todo in enumerate(todos):
            if todo.id ==id:
                todos.pop(index)
                raise HTTPException(status_code=200, detail="todo deleted successfully")
    else:
        raise HTTPException(status_code=404, detail="id not found")        
    
if __name__ == "__main__":
    uvicorn.run("task2.app", host="127.0.0.1", port = 8000, reload=True)    