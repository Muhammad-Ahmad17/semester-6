# Chapter 02: Pydantic Models & Validation

## What is Pydantic?

Pydantic is a **data validation library** that uses Python type hints. It's the backbone of FastAPI's request/response handling.

**Node.js analogy**: Pydantic = **Zod + TypeScript interfaces** combined.
In Express, you'd use Joi or Zod to validate `req.body`. In FastAPI, Pydantic does this automatically.

## Core Concepts

### 1. BaseModel — The Foundation
Every schema inherits from `BaseModel`. Fields are declared as class attributes with type annotations.

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
```

When FastAPI receives a JSON body, it:
1. Parses the raw JSON
2. Creates a `User` instance (validates all fields)
3. Returns **422 Unprocessable Entity** if validation fails

### 2. Field Types & Defaults

```python
class Product(BaseModel):
    name: str                      # required
    price: float                   # required
    description: str = "N/A"       # optional with default
    tags: list[str] = []           # optional list with default
    metadata: dict[str, str] = {}  # optional dict
    is_active: bool = True         # optional bool
```

### 3. The `Field()` Function — Fine-Grained Validation

```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)  # ... means required
    price: float = Field(..., gt=0, le=1_000_000)         # greater than 0, <= 1M
    quantity: int = Field(default=0, ge=0)                # >= 0
    discount: float = Field(default=0.0, ge=0, le=1.0)   # 0% to 100%
```

### 4. Custom Validators

```python
from pydantic import field_validator, model_validator

class Order(BaseModel):
    items: list[str]
    total: float

    @field_validator("items")
    @classmethod
    def items_not_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Order must have at least one item")
        return v

    @model_validator(mode="after")
    def check_total(self):
        if self.total <= 0 and len(self.items) > 0:
            raise ValueError("Total must be positive if items exist")
        return self
```

### 5. Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    country: str = "Pakistan"

class User(BaseModel):
    name: str
    address: Address  # nested model - FastAPI validates recursively
```

JSON body:
```json
{
  "name": "Ahmad",
  "address": {
    "street": "123 Main St",
    "city": "Lahore"
  }
}
```

### 6. Model Methods

| Method | Purpose |
|---|---|
| `model.model_dump()` | Convert to dict (like `JSON.parse(JSON.stringify(obj))` in Node) |
| `model.model_dump(exclude_unset=True)` | Only fields that were explicitly set (for PATCH) |
| `model.model_dump_json()` | Convert to JSON string |
| `Model.model_validate(dict)` | Create model from dict |
| `Model.model_json_schema()` | Get JSON Schema (used by Swagger) |

### 7. Common Pydantic Types

```python
from pydantic import EmailStr, HttpUrl
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"

class User(BaseModel):
    email: EmailStr         # validates email format (needs `pip install pydantic[email]`)
    website: HttpUrl        # validates URL format
    role: Role              # one of the enum values
    created_at: datetime    # parses ISO 8601 strings automatically
```

### 8. Config & JSON Schema Customization

```python
class User(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Ahmad",
                    "email": "ahmad@example.com",
                    "age": 25,
                }
            ]
        }
    }

    name: str
    email: str
    age: int
```

## Why Validation Matters

In Express, if you forget to validate, bad data silently enters your system. FastAPI **refuses invalid data at the door** — before your function ever runs. This is a massive improvement over manual `if (!req.body.name)` checks.
