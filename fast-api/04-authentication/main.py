"""
Chapter 04: Authentication & Authorization
============================================
pip install python-jose[cryptography] passlib[bcrypt] pydantic[email]
Run: uvicorn main:app --reload --port 8000

Test flow:
1. POST /auth/register → create user
2. POST /auth/token → get JWT (use form data: username + password)
3. GET /auth/me → send "Authorization: Bearer <token>"
4. GET /admin/users → admin-only endpoint
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from enum import Enum

app = FastAPI(title="Chapter 04 - Authentication & Authorization")

# ─── Configuration ───────────────────────────────────────────────
SECRET_KEY = "your-super-secret-key-change-in-production"  # Use env var in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# ─── Password Hashing ───────────────────────────────────────────
# Express equivalent: const bcrypt = require('bcrypt')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """bcrypt.hash(password, saltRounds) in Node.js"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """bcrypt.compare(password, hash) in Node.js"""
    return pwd_context.verify(plain_password, hashed_password)


# ─── JWT Token Creation ─────────────────────────────────────────
# Express equivalent: jwt.sign(payload, SECRET, { expiresIn: '30m' })
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ─── OAuth2 Scheme ───────────────────────────────────────────────
# This tells FastAPI to look for "Authorization: Bearer <token>" header
# It also creates a "login" button in Swagger UI!
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# ─── Models ──────────────────────────────────────────────────────
class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: UserRole = UserRole.user


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    created_at: datetime
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


# ─── Fake Database ───────────────────────────────────────────────
users_db: dict[int, dict] = {
    1: {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": hash_password("admin123456"),
        "role": "admin",
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }
}
user_id_counter = 2


# ─── Core Auth Dependencies ─────────────────────────────────────
async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Express equivalent:
    function authMiddleware(req, res, next) {
        const token = req.headers.authorization?.split(' ')[1]
        const decoded = jwt.verify(token, SECRET)
        req.user = decoded
        next()
    }
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_db.get(user_id)
    if user is None:
        raise credentials_exception
    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user


async def get_current_active_user(user: dict = Depends(get_current_user)) -> dict:
    if not user["is_active"]:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# ─── Role-Based Access Control ───────────────────────────────────
def require_role(*allowed_roles: str):
    """
    Factory function that creates a dependency for role checking.
    Usage: dependencies=[Depends(require_role("admin", "moderator"))]
    """
    def role_checker(user: dict = Depends(get_current_user)) -> dict:
        if user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user['role']}' not authorized. Required: {allowed_roles}",
            )
        return user
    return role_checker


# Type aliases for cleaner route signatures
CurrentUser = Annotated[dict, Depends(get_current_active_user)]
AdminUser = Annotated[dict, Depends(require_role("admin"))]


# ═══════════════════════════════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/auth/register", response_model=UserResponse, status_code=201)
def register(user: UserRegister):
    """Register a new user."""
    global user_id_counter

    # Check duplicate email
    for u in users_db.values():
        if u["email"] == user.email:
            raise HTTPException(409, "Email already registered")
        if u["username"] == user.username:
            raise HTTPException(409, "Username already taken")

    new_user = {
        "id": user_id_counter,
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password),
        "role": user.role.value,
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@app.post("/auth/token", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login and get JWT tokens.
    In Swagger UI, click the Authorize button and enter username + password.

    Default admin:  username=admin  password=admin123456
    """
    # Find user by username
    user = None
    for u in users_db.values():
        if u["username"] == form_data.username:
            user = u
            break

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["is_active"]:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    # Create tokens
    access_token = create_access_token(
        data={"sub": user["id"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(data={"sub": user["id"]})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@app.post("/auth/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshRequest):
    """Get a new access token using a refresh token."""
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "refresh" or user_id is None:
            raise HTTPException(401, "Invalid refresh token")
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")

    user = users_db.get(user_id)
    if not user:
        raise HTTPException(401, "User not found")

    new_access = create_access_token(
        data={"sub": user["id"], "role": user["role"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh = create_refresh_token(data={"sub": user["id"]})

    return TokenResponse(
        access_token=new_access,
        refresh_token=new_refresh,
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ═══════════════════════════════════════════════════════════════════
# PROTECTED ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.get("/auth/me", response_model=UserResponse)
def get_me(user: CurrentUser):
    """Get current user profile. Requires valid access token."""
    return user


@app.put("/auth/me")
def update_profile(
    update: dict,
    user: CurrentUser,
):
    """Update your own profile (limited fields)."""
    allowed_fields = {"email", "username"}
    filtered = {k: v for k, v in update.items() if k in allowed_fields}
    users_db[user["id"]].update(filtered)
    return users_db[user["id"]]


# ═══════════════════════════════════════════════════════════════════
# ADMIN ROUTES (Role-based)
# ═══════════════════════════════════════════════════════════════════

@app.get("/admin/users", response_model=list[UserResponse])
def admin_list_users(admin: AdminUser):
    """Admin only — list all users."""
    return list(users_db.values())


@app.put("/admin/users/{user_id}/deactivate")
def admin_deactivate_user(user_id: int, admin: AdminUser):
    """Admin only — deactivate a user."""
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    if user_id == admin["id"]:
        raise HTTPException(400, "Cannot deactivate yourself")
    users_db[user_id]["is_active"] = False
    return {"message": f"User {user_id} deactivated"}


@app.put("/admin/users/{user_id}/role")
def admin_change_role(user_id: int, role: UserRole, admin: AdminUser):
    """Admin only — change a user's role."""
    if user_id not in users_db:
        raise HTTPException(404, "User not found")
    users_db[user_id]["role"] = role.value
    return {"message": f"User {user_id} role changed to {role.value}"}
