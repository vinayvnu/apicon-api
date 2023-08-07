from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException

# from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from app.conn import db_conn_select, db_conn_insert, db_conn_delete, db_conn_update

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
    data = db_conn_select("""select * from apicon.posts order by id""")
    print(data)
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print("here4")
    # # print(post.model_dump())
    # post_dict = post.model_dump()
    # post_dict["id"] = randrange(0, 1000000)
    # my_posts.append(post.model_dump())
    publish_value_pass = 1
    if post.published:
        publish_value_pass = 1
    else:
        publish_value_pass = 0
    query = f"INSERT INTO `apicon`.`posts` (`title`, `content`, `PUBLISHED`) VALUES ('{post.title}', '{post.content}', {publish_value_pass})"
    print(query)

    returned_data = db_conn_insert(query)
    print(f"returned_data: {returned_data}")
    return {"data"}


@app.get("/posts/{id}")
def get_post(id_passed: int):
    print("here3")
    post = db_conn_select(f"select * from apicon.posts where id={id_passed}")
    print(post)
    # post = find_post(id_passed)
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
    # index = find_index_post(id_passed)
    index = db_conn_select(f"select * from apicon.posts where id={id_passed}")
    print(index)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} does not exist",
        )

    print("here2")

    db_conn_delete(f"delete from apicon.posts where id={id_passed}")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id_to_update: int, post: Post):
    print("here2")
    print(post)
    # index = find_index_post(id_to_update)
    index = db_conn_select(f"select * from apicon.posts where id={id_to_update}")
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_to_update} does not exist",
        )

    publish_value = 1
    if post.published:
        publish_value = 1
    else:
        publish_value = 0

    db_conn_update(
        f"update apicon.posts set title= '{post.title}', content= '{post.content}', published={publish_value} where id={id_to_update}"
    )
    # post_dict = post.model_dump()
    # db_conn_update
    # post_dict["id"] = id_to_update
    # my_posts[index] = post_dict
    return {"message": f"updated post {id_to_update}"}
