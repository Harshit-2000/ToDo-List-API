from typing import Optional
from fastapi import HTTPException, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
import hashlib
from models import User
from database import SessionLocal
import jwt
from starlette.status import HTTP_401_UNAUTHORIZED
import datetime

def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, session):
    user = session.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.password_hash == hash_password(password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return user


def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
    return encoded_jwt


def check_token(token: str):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def get_current_user(token: str = Header(None)):
    if not token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Token not provided")
    user = check_token(token)
    return user
    