from fastapi import FastAPI

from dataprocessing import getAllUsers, getUser

app = FastAPI()

@app.get("/users")
def read_root():
    data = getAllUsers()
    return data

@app.get("/users/")
def get_user(user_id: int):
    return getUser(user_id)

