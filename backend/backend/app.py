from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

# --------------------
# FastAPI app instance
# --------------------
app = FastAPI(title="AI Credential Dashboard Backend")

# --------------------
# JWT Config
# --------------------
SECRET_KEY = "supersecretkey"   # ⚠️ change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --------------------
# Helper function
# --------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

# --------------------
# Routes
# --------------------
@app.get("/")
def root():
    return {"message": "Backend API is running 🚀"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Dummy user check (replace with DB later)
    if form_data.username == "admin" and form_data.password == "admin123":
        token = create_access_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/filters")
def get_filters(
    department: str = None,
    role: str = None,
    experience: int = None,
    token: str = Depends(oauth2_scheme)
):
    # Verify token
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    # Dummy employee data
    employees = [
        {"name": "Alice", "department": "HR", "role": "Manager", "experience": 5},
        {"name": "Bob", "department": "IT", "role": "Developer", "experience": 3},
        {"name": "Charlie", "department": "Finance", "role": "Analyst", "experience": 4},
    ]

    # Apply filters
    results = []
    for emp in employees:
        if department and emp["department"] != department:
            continue
        if role and emp["role"] != role:
            continue
        if experience and emp["experience"] < experience:
            continue
        results.append(emp)

    return {"filters": results}
