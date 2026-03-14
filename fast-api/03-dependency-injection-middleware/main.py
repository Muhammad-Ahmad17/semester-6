"""
Chapter 03: Dependency Injection & Middleware
==============================================
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, Depends, HTTPException, Request, Response, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import Optional, Annotated
import time
import uuid


# ─── 1. Lifespan Events (Startup/Shutdown) ───────────────────────
# Express equivalent: app.listen(3000, () => console.log("Server ready"))

fake_db_connection = {"connected": False}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    print("🔌 Connecting to database...")
    fake_db_connection["connected"] = True
    yield  # App runs here
    # SHUTDOWN
    print("🔌 Closing database connection...")
    fake_db_connection["connected"] = False


app = FastAPI(title="Chapter 03 - DI & Middleware", lifespan=lifespan)


# ─── 2. CORS Middleware ──────────────────────────────────────────
# Express equivalent: app.use(cors({ origin: [...], methods: [...] }))
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── 3. Custom Middleware: Request Timing ────────────────────────
# Express: app.use((req, res, next) => { const start = Date.now(); next(); ... })
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    """Adds X-Process-Time header to every response."""
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}s"
    return response


# ─── 4. Custom Middleware: Request ID ────────────────────────────
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Adds a unique request ID for tracing/debugging."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id  # attach to request state
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# ─── 5. Simple Function Dependencies ────────────────────────────

# Dependency 1: Common pagination parameters
def pagination_params(
    skip: int = Query(0, ge=0, description="Items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return"),
) -> dict:
    """Reusable pagination — no need to repeat these params in every route."""
    return {"skip": skip, "limit": limit}


# Dependency 2: Simple API key check
def verify_api_key(
    x_api_key: Optional[str] = Header(None, description="API Key in header"),
) -> str:
    """
    Express equivalent:
    function verifyApiKey(req, res, next) {
        if (req.headers['x-api-key'] !== 'secret123') return res.status(403).json(...)
        next()
    }
    """
    if x_api_key != "secret123":
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return x_api_key


# ─── 6. Generator Dependency (with cleanup) ─────────────────────
def get_db_session():
    """
    A generator dependency that simulates DB session lifecycle.
    The 'yield' is like Express middleware's next() — it hands control to the route.
    The 'finally' block runs after the route completes (cleanup).
    """
    print("  → Opening DB session")
    session = {"active": True, "queries": []}
    try:
        yield session  # route receives this
    finally:
        print(f"  ← Closing DB session (executed {len(session['queries'])} queries)")
        session["active"] = False


# ─── 7. Class-Based Dependency ───────────────────────────────────
class RateLimiter:
    """
    A per-route rate limiter using a class dependency.
    Class dependencies are useful when you need configurable, stateful logic.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict[str, list[float]] = {}

    def __call__(self, request: Request) -> str:
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Remove old requests outside the window
        self.requests[client_ip] = [
            t for t in self.requests[client_ip]
            if now - t < self.window_seconds
        ]

        if len(self.requests[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Max {self.max_requests} requests per {self.window_seconds}s",
            )

        self.requests[client_ip].append(now)
        return client_ip


# Create rate limiter instances with different configs
default_limiter = RateLimiter(max_requests=10, window_seconds=60)
strict_limiter = RateLimiter(max_requests=3, window_seconds=60)


# ─── 8. Dependency Chain ─────────────────────────────────────────
def get_current_user(
    x_token: str = Header(..., description="User auth token"),
    db=Depends(get_db_session),
) -> dict:
    """Resolves: get_db_session → get_current_user"""
    db["queries"].append("SELECT * FROM users WHERE token = ?")

    fake_users = {
        "token-admin": {"id": 1, "name": "Admin", "role": "admin"},
        "token-user": {"id": 2, "name": "Ahmad", "role": "user"},
    }
    user = fake_users.get(x_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user


def require_admin(user: dict = Depends(get_current_user)) -> dict:
    """Resolves: get_db_session → get_current_user → require_admin"""
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# ─── Type Aliases with Annotated (Modern Pattern) ────────────────
# Instead of repeating Depends() everywhere, use Annotated
PaginationDep = Annotated[dict, Depends(pagination_params)]
CurrentUser = Annotated[dict, Depends(get_current_user)]
AdminUser = Annotated[dict, Depends(require_admin)]
DBSession = Annotated[dict, Depends(get_db_session)]


# ═══════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════

fake_items = [{"id": i, "name": f"Item {i}", "price": i * 10.0} for i in range(1, 51)]


@app.get("/")
def root():
    return {
        "message": "Chapter 03 - DI & Middleware",
        "db_connected": fake_db_connection["connected"],
        "docs": "/docs",
    }


# ─── Using pagination dependency ─────────────────────────────────
@app.get("/items")
def list_items(pagination: PaginationDep):
    """Uses reusable pagination dependency."""
    s, l = pagination["skip"], pagination["limit"]
    return {"items": fake_items[s : s + l], "total": len(fake_items)}


# ─── Using API key dependency ────────────────────────────────────
@app.get("/protected")
def protected_route(api_key: str = Depends(verify_api_key)):
    """Send header: X-Api-Key: secret123"""
    return {"message": "You have access!", "api_key_used": api_key}


# ─── Using DB session (generator) dependency ─────────────────────
@app.get("/db-demo")
def db_demo(db: DBSession):
    """Watch the terminal — you'll see session open/close logs."""
    db["queries"].append("SELECT * FROM items")
    db["queries"].append("SELECT COUNT(*) FROM items")
    return {"session_active": db["active"], "queries_executed": db["queries"]}


# ─── Using rate limiter (class) dependency ────────────────────────
@app.get("/rate-limited")
def rate_limited_route(client_ip: str = Depends(default_limiter)):
    """Try hitting this more than 10 times in 60 seconds."""
    return {"message": "Request accepted", "your_ip": client_ip}


@app.get("/strict-rate-limited")
def strict_rate_limited_route(client_ip: str = Depends(strict_limiter)):
    """Only 3 requests per 60 seconds!"""
    return {"message": "Request accepted (strict)", "your_ip": client_ip}


# ─── Using dependency chain ──────────────────────────────────────
@app.get("/me")
def get_me(user: CurrentUser):
    """Send header: X-Token: token-user (or token-admin)"""
    return {"user": user}


@app.get("/admin/dashboard")
def admin_dashboard(admin: AdminUser):
    """
    Send header: X-Token: token-admin
    The dependency chain resolves: DB → User → Admin check
    """
    return {"message": f"Welcome, {admin['name']}!", "role": admin["role"]}


# ─── Route-level dependencies (applied to entire route) ──────────
@app.get(
    "/vip",
    dependencies=[Depends(verify_api_key), Depends(default_limiter)],
)
def vip_route():
    """
    Route-level dependencies: run checks without injecting values.
    Both API key AND rate limit must pass.
    """
    return {"message": "VIP access granted"}


# ─── Request state from middleware ────────────────────────────────
@app.get("/request-info")
async def request_info(request: Request):
    """Demonstrates accessing middleware-injected data."""
    return {
        "request_id": getattr(request.state, "request_id", None),
        "method": request.method,
        "url": str(request.url),
        "client_host": request.client.host if request.client else None,
        "headers": dict(request.headers),
    }
