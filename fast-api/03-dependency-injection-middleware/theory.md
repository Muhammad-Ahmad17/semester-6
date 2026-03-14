# Chapter 03: Dependency Injection & Middleware

## Dependency Injection (DI)

### What is DI?
DI is a design pattern where a function **receives its dependencies from the outside** instead of creating them itself.

**Node.js analogy**: In Express, you use **middleware** (`app.use(authMiddleware)`) to inject things into `req` (like `req.user`). In FastAPI, you use `Depends()` — but it's more powerful and flexible.

### Why DI Matters in FastAPI
1. **Reusability**: Write once, use in many routes
2. **Testability**: Easily swap dependencies in tests
3. **Composability**: Dependencies can depend on other dependencies
4. **Auto-documentation**: FastAPI documents dependency parameters in Swagger

### How it Works

```
Request → Middleware (global) → Route Dependencies (Depends) → Your Function
```

```python
from fastapi import Depends

# 1. Define a dependency (it's just a function!)
def get_db():
    db = connect_to_database()
    try:
        yield db          # like Express next() — hands control to route
    finally:
        db.close()        # cleanup after route completes

# 2. Use it in a route
@app.get("/users")
def list_users(db = Depends(get_db)):   # FastAPI injects the DB connection
    return db.query(User).all()
```

### Dependency Chain

```python
def get_db():
    ...

def get_current_user(db = Depends(get_db)):    # depends on get_db
    ...

def get_admin_user(user = Depends(get_current_user)):  # depends on get_current_user
    if user.role != "admin":
        raise HTTPException(403)
    return user

@app.get("/admin/dashboard")
def admin_dashboard(admin = Depends(get_admin_user)):
    # FastAPI resolves the full chain: get_db → get_current_user → get_admin_user
    ...
```

### Types of Dependencies

| Type | How | When to Use |
|---|---|---|
| Function | `Depends(my_func)` | Most common - DB sessions, auth, pagination |
| Class | `Depends(MyClass)` | When you need state or complex logic |
| Generator (yield) | `yield` inside function | When you need cleanup (DB, files) |

## Middleware

### What is Middleware?
Code that runs **before and after every request**. Identical concept to Express middleware.

```
Express:  app.use((req, res, next) => { ... next() ... })
FastAPI:  @app.middleware("http") async def my_middleware(request, call_next): ...
```

### Middleware vs Dependencies

| Feature | Middleware | Dependencies |
|---|---|---|
| Scope | Every request | Only routes that use `Depends()` |
| Access to response | Yes (can modify) | No (only request data) |
| Use case | Logging, CORS, timing | Auth, DB, pagination |
| Order | Top-to-bottom registration | Per-route declaration |

### Common Middleware Patterns

1. **CORS** — Allow cross-origin requests (like `cors` npm package)
2. **Request timing** — Log how long each request takes
3. **Request ID** — Add unique ID to each request for tracing
4. **Error handling** — Global exception catching

## Event Handlers (Lifespan)

In Express you might do setup in `app.listen()` callback. In FastAPI, use **lifespan events**:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before the app starts accepting requests
    print("Connecting to DB...")
    yield
    # SHUTDOWN: runs when the app is stopping
    print("Closing DB connection...")

app = FastAPI(lifespan=lifespan)
```
