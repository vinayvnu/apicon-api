from fastapi import FastAPI, Response, status, HTTPException, Depends
from .conn import db_conn_select, db_conn_insert, db_conn_delete, db_conn_update
from .sqlalchemy import engine, get_db
from sqlalchemy.orm import Session
from . import model, schemas, utils
from .routers import post, user, auth

import time

model.Base.metadata.create_all(bind=engine)
app = FastAPI()


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favourite fruit", "content": "I like Mangoes", "id": 2},
]


def find_post(id_to_check):
    for p in my_posts:
        if p["id"] == id_to_check:
            return p


def find_index_post(id_to_find):
    for i, p in enumerate(my_posts):
        if p["id"] == id_to_find:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "HelloWorld!!!!!"}
