# Chapter 05: SQL Database Integration (PostgreSQL + SQLAlchemy)

## Overview

This chapter covers connecting FastAPI to a **PostgreSQL** database using **SQLAlchemy** (the most popular Python ORM).

### Node.js → Python ORM Mapping

| Node.js | Python (FastAPI) |
|---|---|
| Sequelize | SQLAlchemy |
| Prisma | SQLAlchemy + Alembic |
| TypeORM | SQLAlchemy |
| Knex.js (query builder) | SQLAlchemy Core |
| Mongoose (MongoDB) | See Chapter 06 |

## SQLAlchemy Architecture

```
Your Code (Models + Queries)
        ↓
SQLAlchemy ORM (object-relational mapping)
        ↓
SQLAlchemy Core (SQL expression language)
        ↓
Database Driver (psycopg2 / asyncpg)
        ↓
PostgreSQL Database
```

### Two Styles

1. **SQLAlchemy ORM** (recommended for FastAPI) — define Python classes that map to tables
2. **SQLAlchemy Core** — write SQL-like expressions in Python (more control, less convenience)

## Key Concepts

### 1. Engine & Session
```python
# Engine = connection pool (like Sequelize's connection)
engine = create_engine("postgresql://user:password@localhost/dbname")

# Session = a "conversation" with the DB (like a transaction)
SessionLocal = sessionmaker(bind=engine)
```

### 2. Declarative Models
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
```

### 3. Relationships
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
```

### 4. Session as Dependency
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### 5. Alembic — Database Migrations
```bash
# Like Sequelize migrations or Prisma Migrate
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "create users table"
alembic upgrade head
```

## Async vs Sync

- **Sync**: `create_engine` + `Session` (simpler, good for most apps)
- **Async**: `create_async_engine` + `AsyncSession` (for high-concurrency apps)

This chapter uses **sync** SQLAlchemy for clarity. The async version is shown in the advanced section.

## Dependencies

```bash
pip install sqlalchemy psycopg2-binary alembic
# For async: pip install sqlalchemy[asyncio] asyncpg
```

## Note on SQLite (for development)

The code in this chapter uses **SQLite** by default so you can run it without a PostgreSQL server. To switch to PostgreSQL, just change the `DATABASE_URL`:

```python
# SQLite (development)
DATABASE_URL = "sqlite:///./app.db"

# PostgreSQL (production)
DATABASE_URL = "postgresql://user:password@localhost:5432/mydb"
```
