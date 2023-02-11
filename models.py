from database import Base
from sqlalchemy import Column, Integer, String, Boolean


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), index=True)
    completed = Column(Boolean, default=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), index=True)
    password_hash = Column(String(500))