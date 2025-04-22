from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Dict

app = FastAPI()

#pwd hasher
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

#in memory user "DB"
users_db: Dict[str, str]  = {}

#pydantic models
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# signup
@app.post("/signup")
def signup(user: UserCreate):
    if user.username in users_db:
        return HTTPException(status_code = 400, detail = "Username already existss")
    
    hashed_password = pwd_context.hash(user.password)
    users_db[user.username] = hashed_password
    return {"message": "User registered successfully"}

#Login

@app.post("/login")
def login(user: UserLogin):
    stored_password = users_db.get(user.username)

    if not stored_password or not pwd_context.verify(user.password, stored_password):
        return HTTPException(status_code = 401, detail = "Invalid credentials")
    
    return {"message": "Login successful"}