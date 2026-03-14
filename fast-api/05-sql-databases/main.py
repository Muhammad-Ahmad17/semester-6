"""
Chapter 05: SQL Database Integration
======================================
pip install sqlalchemy
Run: uvicorn main:app --reload --port 8000

This uses SQLite for zero-config setup. Change DATABASE_URL for PostgreSQL.
"""

from fastapi import FastAPI, Depends, HTTPException, status, Query
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session, relationship
from typing import Optional, Annotated
from datetime import datetime, timezone
from contextlib import asynccontextmanager


# ═══════════════════════════════════════════════════════════════════
# DATABASE SETUP
# ═══════════════════════════════════════════════════════════════════

# SQLite for development (no server needed)
# For PostgreSQL: "postgresql://user:password@localhost:5432/mydb"
DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite-specific
    echo=True,  # Logs all SQL queries (disable in production)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ─── Base Model ──────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


# ═══════════════════════════════════════════════════════════════════
# SQLALCHEMY MODELS (Database Tables)
# ═══════════════════════════════════════════════════════════════════
# This is like defining Sequelize models or Prisma schema

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship: User has many Posts
    posts = relationship("DBPost", back_populates="author", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class DBPost(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Foreign Key: belongs to User
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("DBUser", back_populates="posts")

    # Relationship: Post has many Comments
    comments = relationship("DBComment", back_populates="post", cascade="all, delete-orphan")


class DBComment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    body = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    commenter_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    post = relationship("DBPost", back_populates="comments")
    commenter = relationship("DBUser")


# ═══════════════════════════════════════════════════════════════════
# PYDANTIC SCHEMAS (API Request/Response)
# ═══════════════════════════════════════════════════════════════════
# Separate from SQLAlchemy models! Pydantic = API shape, SQLAlchemy = DB shape.

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    post_count: int = 0

    model_config = {"from_attributes": True}  # Allows creating from SQLAlchemy objects


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    published: bool = False


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    published: bool
    created_at: datetime
    updated_at: datetime
    author_id: int
    author_username: str = ""
    comment_count: int = 0

    model_config = {"from_attributes": True}


class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    id: int
    body: str
    created_at: datetime
    post_id: int
    commenter_id: int

    model_config = {"from_attributes": True}


# ═══════════════════════════════════════════════════════════════════
# APP SETUP
# ═══════════════════════════════════════════════════════════════════

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (in production, use Alembic migrations instead)
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    yield
    print("Shutting down...")


app = FastAPI(title="Chapter 05 - SQL Databases", lifespan=lifespan)


# ─── Database Dependency ─────────────────────────────────────────
# Express equivalent: a middleware that attaches db to req
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DB = Annotated[Session, Depends(get_db)]


# ═══════════════════════════════════════════════════════════════════
# USER CRUD ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: DB):
    """Create a new user."""
    # Check duplicates
    existing = db.query(DBUser).filter(
        (DBUser.email == user.email) | (DBUser.username == user.username)
    ).first()
    if existing:
        raise HTTPException(409, "Username or email already exists")

    db_user = DBUser(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # reload from DB to get auto-generated fields
    return _user_to_response(db_user)


@app.get("/users", response_model=list[UserResponse])
def list_users(
    db: DB,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    active_only: bool = Query(False),
):
    """List users with pagination and optional filter."""
    query = db.query(DBUser)
    if active_only:
        query = query.filter(DBUser.is_active == True)
    users = query.offset(skip).limit(limit).all()
    return [_user_to_response(u) for u in users]


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: DB):
    """Get a specific user."""
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return _user_to_response(user)


@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update: UserUpdate, db: DB):
    """Update a user (partial update)."""
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return _user_to_response(user)


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: DB):
    """Delete a user and all their posts (cascade)."""
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    db.delete(user)
    db.commit()


# ═══════════════════════════════════════════════════════════════════
# POST CRUD ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/users/{user_id}/posts", response_model=PostResponse, status_code=201)
def create_post(user_id: int, post: PostCreate, db: DB):
    """Create a post for a user."""
    user = db.query(DBUser).filter(DBUser.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    db_post = DBPost(**post.model_dump(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return _post_to_response(db_post)


@app.get("/posts", response_model=list[PostResponse])
def list_posts(
    db: DB,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = Query(False),
    search: Optional[str] = Query(None, min_length=1),
):
    """List posts with filters and search."""
    query = db.query(DBPost)
    if published_only:
        query = query.filter(DBPost.published == True)
    if search:
        query = query.filter(DBPost.title.ilike(f"%{search}%"))
    query = query.order_by(DBPost.created_at.desc())
    posts = query.offset(skip).limit(limit).all()
    return [_post_to_response(p) for p in posts]


@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: DB):
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    return _post_to_response(post)


@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, update: PostUpdate, db: DB):
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(post, key, value)

    db.commit()
    db.refresh(post)
    return _post_to_response(post)


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int, db: DB):
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    db.delete(post)
    db.commit()


# ═══════════════════════════════════════════════════════════════════
# COMMENT ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(post_id: int, comment: CommentCreate, commenter_id: int, db: DB):
    """Add a comment to a post."""
    post = db.query(DBPost).filter(DBPost.id == post_id).first()
    if not post:
        raise HTTPException(404, "Post not found")
    commenter = db.query(DBUser).filter(DBUser.id == commenter_id).first()
    if not commenter:
        raise HTTPException(404, "Commenter not found")

    db_comment = DBComment(body=comment.body, post_id=post_id, commenter_id=commenter_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
def list_comments(post_id: int, db: DB):
    return db.query(DBComment).filter(DBComment.post_id == post_id).all()


# ═══════════════════════════════════════════════════════════════════
# AGGREGATE QUERIES (Advanced SQLAlchemy)
# ═══════════════════════════════════════════════════════════════════

@app.get("/stats")
def get_stats(db: DB):
    """Database aggregate queries — like Sequelize's findAndCountAll."""
    total_users = db.query(func.count(DBUser.id)).scalar()
    total_posts = db.query(func.count(DBPost.id)).scalar()
    total_comments = db.query(func.count(DBComment.id)).scalar()
    published_posts = db.query(func.count(DBPost.id)).filter(DBPost.published == True).scalar()

    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": total_posts - published_posts,
        "total_comments": total_comments,
    }


# ─── Helper Functions ────────────────────────────────────────────
def _user_to_response(user: DBUser) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "post_count": len(user.posts),
    }


def _post_to_response(post: DBPost) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "published": post.published,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "author_id": post.author_id,
        "author_username": post.author.username if post.author else "",
        "comment_count": len(post.comments),
    }
