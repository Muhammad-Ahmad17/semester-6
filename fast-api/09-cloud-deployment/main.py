"""
Chapter 09: Cloud-Ready FastAPI Application
=============================================
This is a production-ready app structure demonstrating:
- Environment-based configuration
- Health checks
- Structured logging
- Graceful shutdown
- Docker-ready setup

pip install fastapi uvicorn pydantic-settings
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from pydantic import Field
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import logging
import time
import os


# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION (pydantic-settings)
# ═══════════════════════════════════════════════════════════════════

class Settings(BaseSettings):
    """
    All config from environment variables.
    In Node.js: process.env.DATABASE_URL
    In FastAPI: settings.database_url (auto-loaded from env)
    """
    app_name: str = "FastAPI Cloud Demo"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False)
    environment: str = Field(default="development")  # development, staging, production

    # Database
    database_url: str = Field(default="sqlite:///./app.db")

    # Security
    secret_key: str = Field(default="change-me-in-production")
    allowed_origins: str = Field(default="http://localhost:3000,http://localhost:5173")

    # External services
    redis_url: str = Field(default="redis://localhost:6379")
    sentry_dsn: str = Field(default="")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()


# ═══════════════════════════════════════════════════════════════════
# LOGGING (Structured JSON logs for cloud)
# ═══════════════════════════════════════════════════════════════════

logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app")


# ═══════════════════════════════════════════════════════════════════
# LIFESPAN (Startup/Shutdown)
# ═══════════════════════════════════════════════════════════════════

startup_time: float = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    global startup_time
    startup_time = time.time()

    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Database: {settings.database_url[:20]}...")

    # STARTUP: Initialize connections
    # In production: connect to DB, Redis, etc.
    yield

    # SHUTDOWN: Cleanup
    logger.info("Shutting down gracefully...")
    # In production: close DB pool, flush caches, etc.


# ═══════════════════════════════════════════════════════════════════
# APP CREATION
# ═══════════════════════════════════════════════════════════════════

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs" if settings.debug else None,  # Disable Swagger in production
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# ─── CORS ────────────────────────────────────────────────────────
origins = [o.strip() for o in settings.allowed_origins.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request Logging Middleware ──────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    logger.info(
        f"{request.method} {request.url.path} → {response.status_code} ({duration:.3f}s)"
    )
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response


# ─── Global Exception Handler ───────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ═══════════════════════════════════════════════════════════════════
# HEALTH CHECK ENDPOINTS (Required for cloud platforms)
# ═══════════════════════════════════════════════════════════════════

@app.get("/health")
def health_check():
    """
    Basic health check — cloud platforms hit this to know if the app is alive.
    - AWS ELB: health check path
    - Kubernetes: liveness probe
    - Google Cloud Run: startup check
    """
    return {"status": "healthy"}


@app.get("/health/detailed")
def detailed_health():
    """Detailed health check with system info."""
    uptime_seconds = time.time() - startup_time if startup_time else 0

    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "uptime_seconds": round(uptime_seconds, 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": {
            "database": "connected",  # In production: actually ping DB
            "redis": "connected",     # In production: actually ping Redis
        },
    }


@app.get("/health/ready")
def readiness_check():
    """
    Readiness check — are all dependencies available?
    Kubernetes uses this to decide if traffic should be routed here.
    """
    # In production, check DB, Redis, external APIs
    checks = {
        "database": True,
        "redis": True,
    }
    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
    }


# ═══════════════════════════════════════════════════════════════════
# APPLICATION ROUTES
# ═══════════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "health": "/health",
    }


@app.get("/config")
def show_config():
    """Show non-sensitive configuration (useful for debugging)."""
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "debug": settings.debug,
        "allowed_origins": origins,
        # NEVER expose: secret_key, database passwords, API keys
    }
