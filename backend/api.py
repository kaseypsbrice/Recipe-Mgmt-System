from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db, User
from security import hash_password
from response_model import UserOut, UserIn

app = FastAPI()

@app.post("/users/", response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    pwd_hash = hash_password(user.password)
    new_user = User(username=user.username, password_hash=pwd_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return (new_user)
# Creates a new user

@app.get("/users/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return (db.query(User).all())
# Returns all users in database

