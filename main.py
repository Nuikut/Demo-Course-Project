from fastapi import FastAPI
from database import Database

app = FastAPI()
database = Database()

database.create_user('aaaaa', '123')
database.select_all()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
