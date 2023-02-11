from fastapi import FastAPI, Depends, HTTPException
from models import User, Todo
from fastapi.security import OAuth2PasswordRequestForm
from utils import *
from schemas import * 
from typing import List
import models
from database import db_engine


models.Base.metadata.create_all(bind=db_engine)
app = FastAPI()


@app.get("/")
def home():
    return {"message" : "Hello World"}

    
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup")
def signup(user: UserInDB, db=Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password_hash)
    new_user = User(username=user.username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created"}


@app.post("/todos",  response_model=TodoCreate)
def create_todo(todo: TodoCreate, current_user=Depends(get_current_user),db=Depends(get_db)):
    todo_item = Todo(task=todo.task, completed=todo.completed)
    db.add(todo_item)
    db.commit()
    
    return todo_item


@app.get("/todos", response_model=TodoList)
def read_todos(skip: int = 0, limit: int = 100, current_user=Depends(get_current_user), db=Depends(get_db)):
    todos = db.query(Todo).offset(skip).limit(limit).all()
    return todos


@app.get("/todos/{todo_id}",  response_model=TodoList)
def read_todo(todo_id: int, current_user=Depends(get_current_user),db=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todos/{todo_id}", response_model=TodoList)
def update_todo(todo_id: int, todo: TodoUpdate, current_user=Depends(get_current_user), db=Depends(get_db)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_item.task = todo.task
    todo_item.completed = todo.completed
    db.commit()
    return todo_item


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, current_user=Depends(get_current_user),db=Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}
