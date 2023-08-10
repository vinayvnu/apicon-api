from jose import JWTError, jwt

# we need to provide secret key and the algorithm we want to use.
# we need to provide expiration time of token. If expiration time is not provided, then the user will
# allowed to be logged in forever.

SECRET_KEY = "dat4q5q424gf56asfrty5w6wgreg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_toke(data: dict):
    data.copy()