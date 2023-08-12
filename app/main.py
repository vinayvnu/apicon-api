from fastapi import FastAPI
from .sqlalchemy import engine
from . import model
from .routers import post, user, auth, vote


model.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "HelloWorld!!!!!"}
