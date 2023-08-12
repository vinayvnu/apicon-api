from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, model, utils, oauth2
from ..sqlalchemy import engine, get_db

router = APIRouter(prefix="/login", tags=["Authentication"])


@router.post("/", response_model=schemas.Token)
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """OAuth2PasswordRequestForm will give two values only username and password
    username can be any value id, mailid or name. that's why email is being compared to
    username (model.Users.email == user_credentials.username)
    """
    print("user_login called")
    check_user = (
        db.query(model.Users)
        .filter(model.Users.email == user_credentials.username)
        .first()
    )

    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    if not utils.verify(user_credentials.password, check_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials",
        )

    access_token = oauth2.create_access_token(data={"user_id": check_user.id})
    return {"access_token": access_token, "token_type": "bearer"}
