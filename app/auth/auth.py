from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from app.models.models import TeacherCredentials
from app.schemas.schemas import TokenData
import os
import secrets
import hashlib

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Для нового кода используйте bcrypt (рекомендуется)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(session: Session, username: str, password: str):
    credentials = session.exec(select(TeacherCredentials).where(TeacherCredentials.username == username)).first()
    if not credentials:
        return False
    if not verify_password(password, credentials.password_hash):
        return False
    return credentials

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Старые функции (если они где-то используются)
def hash_password_sha256(password, salt=None):
    """
    Хеширование пароля с использованием salt (старая версия)
    """
    if salt is None:
        salt = secrets.token_hex(16)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return f"{salt}${hashed_password}"

def verify_password_sha256(stored_password, provided_password):
    """
    Проверка пароля (старая версия)
    """
    try:
        salt, hashed = stored_password.split('$')
        new_hash = hash_password_sha256(provided_password, salt)
        return new_hash == stored_password
    except:
        return False