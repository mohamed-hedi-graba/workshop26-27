from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import RegisterIn, LoginIn, UserPublic
from ..security import create_token, COOKIE_NAME, TOKEN_TTL_HOURS

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=UserPublic)
def register(data: RegisterIn, response: Response, db: Session = Depends(get_db)):
    existing = (
        db.query(User)
        .filter((User.username == data.username) | (User.email == data.email))
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already in use")

    user = User(
        username=data.username,
        email=data.email,
        password=data.password,
        role="user",
        bio="",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_token(user.id)
    response.set_cookie(
        COOKIE_NAME, token, httponly=True, max_age=TOKEN_TTL_HOURS * 3600, samesite="lax"
    )
    return user


@router.post("/login", response_model=UserPublic)
def login(data: LoginIn, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if user is None or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(user.id)
    response.set_cookie(
        COOKIE_NAME, token, httponly=True, max_age=TOKEN_TTL_HOURS * 3600, samesite="lax"
    )
    return user


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
    return {"ok": True}
