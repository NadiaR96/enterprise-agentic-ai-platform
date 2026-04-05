from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

from .security import (
    authenticate_user,
    create_access_token,
    fake_users_db,
    get_current_active_user,
    User,
    Token
)

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str
    email: Optional[str] = None

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return JWT token."""
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.user_id, "roles": user.roles},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(form_data: RegisterRequest):
    """Register a new user (simplified for demo)."""
    if form_data.username in fake_users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    from .security import get_password_hash
    fake_users_db[form_data.username] = {
        "user_id": form_data.username,
        "email": form_data.email,
        "full_name": form_data.username,
        "disabled": False,
        "hashed_password": get_password_hash(form_data.password),
        "roles": ["user"]
    }
    return {"message": "User created successfully"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get current user information."""
    return current_user

@router.get("/users")
async def get_all_users(current_user: User = Depends(get_current_active_user)):
    """Get all users (admin only)."""
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=403, detail="Admin access required")

    return [
        {"user_id": uid, "email": user["email"], "roles": user["roles"]}
        for uid, user in fake_users_db.items()
    ]