from fastapi import APIRouter, Depends, HTTPException
from db import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from utils import get_hashed_password, verify_password, create_access_token

from models import UserRegister
from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str

user_router = APIRouter()

#create an endpoint for user registration, get email and password from request body then add them to the database
@user_router.post("/register")
def register_user(user:User , db: Session = Depends(get_db)):

    user.password = get_hashed_password(user.password)

    try:
        db.execute(text("""
            INSERT INTO users (email, password)
            VALUES (:email, :password)
        """), {"email": user.email, "password": user.password})
        db.commit()
    except:
        raise HTTPException(status_code=400, detail="Email already exists")

    access_token = create_access_token(subject={"sub": user.email}, expires_delta=7)

    return {"token": access_token, "token_type": "bearer"}

@user_router.post("/login")
def login_user(_user:User , db: Session = Depends(get_db)):
    
    user = db.query(UserRegister).filter(UserRegister.email == _user.email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    hashed_pasword = user.password

    if not verify_password(_user.password, hashed_pasword):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token = create_access_token(subject={"sub": user.email}, expires_delta=7)

    return {"token": access_token, "token_type": "bearer"}