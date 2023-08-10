from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, model, utils
from ..sqlalchemy import engine, get_db

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/")
def user_login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    print("user_login called")
    check_user = (
        db.query(model.Users)
        .filter(model.Users.email == user_credentials.email)
        .first()
    )

    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )

    if not utils.verify(user_credentials.password, check_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials",
        )

    return {"token": "example token"}
