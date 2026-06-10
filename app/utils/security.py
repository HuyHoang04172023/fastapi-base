import hashlib
from datetime import datetime, timedelta
from jose import jwt

from models.user import User
from utils.configs import project_settings


def generate_token(user: User, time_delta: int) -> str:
    expire = datetime.now() + timedelta(minutes=time_delta)
    data_encode = {
        'id': user.id,
        'email': user.email,
        'admin': user.is_admin,
        'active': user.is_active,
        'exp': expire
    }
    encoded_jwt = jwt.encode(data_encode, project_settings.SECRET_KEY, algorithm=project_settings.ALGORITHM)
    return encoded_jwt


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()
