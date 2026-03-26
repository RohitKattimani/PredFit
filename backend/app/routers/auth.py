from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models import User
from app.schemas import LoginIn, TokenOut, UserCreate, UserOut
from app.security import create_access_token, hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=UserOut)
def signup(payload: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == payload.email)).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        age=payload.age,
        gender=payload.gender,
        height_cm=payload.height_cm,
        weight_kg=payload.weight_kg,
        role="user",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserOut(
        id=user.id,
        email=user.email,
        role=user.role,
        age=user.age,
        gender=user.gender,
        height_cm=user.height_cm,
        weight_kg=user.weight_kg,
    )


@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == payload.email)).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token(subject=str(user.id), role=user.role)
    return TokenOut(access_token=token)

