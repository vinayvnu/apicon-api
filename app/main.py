from fastapi import FastAPI
from .sqlalchemy import engine
from . import model
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

# this is the list who are allowed to access the api
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "HelloWorld!!!!!"}
