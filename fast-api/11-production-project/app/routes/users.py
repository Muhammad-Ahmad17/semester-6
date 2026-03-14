from fastapi import APIRouter, HTTPException, Query
from app.dependencies import DB, CurrentUser, AdminUser
from app.models.user import DBUser
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(user: CurrentUser):
    return user


@router.get("/", response_model=list[UserResponse])
def list_users(
    db: DB,
    admin: AdminUser,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return db.query(DBUser).offset(skip).limit(limit).all()
