from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    return (pwd_context.hash(plain_password))
# Returns plain text password as a hash

def verify_password(plain_password: str, hashed_password: str) -> str:
    return (pwd_context.verify(plain_password, hashed_password))
# Checks if the plain text password matches the stored hash