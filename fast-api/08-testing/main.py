"""
Chapter 08: The App Being Tested
==================================
A small self-contained app that we will write tests for.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Chapter 08 - App Under Test")

# ─── In-memory DB ────────────────────────────────────────────────
items_db: dict[int, dict] = {}
next_id = 1


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    category: str = "general"


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    category: str


# ─── Dependency ──────────────────────────────────────────────────
def get_current_user(x_token: str = None) -> dict:
    """Simple token-based auth dependency."""
    if x_token == "valid-token":
        return {"id": 1, "name": "Test User", "role": "admin"}
    elif x_token == "user-token":
        return {"id": 2, "name": "Normal User", "role": "user"}
    raise HTTPException(401, "Invalid token")


# ─── Routes ──────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Testing chapter app"}


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    global next_id
    new = {"id": next_id, **item.model_dump()}
    items_db[next_id] = new
    next_id += 1
    return new


@app.get("/items", response_model=list[ItemResponse])
def list_items(category: Optional[str] = None):
    items = list(items_db.values())
    if category:
        items = [i for i in items if i["category"] == category]
    return items


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    return items_db[item_id]


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    for k, v in update.model_dump(exclude_unset=True).items():
        items_db[item_id][k] = v
    return items_db[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(404, "Item not found")
    del items_db[item_id]


@app.get("/protected")
def protected_route(user: dict = Depends(get_current_user)):
    return {"message": f"Hello {user['name']}", "role": user["role"]}
