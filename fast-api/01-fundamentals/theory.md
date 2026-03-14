# Chapter 01: FastAPI Fundamentals

## Why FastAPI? (Coming from Node.js/Express)

| Feature | Express (Node.js) | FastAPI (Python) |
|---|---|---|
| Type Safety | Manual (TypeScript optional) | Built-in (Pydantic + type hints) |
| Auto Docs | Swagger via plugins | Swagger + ReDoc built-in |
| Async Support | Native (event loop) | Native (`async/await`) |
| Validation | Manual or Joi/Zod | Pydantic (automatic) |
| Performance | Fast (V8) | Very fast (Starlette + Uvicorn, on par with Node) |
| Learning Curve | Low | Low (especially with Python knowledge) |

## Core Concepts

### 1. ASGI vs WSGI
- **WSGI** (Web Server Gateway Interface): Synchronous, one request at a time per worker (Flask, Django).
- **ASGI** (Asynchronous Server Gateway Interface): Async, handles many concurrent connections (FastAPI, Starlette).
- FastAPI is built on **Starlette** (ASGI framework) and uses **Uvicorn** as the ASGI server.

### 2. How FastAPI Works
```
Client Request → Uvicorn (ASGI Server) → Starlette (Routing) → FastAPI (Validation + Serialization) → Your Function
```

### 3. Path Operations (Routes)
In Express you write `app.get('/path', handler)`. In FastAPI it's similar but uses **decorators**:
```python
@app.get("/path")          # Express equivalent: app.get('/path', ...)
@app.post("/path")         # Express equivalent: app.post('/path', ...)
@app.put("/path/{id}")     # Express equivalent: app.put('/path/:id', ...)
@app.delete("/path/{id}")  # Express equivalent: app.delete('/path/:id', ...)
```

### 4. Path Parameters vs Query Parameters
```python
# Path parameter — /users/42
@app.get("/users/{user_id}")
def get_user(user_id: int):  # FastAPI auto-validates that user_id is int
    ...

# Query parameter — /users?skip=0&limit=10
@app.get("/users")
def list_users(skip: int = 0, limit: int = 10):
    ...
```
- **Path params** are part of the URL path (required).
- **Query params** are after `?` (optional with defaults).

### 5. Request Body
In Express: `req.body`. In FastAPI: you define a **Pydantic model**.
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):  # FastAPI auto-parses & validates JSON body
    return item
```

### 6. Response Model
FastAPI can filter and document your response shape:
```python
@app.get("/items/{id}", response_model=Item)
def get_item(id: int):
    return {"name": "Widget", "price": 9.99, "internal_secret": "hidden"}
    # "internal_secret" will be stripped from response!
```

### 7. Status Codes
```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item
```

### 8. Automatic Interactive Docs
Once your app runs, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

No setup needed — FastAPI generates these from your type hints and models.

## Setup Instructions

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install fastapi uvicorn[standard]

# Run the server
uvicorn main:app --reload --port 8000
```

## Node.js → FastAPI Cheat Sheet

| Express.js | FastAPI |
|---|---|
| `const app = express()` | `app = FastAPI()` |
| `app.get('/path', (req, res) => {})` | `@app.get("/path") def handler():` |
| `req.params.id` | `def handler(id: int):` (path param) |
| `req.query.page` | `def handler(page: int = 1):` (query param) |
| `req.body` | `def handler(item: ItemModel):` (Pydantic model) |
| `res.json({...})` | `return {...}` (auto-serialized) |
| `res.status(201).json()` | `status_code=201` in decorator |
| `app.listen(3000)` | `uvicorn main:app --port 8000` |
