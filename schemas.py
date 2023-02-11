from pydantic import BaseModel

class TodoList(BaseModel):
    task: str
    completed: bool = False

    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    task: str
    completed: bool = False

    class Config:
        orm_mode = True

class TodoUpdate(BaseModel):
    task: str
    completed: bool = False

    class Config:
        orm_mode = True

class UserInDB(BaseModel):
    username: str
    password_hash: str
