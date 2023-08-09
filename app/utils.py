from passlib.context import CryptContext

# we are just telling the passlib is default hashing algorithm is bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)
