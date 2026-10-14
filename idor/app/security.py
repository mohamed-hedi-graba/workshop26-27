from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import Depends, Request, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models import User

SECRET_KEY = "inkwell-dev-secret-key"
ALGORITHM = "HS256"
TOKEN_TTL_HOURS = 24
COOKIE_NAME = "session"


def create_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(hours=TOKEN_TTL_HOURS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _user_from_token(token: Optional[str], db: Session) -> Optional[User]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def get_optional_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get(COOKIE_NAME)
    return _user_from_token(token, db)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    token = request.cookies.get(COOKIE_NAME)
    user = _user_from_token(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
