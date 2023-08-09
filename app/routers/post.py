from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from ..sqlalchemy import engine, get_db
from .. import model, schemas
from ..conn import db_conn_select, db_conn_insert, db_conn_delete

# by adding prefix the common /posts from decorators can be removed
# tags are used to group tags into categories in  swagger ui
router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/posts", response_model=List[schemas.PostResponse])
@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    print("here5")
    data = db.query(model.Post).all()
    # data = db_conn_select("""select * from apicon.posts order by id""")
    print(data)
    return data


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    print("here4")
    print(post.model_dump())
    new_posts = model.Post(**post.model_dump())
    # new_posts = model.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)

    # returned_data = db_conn_insert(query)
    print(f"returned_data: {new_posts}")
    return new_posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id_passed: int, db: Session = Depends(get_db)):
    print("here3")
    print(id_passed)
    post = db.query(model.Post).filter(model.Post.id == id_passed).first()
    print(post)

    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id_passed} was not found"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} was not found",
        )

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id_passed: int, db: Session = Depends(get_db)):
    print("here1")
    post = db.query(model.Post).filter(model.Post.id == id_passed).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} does not exist",
        )
    else:
        db.delete(post)
        db.commit()

    print("here2")

    db_conn_delete(f"delete from apicon.posts where id={id_passed}")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id_to_update: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    print("here2")
    post_query = db.query(model.Post).filter(model.Post.id == id_to_update).first()

    if post_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_to_update} does not exist",
        )
    # TODO ADD THE CODE TO UPDATE THE DATA
    post_query.update(updated_post.model_dump())
    db.commit()
    return {"message": f"updated post {id_to_update}"}
