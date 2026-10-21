import hashlib
import secrets
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from typing import List

from app.core.database import get_db
from app.schemas.user import UserResponse, UserCreate
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    salt = secrets.token_bytes(16)
    password_hash = hashlib.scrypt(user.password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1)
    new_user = User(
        email=user.email,
        hashed_password=f"scrypt${salt.hex()}${password_hash.hex()}",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).options(selectinload(User.tasks)).all()