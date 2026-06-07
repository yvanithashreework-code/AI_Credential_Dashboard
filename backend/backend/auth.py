from datetime import datetime, timedelta
from jose import JWTError, jwt

# --------------------
# JWT Config
# --------------------
SECRET_KEY = "supersecretkey"   # ⚠️ change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --------------------
# Create JWT Token
# --------------------
def create_access_token(data: dict):
    """
    Generate a JWT access token with expiry.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --------------------
# Verify JWT Token
# --------------------
def verify_token(token: str):
    """
    Decode and verify JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
