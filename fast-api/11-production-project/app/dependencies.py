"""Shared dependencies used across routes."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import SessionLocal
from app.models.user import DBUser
from app.services.auth import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> DBUser:
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

    user = db.query(DBUser).filter(DBUser.id == payload.get("sub")).first()
    if not user or not user.is_active:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found or inactive")
    return user


def require_admin(user: DBUser = Depends(get_current_user)) -> DBUser:
    if user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Admin access required")
    return user


# Type aliases for cleaner signatures
DB = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[DBUser, Depends(get_current_user)]
AdminUser = Annotated[DBUser, Depends(require_admin)]
