from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_passw: str, hashed_passw: str) -> bool:
    return password_context.verify(plain_passw, hashed_passw)
