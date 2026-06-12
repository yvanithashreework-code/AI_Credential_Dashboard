import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import exceptions

# ⚠️ SECRET_KEY ko settings.py me rakho, hardcode mat karo
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(user):
    """
    Create JWT token for authenticated user
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user.username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """
    Verify JWT token and return username
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exceptions.AuthenticationFailed("Invalid token")
        return username
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Token expired")
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Invalid token")


def login_user(username: str, password: str):
    """
    Authenticate user with Django's built-in auth system
    """
    user = authenticate(username=username, password=password)
    if not user:
        raise exceptions.AuthenticationFailed("Invalid credentials")
    token = create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}
