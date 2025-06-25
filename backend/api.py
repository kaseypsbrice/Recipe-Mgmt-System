from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db, User
from security import hash_password

app = FastAPI()

@app.post("/users/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    pwd_hash = hash_password(password)
    new_user = User(username=username, password_hash=pwd_hash)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return (new_user)
# Creates a new user

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return (db.query(User).all())
# Returns all users in database