# Chapter 08: Testing FastAPI Applications

## Overview

Testing in FastAPI uses **pytest** + FastAPI's built-in **TestClient** (which wraps `httpx`).

### Node.js → Python Testing Mapping

| Node.js | Python (FastAPI) |
|---|---|
| Jest / Mocha | pytest |
| supertest | TestClient (httpx) |
| `describe` / `it` | `class Test...` / `def test_...` |
| `expect(res.status).toBe(200)` | `assert response.status_code == 200` |
| `beforeAll` / `afterAll` | `@pytest.fixture(scope="module")` |
| `beforeEach` | `@pytest.fixture` (default: per-test) |
| Mock / Jest.fn() | `unittest.mock.patch` / `pytest-mock` |

## Core Concepts

### 1. TestClient

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello"
```

### 2. Fixtures (Setup/Teardown)

```python
import pytest

@pytest.fixture
def client():
    """Fresh test client for each test."""
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Get auth token for protected routes."""
    client = TestClient(app)
    response = client.post("/auth/token", data={"username": "test", "password": "test"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

### 3. Dependency Overrides

FastAPI's killer testing feature — swap real dependencies with fakes:

```python
def override_get_db():
    """Use test database instead of real one."""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
```

### 4. Async Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.anyio
async def test_async_route():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/async-endpoint")
    assert response.status_code == 200
```

## Test Organization

```
tests/
├── conftest.py          # shared fixtures
├── test_users.py        # user endpoint tests
├── test_auth.py         # auth tests
└── test_posts.py        # post tests
```

## Running Tests

```bash
pip install pytest httpx
pytest                     # run all tests
pytest -v                  # verbose output
pytest tests/test_users.py # specific file
pytest -k "test_create"    # tests matching pattern
pytest --cov=app           # with coverage (pip install pytest-cov)
```
