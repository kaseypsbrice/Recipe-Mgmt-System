from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your-very-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(plain_password: str) -> str:
    return (pwd_context.hash(plain_password))
# Returns plain text password as a hash

def verify_password(plain_password: str, hashed_password: str) -> str:
    return (pwd_context.verify(plain_password, hashed_password))
# Checks if the plain text password matches the stored hash

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return {}