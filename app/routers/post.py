from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from sqlalchemy.orm import Session
from app.sqlalchemy import get_db
from app import model, schemas, oauth2
from sqlalchemy import func

# by adding prefix the common /posts from decorators can be removed
# tags are used to group tags into categories in  swagger ui
router = APIRouter(prefix="/posts", tags=["Posts"])


# @router.get("/posts", response_model=List[schemas.PostResponse])
# limit is the query parameter it can be called like this
# http://127.0.0.1:8000/posts?limit=3&skip=1&search=onetext%20twotext
@router.get("/")
# @router.get("/", response_model=List[schemas.PostResponse])
def get_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    print("here5")
    data = (
        db.query(model.Post)
        .filter(model.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    results = (
        db.query(model.Post, func.count(model.Vote.post_id).label("votes"))
        .join(model.Vote, model.Vote.post_id == model.Post.id, isouter=True)
        .group_by(model.Post.id)
        .filter(model.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    print(results)
    print(limit)
    return data


# TODO, the authentication of user before creating a post is not working.
# TODO check why user_id_get: int = Depends(oauth2.get_current_user)
@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse
)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    # current_user: int = Depends(oauth2.get_current_user())
):
    print("here4")
    current_user: int = Depends(oauth2.get_current_user)
    print(type(current_user))
    print(current_user.id)
    new_posts = model.Post(owner_id=current_user.id, **post.model_dump())
    # new_posts = model.Post(
    #     title=post.title, content=post.content, published=post.published
    # )
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
    current_user: int = Depends(oauth2.get_current_user())
    post = db.query(model.Post).filter(model.Post.id == id_passed).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_passed} does not exist",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorised to perform action",
        )

    db.delete(post)
    db.commit()

    print("here2")

    # db_conn_delete(f"delete from apicon.posts where id={id_passed}")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id_to_update: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)
):
    print("here2")
    current_user: int = Depends(oauth2.get_current_user())
    post_query = db.query(model.Post).filter(model.Post.id == id_to_update).first()

    if post_query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_to_update} does not exist",
        )
    if post_query.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"not authorised to perform action",
        )
    # TODO ADD THE CODE TO UPDATE THE DATA
    post_query.update(updated_post.model_dump())
    db.commit()
    return {"message": f"updated post {id_to_update}"}
