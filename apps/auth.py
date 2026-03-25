from passlib.context import CryptContext
from passlib.exc import UnknownHashError

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256", "bcrypt"],
    deprecated="auto",
)


def hash_password(password: str):
    # 🔥 FIX: limit password length
    password = password[:72]
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    if not hashed_password:
        return False

    plain_password = plain_password[:72]
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except (UnknownHashError, ValueError):
        return False
