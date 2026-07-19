from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from ..database import engine
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os
import bcrypt

router = APIRouter(prefix="/auth", tags=["Auth"])

# ==================== PASSWORD HASHING ====================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def get_password_hash(password: str) -> str:
    # Ensure password is max 72 bytes
    password = password[:72]
    # Hash using bcrypt directly
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

# ==================== JWT ====================
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ==================== SCHEMAS ====================
class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

# ==================== ROUTES ====================

@router.get("/test")
async def test():
    return {"message": "Auth router working!"}

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    try:
        with engine.connect() as conn:
            existing = conn.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": user.email}
            ).fetchone()

            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")

            # Strong truncation (double safety)
            password = user.password[:72].encode('utf-8')[:72].decode('utf-8', errors='ignore')
            hashed_password = get_password_hash(password)

            conn.execute(text("""
                INSERT INTO users (email, hashed_password, full_name)
                VALUES (:email, :password, :full_name)
            """), {
                "email": user.email,
                "password": hashed_password,
                "full_name": user.full_name
            })
            conn.commit()

            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        with engine.connect() as conn:
            user = conn.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {"email": form_data.username}
            ).fetchone()

            if not user or not verify_password(form_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password"
                )

            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )


# ==================== GET CURRENT USER ====================
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with engine.connect() as conn:
        user = conn.execute(
            text("SELECT id, email, full_name FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()

    if user is None:
        raise credentials_exception

    return {"id": user.id, "email": user.email, "full_name": user.full_name}