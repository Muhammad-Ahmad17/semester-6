from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies import DB
from app.models.user import DBUser
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from app.services.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: DB):
    if db.query(DBUser).filter(DBUser.email == user.email).first():
        raise HTTPException(409, "Email already registered")
    if db.query(DBUser).filter(DBUser.username == user.username).first():
        raise HTTPException(409, "Username already taken")

    db_user = DBUser(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: DB = None):
    """Login with username + password, get JWT token."""
    user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")
    if not user.is_active:
        raise HTTPException(403, "Account deactivated")

    token = create_access_token(data={"sub": user.id, "role": user.role})
    return TokenResponse(access_token=token)
