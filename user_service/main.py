from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    username: str
    email: str

users: List[User] = []

@app.post("/users/", response_model=User)
async def create_user(user: User):
    for existing_user in users:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User already exists")
    users.append(user)
    return user

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)