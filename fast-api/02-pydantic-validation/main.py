"""
Chapter 02: Pydantic Models & Validation
==========================================
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum

app = FastAPI(title="Chapter 02 - Pydantic & Validation")


# ─── 1. Enums for Constrained Choices ────────────────────────────
class UserRole(str, Enum):
    """String enum — only these values are accepted."""
    admin = "admin"
    user = "user"
    moderator = "moderator"


class OrderStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"


# ─── 2. Nested Models ────────────────────────────────────────────
class Address(BaseModel):
    street: str = Field(..., min_length=1, examples=["123 Main Street"])
    city: str = Field(..., min_length=1, examples=["Lahore"])
    country: str = Field(default="Pakistan", examples=["Pakistan"])
    zip_code: Optional[str] = Field(None, pattern=r"^\d{5}$", examples=["54000"])


class SocialLinks(BaseModel):
    github: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None


# ─── 3. Complex Model with Validators ────────────────────────────
class UserCreate(BaseModel):
    """
    Full user creation schema with:
    - Type validation (automatic)
    - Field constraints (min/max, regex)
    - Custom field validators
    - Model-level validators
    """
    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr  # requires: pip install pydantic[email]
    password: str = Field(..., min_length=8, max_length=100)
    confirm_password: str = Field(..., min_length=8)
    age: int = Field(..., ge=13, le=120, description="Must be at least 13")
    role: UserRole = Field(default=UserRole.user)
    address: Address  # nested model
    social: Optional[SocialLinks] = None
    tags: list[str] = Field(default=[], max_length=10)

    # --- Field Validator: runs on a single field ---
    @field_validator("username")
    @classmethod
    def username_not_reserved(cls, v: str) -> str:
        reserved = {"admin", "root", "superuser", "system"}
        if v.lower() in reserved:
            raise ValueError(f"Username '{v}' is reserved")
        return v.lower()  # normalize to lowercase

    @field_validator("tags")
    @classmethod
    def normalize_tags(cls, v: list[str]) -> list[str]:
        return [tag.strip().lower() for tag in v if tag.strip()]

    # --- Model Validator: runs after all fields are validated ---
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserResponse(BaseModel):
    """What the client sees (no password fields!)."""
    id: int
    username: str
    email: EmailStr
    age: int
    role: UserRole
    address: Address
    social: Optional[SocialLinks] = None
    tags: list[str]
    created_at: datetime


# ─── 4. Order Models with Computed Validation ────────────────────
class OrderItem(BaseModel):
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=1000)
    unit_price: float = Field(..., gt=0)

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


class OrderCreate(BaseModel):
    items: list[OrderItem] = Field(..., min_length=1, max_length=50)
    discount_percent: float = Field(default=0.0, ge=0, le=50)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("items")
    @classmethod
    def no_duplicate_products(cls, v: list[OrderItem]) -> list[OrderItem]:
        names = [item.product_name.lower() for item in v]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate products in order")
        return v


class OrderResponse(BaseModel):
    id: int
    items: list[OrderItem]
    subtotal: float
    discount_percent: float
    total: float
    status: OrderStatus
    created_at: datetime


# ─── In-Memory Storage ───────────────────────────────────────────
users_db: dict[int, dict] = {}
orders_db: dict[int, dict] = {}
user_id_counter = 1
order_id_counter = 1


# ─── User Routes ─────────────────────────────────────────────────
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """
    Create a new user.
    Try sending invalid data to see Pydantic's error messages!

    Example invalid payloads to test:
    - Missing required fields → 422
    - age: 10 → "Must be at least 13"
    - username: "admin" → "Username 'admin' is reserved"
    - mismatched passwords → "Passwords do not match"
    - email: "not-an-email" → email validation error
    """
    global user_id_counter

    # Check for duplicate email
    for u in users_db.values():
        if u["email"] == user.email:
            raise HTTPException(status_code=409, detail="Email already registered")

    new_user = {
        "id": user_id_counter,
        **user.model_dump(exclude={"confirm_password"}),  # exclude password confirmation
        "created_at": datetime.now(),
    }
    users_db[user_id_counter] = new_user
    user_id_counter += 1
    return new_user


@app.get("/users", response_model=list[UserResponse])
def list_users():
    return list(users_db.values())


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]


# ─── Order Routes ────────────────────────────────────────────────
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
    """
    Create a new order.
    Subtotal and total are computed from items.
    """
    global order_id_counter

    subtotal = sum(item.quantity * item.unit_price for item in order.items)
    discount_amount = subtotal * (order.discount_percent / 100)
    total = subtotal - discount_amount

    new_order = {
        "id": order_id_counter,
        "items": [item.model_dump() for item in order.items],
        "subtotal": round(subtotal, 2),
        "discount_percent": order.discount_percent,
        "total": round(total, 2),
        "status": OrderStatus.pending,
        "created_at": datetime.now(),
    }
    orders_db[order_id_counter] = new_order
    order_id_counter += 1
    return new_order


# ─── Demonstrating model_dump Options ────────────────────────────
@app.get("/demo/model-dump")
def demo_model_dump():
    """Shows different ways to serialize Pydantic models."""
    address = Address(street="123 Main St", city="Lahore")
    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="securepass123",
        confirm_password="securepass123",
        age=25,
        address=address,
    )

    return {
        "full_dump": user_data.model_dump(),
        "exclude_password": user_data.model_dump(exclude={"password", "confirm_password"}),
        "only_username_email": user_data.model_dump(include={"username", "email"}),
        "json_schema": UserCreate.model_json_schema(),
    }
