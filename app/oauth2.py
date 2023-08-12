from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, sqlalchemy, model
from config import settings

# this is the endpoint of login
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

"""SECRET_KEY (this is any string text provided)
ALGORITHM (algorithm for encryption will be HS256)
ACCESS_TOKEN_EXPIRE_MINUTES (this is the duration for which the 
secret will be valid and the connection will be valid)
we need to provide secret key and the algorithm we want to use."""
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

"""we need to provide expiration time of token. If expiration time is not provided, 
then the user will allowed to be logged in forever."""
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

"""data provided in the create_access_token will be encoded. the data provided in dict format."""


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # expire time is added to the copy of data
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# its use is just to verify the token only.
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id_extracted: str = payload.get("user_id")

        if id_extracted is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id_extracted)
    except JWTError as e:
        print(e)
        raise credentials_exception
    return token_data


# get_current_user function will take the token from the request automatically extract the id,
# verify the token is correct by calling verify_access_token and its going to extract the id
# once the user is confirmed by verify_access_token, get_current_user will fetch the user from db
def get_current_user(
    token: str = Depends(oauth_scheme), db: Session = Depends(sqlalchemy.get_db())
):
    print("get_current_user called.")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(model.Users).filter(model.Users.id == token.id).first()
    # return verify_access_token(token, credentials_exception)
    return user
