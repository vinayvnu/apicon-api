from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException

# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



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


@app.get("/")
async def root():
    return {"message": "HelloWorld!!!!!"}


@app.get("/posts")
def get_posts():
    print("here5")
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    print("here4")
    # print(post.model_dump())
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post.model_dump())
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id_passed: int):
    print("here3")
    post = find_post(id_passed)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id_passed} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} was not found",
        )

    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_passed: int):
    print("here1")
    index = find_index_post(id_passed)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} does not exist",
        )

    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id_to_update: int, post: Post):
    print("here2")
    print(post)
    index = find_index_post(id_to_update)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_to_update} does not exist",
        )

    post_dict = post.model_dump()
    post_dict["id"] = id_to_update
    my_posts[index] = post_dict
    return {"message": f"updated post {id_to_update}"}
