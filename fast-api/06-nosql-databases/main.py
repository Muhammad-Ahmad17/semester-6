"""
Chapter 06: NoSQL Database Integration (MongoDB)
==================================================
pip install motor beanie
Run: uvicorn main:app --reload --port 8000

IMPORTANT: You need a running MongoDB instance.
- Local: Install MongoDB and run `mongod`
- Docker: docker run -d -p 27017:27017 --name mongodb mongo:7
- Cloud: Use MongoDB Atlas (free tier) and update MONGODB_URL

This chapter shows BOTH approaches:
- Part A: Raw Motor (low-level, like raw mongodb npm driver)
- Part B: Beanie ODM (high-level, like Mongoose)
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime, timezone
from contextlib import asynccontextmanager

# Motor — async MongoDB driver
from motor.motor_asyncio import AsyncIOMotorClient

# Beanie — ODM (like Mongoose for Python)
from beanie import Document, init_beanie, PydanticObjectId

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "fastapi_learning"


# ═══════════════════════════════════════════════════════════════════
# BEANIE DOCUMENT MODELS (Like Mongoose Schemas)
# ═══════════════════════════════════════════════════════════════════

class Address(BaseModel):
    """Embedded document (like Mongoose subdocument)."""
    street: str = ""
    city: str = ""
    country: str = "Pakistan"


class Product(Document):
    """
    Beanie Document = Mongoose Model.
    Each instance is a MongoDB document.
    """
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0)
    category: str = "general"
    tags: list[str] = []
    in_stock: bool = True
    quantity: int = Field(ge=0, default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "products"  # MongoDB collection name


class Customer(Document):
    name: str
    email: str  # Using plain str to avoid extra dependency
    age: Optional[int] = Field(None, ge=0)
    address: Address = Address()
    is_active: bool = True
    orders: list[str] = []  # list of product IDs
    registered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "customers"


# ═══════════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS (Request/Response shapes)
# ═══════════════════════════════════════════════════════════════════

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category: str = "general"
    tags: list[str] = []
    quantity: int = Field(ge=0, default=0)


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    tags: Optional[list[str]] = None
    in_stock: Optional[bool] = None
    quantity: Optional[int] = Field(None, ge=0)


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: str
    age: Optional[int] = Field(None, ge=0)
    address: Address = Address()


# ═══════════════════════════════════════════════════════════════════
# APP SETUP
# ═══════════════════════════════════════════════════════════════════

# Global motor client reference
motor_client: Optional[AsyncIOMotorClient] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global motor_client

    # STARTUP: Connect to MongoDB
    print(f"Connecting to MongoDB at {MONGODB_URL}...")
    motor_client = AsyncIOMotorClient(MONGODB_URL)

    # Initialize Beanie with document models
    await init_beanie(
        database=motor_client[DATABASE_NAME],
        document_models=[Product, Customer],
    )
    print("MongoDB connected and Beanie initialized!")

    yield  # App runs here

    # SHUTDOWN: Close connection
    print("Closing MongoDB connection...")
    motor_client.close()


app = FastAPI(title="Chapter 06 - MongoDB Integration", lifespan=lifespan)


# ═══════════════════════════════════════════════════════════════════
# PART A: RAW MOTOR (Low-Level — like raw mongodb npm driver)
# ═══════════════════════════════════════════════════════════════════

@app.get("/motor/stats")
async def motor_stats():
    """Direct Motor query — get collection stats."""
    db = motor_client[DATABASE_NAME]
    collections = await db.list_collection_names()
    stats = {}
    for col in collections:
        count = await db[col].count_documents({})
        stats[col] = count
    return {"database": DATABASE_NAME, "collections": stats}


@app.get("/motor/products/search")
async def motor_search_products(
    q: str = Query(..., min_length=1),
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
):
    """
    Raw Motor aggregation pipeline.
    Like using MongoDB's native driver in Node.js:
    db.collection('products').aggregate([...])
    """
    db = motor_client[DATABASE_NAME]

    # Build MongoDB query filter
    filter_query: dict = {
        "$or": [
            {"name": {"$regex": q, "$options": "i"}},
            {"description": {"$regex": q, "$options": "i"}},
            {"tags": {"$in": [q.lower()]}},
        ]
    }

    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        filter_query["price"] = price_filter

    # Execute query
    cursor = db.products.find(filter_query).sort("price", 1).limit(20)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
        results.append(doc)

    return {"query": q, "count": len(results), "results": results}


# ═══════════════════════════════════════════════════════════════════
# PART B: BEANIE ODM (High-Level — like Mongoose)
# ═══════════════════════════════════════════════════════════════════

# ─── Product CRUD ────────────────────────────────────────────────

@app.post("/products", status_code=201)
async def create_product(data: ProductCreate):
    """
    Mongoose equivalent:
    const product = await Product.create({ name, price, ... })
    """
    product = Product(**data.model_dump())
    await product.insert()
    return product


@app.get("/products")
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    sort_by: str = Query("created_at", pattern="^(name|price|created_at)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
):
    """
    Mongoose equivalent:
    Product.find(filter).sort(sort).skip(skip).limit(limit)
    """
    # Build query
    query_filter = {}
    if category:
        query_filter["category"] = category
    if in_stock is not None:
        query_filter["in_stock"] = in_stock

    # Beanie query
    sort_prefix = "+" if order == "asc" else "-"
    products = (
        await Product.find(query_filter)
        .sort(f"{sort_prefix}{sort_by}")
        .skip(skip)
        .limit(limit)
        .to_list()
    )
    total = await Product.find(query_filter).count()

    return {"items": products, "total": total, "skip": skip, "limit": limit}


@app.get("/products/{product_id}")
async def get_product(product_id: PydanticObjectId):
    """
    Mongoose equivalent: Product.findById(id)
    PydanticObjectId auto-validates MongoDB ObjectId format!
    """
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@app.put("/products/{product_id}")
async def update_product(product_id: PydanticObjectId, data: ProductUpdate):
    """
    Mongoose equivalent: Product.findByIdAndUpdate(id, update, { new: true })
    """
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    await product.save()
    return product


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: PydanticObjectId):
    """Mongoose equivalent: Product.findByIdAndDelete(id)"""
    product = await Product.get(product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    await product.delete()


# ─── Customer CRUD ───────────────────────────────────────────────

@app.post("/customers", status_code=201)
async def create_customer(data: CustomerCreate):
    customer = Customer(**data.model_dump())
    await customer.insert()
    return customer


@app.get("/customers")
async def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active_only: bool = Query(False),
):
    filter_q = {"is_active": True} if active_only else {}
    customers = await Customer.find(filter_q).skip(skip).limit(limit).to_list()
    total = await Customer.find(filter_q).count()
    return {"items": customers, "total": total}


@app.get("/customers/{customer_id}")
async def get_customer(customer_id: PydanticObjectId):
    customer = await Customer.get(customer_id)
    if not customer:
        raise HTTPException(404, "Customer not found")
    return customer


# ─── Aggregation Pipeline (Advanced MongoDB) ─────────────────────

@app.get("/analytics/products")
async def product_analytics():
    """
    MongoDB Aggregation Pipeline — like Mongoose's .aggregate()
    Computes per-category statistics.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_products": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "total_quantity": {"$sum": "$quantity"},
                "in_stock_count": {
                    "$sum": {"$cond": [{"$eq": ["$in_stock", True]}, 1, 0]}
                },
            }
        },
        {"$sort": {"total_products": -1}},
    ]

    db = motor_client[DATABASE_NAME]
    results = []
    async for doc in db.products.aggregate(pipeline):
        doc["category"] = doc.pop("_id")
        results.append(doc)

    return {"analytics": results}


@app.get("/")
async def root():
    return {
        "message": "Chapter 06 - MongoDB Integration",
        "motor_example": "/motor/stats",
        "beanie_example": "/products",
        "analytics": "/analytics/products",
    }
