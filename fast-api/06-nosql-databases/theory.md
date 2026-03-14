# Chapter 06: NoSQL Database Integration (MongoDB + Motor)

## Overview

If you've used **Mongoose** in Node.js, this chapter will feel familiar. MongoDB is a document database — data is stored as JSON-like documents instead of rows in tables.

### Node.js → Python MongoDB Mapping

| Node.js (Mongoose) | Python (FastAPI) |
|---|---|
| `mongoose` | `motor` (async driver) + `beanie` (ODM) |
| `mongoose.connect(url)` | `motor.AsyncIOMotorClient(url)` |
| `mongoose.Schema` | Beanie `Document` or raw dicts |
| `Model.find()` | `collection.find()` |
| `Model.findById()` | `collection.find_one({"_id": id})` |
| `Model.create()` | `collection.insert_one()` |
| `Model.findByIdAndUpdate()` | `collection.update_one()` |

## Two Approaches

### 1. Motor (Low-Level Async Driver)
Direct MongoDB operations — like using the raw `mongodb` npm package.
```python
from motor.motor_asyncio import AsyncIOMotorClient
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.mydb
result = await db.users.find_one({"email": "test@test.com"})
```

### 2. Beanie (ODM — Object Document Mapper)
Like Mongoose — define models with schemas and validation.
```python
from beanie import Document

class User(Document):
    name: str
    email: str

    class Settings:
        name = "users"  # collection name
```

## MongoDB Document Structure

```json
{
    "_id": ObjectId("507f1f77bcf86cd799439011"),
    "name": "Ahmad",
    "email": "ahmad@example.com",
    "address": {
        "city": "Lahore",
        "country": "Pakistan"
    },
    "tags": ["developer", "python"],
    "created_at": ISODate("2025-01-01T00:00:00Z")
}
```

- Documents are like JSON objects (no fixed schema)
- Can have nested objects and arrays
- `_id` is auto-generated (like MongoDB's default)

## When to Use MongoDB vs PostgreSQL

| Use MongoDB When | Use PostgreSQL When |
|---|---|
| Schema changes frequently | Schema is well-defined |
| Storing JSON-like documents | Complex joins needed |
| Rapid prototyping | ACID transactions critical |
| Nested/hierarchical data | Relational data |
| Horizontal scaling needed | Data integrity is priority |

## Dependencies

```bash
pip install motor beanie
```

## Connection String Formats

```python
# Local MongoDB
"mongodb://localhost:27017"

# MongoDB Atlas (Cloud)
"mongodb+srv://username:password@cluster.mongodb.net/dbname"

# With authentication
"mongodb://username:password@localhost:27017/dbname?authSource=admin"
```
