import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Security configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Security schemes
security = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    roles: list[str] = []

class User(BaseModel):
    user_id: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    roles: list[str] = ["user"]

class UserInDB(User):
    hashed_password: Optional[str] = None

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password (simplified for demo - use proper hashing in production)."""
    # For demo purposes, using plain text comparison
    # In production, use proper password hashing
    return plain_password == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password (simplified for demo)."""
    # For demo purposes, return plain text
    # In production, use proper password hashing like bcrypt
    return password

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        roles: list = payload.get("roles", [])
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id, roles=roles)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    token_data = verify_token(token, credentials_exception)

    # In a real app, you'd fetch user from database
    # For now, create a mock user
    user = User(
        user_id=token_data.user_id,
        roles=token_data.roles
    )
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get the current active user."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(*required_roles: str):
    """Decorator to require specific roles."""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if not any(role in current_user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

# Mock user database - in production, use real database
fake_users_db = {
    "admin": {
        "user_id": "admin",
        "email": "admin@example.com",
        "full_name": "Admin User",
        "disabled": False,
        "hashed_password": "admin",  # Plain text for demo
        "roles": ["admin", "user"]
    },
    "user1": {
        "user_id": "user1",
        "email": "user1@example.com",
        "full_name": "Regular User",
        "disabled": False,
        "hashed_password": "password",  # Plain text for demo
        "roles": ["user"]
    }
}

def authenticate_user(fake_db, user_id: str, password: str):
    """Authenticate a user."""
    user = fake_db.get(user_id)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return UserInDB(**user)