"""
Chapter 01: FastAPI Fundamentals
=================================
Run: uvicorn main:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

from fastapi import FastAPI, status, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import Optional

# ─── Initialize App ───────────────────────────────────────────────
# Express equivalent: const app = express()
app = FastAPI(
    title="Chai have prior expericence of node js as backend , but now i want to go for fast api , from begining to advanve , with connection of dbs , cloud integration , ai integration , so what i want section wise learning docs and code like a topic in a section have code and markdown containing theory relevent to that codepter 01 - FastAPI Fundamentals",
    description="Learning FastAPI basics coming from Node.js",
    version="1.0.0",
)

# ─── In-Memory Database (like a simple array in Node.js) ──────────
fake_db: dict[int, dict] = {
    1: {"id": 1, "name": "Laptop", "price": 999.99, "in_stock": True},
    2: {"id": 2, "name": "Mouse", "price": 29.99, "in_stock": True},
    3: {"id": 3, "name": "Keyboard", "price": 79.99, "in_stock": False},
}
next_id = 4


# ─── Pydantic Models (Request/Response Schemas) ──────────────────
class ItemCreate(BaseModel):
    """Schema for creating an item (request body)."""
    name: str = Field(..., min_length=1, max_length=100, examples=["Laptop"])
    price: float = Field(..., gt=0, examples=[999.99])
    in_stock: bool = Field(default=True)


class ItemResponse(BaseModel):
    """Schema for item response (what client sees)."""
    id: int
    name: str
    price: float
    in_stock: bool


class ItemUpdate(BaseModel):
    """Schema for partial updates (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    in_stock: Optional[bool] = None


# ─── Route 1: Root ────────────────────────────────────────────────
# Express: app.get('/', (req, res) => res.json({message: "Hello World"}))
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!", "docs": "/docs"}


# ─── Route 2: GET all items with Query Parameters ────────────────
# Express: app.get('/items', (req, res) => {
#   const skip = parseInt(req.query.skip) || 0;
#   const limit = parseInt(req.query.limit) || 10;
# })
@app.get("/items", response_model=list[ItemResponse])
def list_items(
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
):
    """List all items with pagination (skip/limit)."""
    items = list(fake_db.values())
    return items[skip : skip + limit]


# ─── Route 3: GET single item with Path Parameter ────────────────
# Express: app.get('/items/:item_id', (req, res) => {
#   const id = parseInt(req.params.item_id);
# })
@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int = Path(..., gt=0, description="The ID of the item to retrieve"),
):
    """Get a single item by ID."""
    if item_id not in fake_db:
        # Express equivalent: res.status(404).json({detail: "Item not found"})
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]


# ─── Route 4: POST create item with Request Body ─────────────────
# Express: app.post('/items', (req, res) => {
#   const { name, price, in_stock } = req.body
# })
@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    """Create a new item. Body is automatically validated by Pydantic."""
    global next_id
    new_item = {"id": next_id, **item.model_dump()}
    fake_db[next_id] = new_item
    next_id += 1
    return new_item


# ─── Route 5: PUT update item ────────────────────────────────────
# Express: app.put('/items/:item_id', (req, res) => { ... })
@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate):
    """Update an item (partial update - only send fields you want to change)."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored = fake_db[item_id]
    update_data = item.model_dump(exclude_unset=True)  # only fields that were sent
    stored.update(update_data)
    return stored


# ─── Route 6: DELETE item ────────────────────────────────────────
# Express: app.delete('/items/:item_id', (req, res) => { ... })
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del fake_db[item_id]
    return None  # 204 No Content


# ─── Route 7: Search with multiple query params ──────────────────
# Express: app.get('/search', (req, res) => {
#   const { q, max_price, in_stock_only } = req.query
# })
@app.get("/search", response_model=list[ItemResponse])
def search_items(
    q: Optional[str] = Query(None, min_length=1, description="Search term"),
    max_price: Optional[float] = Query(None, gt=0, description="Maximum price"),
    in_stock_only: bool = Query(False, description="Only show in-stock items"),
):
    """Search items with filters."""
    results = list(fake_db.values())

    if q:
        results = [i for i in results if q.lower() in i["name"].lower()]
    if max_price is not None:
        results = [i for i in results if i["price"] <= max_price]
    if in_stock_only:
        results = [i for i in results if i["in_stock"]]

    return results


# ─── Route 8: Async route ────────────────────────────────────────
# FastAPI supports async/await just like Node.js
# Use `async def` when you have I/O-bound operations (DB, HTTP calls, file I/O)
@app.get("/async-demo")
async def async_demo():
    """
    Use 'async def' for I/O-bound operations.
    Use plain 'def' for CPU-bound operations (FastAPI runs them in a thread pool).
    """
    import asyncio
    await asyncio.sleep(0.1)  # simulating an async I/O operation
    return {"message": "This was an async operation!"}
