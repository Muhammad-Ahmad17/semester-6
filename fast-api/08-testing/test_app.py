"""
Chapter 08: Test Suite
=======================
pip install pytest httpx
Run: pytest test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app, items_db, get_current_user


# ═══════════════════════════════════════════════════════════════════
# FIXTURES (setup/teardown — like beforeEach in Jest)
# ═══════════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Provide a fresh TestClient for each test."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory DB before each test (like beforeEach)."""
    items_db.clear()
    yield
    items_db.clear()


@pytest.fixture
def sample_item(client):
    """Create a sample item and return its data."""
    response = client.post("/items", json={
        "name": "Test Widget",
        "price": 29.99,
        "category": "electronics",
    })
    return response.json()


# ═══════════════════════════════════════════════════════════════════
# TEST: ROOT ENDPOINT
# ═══════════════════════════════════════════════════════════════════

def test_root(client):
    """GET / should return welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Testing chapter app"


# ═══════════════════════════════════════════════════════════════════
# TEST: CREATE ITEM
# ═══════════════════════════════════════════════════════════════════

def test_create_item(client):
    """POST /items with valid data should return 201."""
    response = client.post("/items", json={
        "name": "Laptop",
        "price": 999.99,
        "category": "electronics",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data


def test_create_item_invalid_price(client):
    """POST /items with price <= 0 should return 422."""
    response = client.post("/items", json={
        "name": "Bad Item",
        "price": -10.0,
    })
    assert response.status_code == 422  # Validation error


def test_create_item_missing_name(client):
    """POST /items without required 'name' should return 422."""
    response = client.post("/items", json={"price": 10.0})
    assert response.status_code == 422


def test_create_item_name_too_long(client):
    """POST /items with name > 100 chars should return 422."""
    response = client.post("/items", json={
        "name": "x" * 101,
        "price": 10.0,
    })
    assert response.status_code == 422


# ═══════════════════════════════════════════════════════════════════
# TEST: LIST ITEMS
# ═══════════════════════════════════════════════════════════════════

def test_list_items_empty(client):
    """GET /items with empty DB should return empty list."""
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_with_data(client, sample_item):
    """GET /items should include the created item."""
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    assert len(items) == 1
    assert items[0]["name"] == "Test Widget"


def test_list_items_filter_by_category(client):
    """GET /items?category=X should filter results."""
    client.post("/items", json={"name": "A", "price": 10, "category": "food"})
    client.post("/items", json={"name": "B", "price": 20, "category": "electronics"})
    client.post("/items", json={"name": "C", "price": 30, "category": "food"})

    response = client.get("/items?category=food")
    assert len(response.json()) == 2

    response = client.get("/items?category=electronics")
    assert len(response.json()) == 1


# ═══════════════════════════════════════════════════════════════════
# TEST: GET SINGLE ITEM
# ═══════════════════════════════════════════════════════════════════

def test_get_item(client, sample_item):
    """GET /items/{id} should return the item."""
    item_id = sample_item["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Widget"


def test_get_item_not_found(client):
    """GET /items/{id} with invalid ID should return 404."""
    response = client.get("/items/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


# ═══════════════════════════════════════════════════════════════════
# TEST: UPDATE ITEM
# ═══════════════════════════════════════════════════════════════════

def test_update_item(client, sample_item):
    """PUT /items/{id} should update fields."""
    item_id = sample_item["id"]
    response = client.put(f"/items/{item_id}", json={"name": "Updated Widget"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Widget"
    assert response.json()["price"] == 29.99  # unchanged


def test_update_item_not_found(client):
    """PUT /items/{id} with invalid ID should return 404."""
    response = client.put("/items/9999", json={"name": "Nope"})
    assert response.status_code == 404


# ═══════════════════════════════════════════════════════════════════
# TEST: DELETE ITEM
# ═══════════════════════════════════════════════════════════════════

def test_delete_item(client, sample_item):
    """DELETE /items/{id} should remove the item."""
    item_id = sample_item["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204

    # Verify it's gone
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404


def test_delete_item_not_found(client):
    """DELETE /items/{id} with invalid ID should return 404."""
    response = client.delete("/items/9999")
    assert response.status_code == 404


# ═══════════════════════════════════════════════════════════════════
# TEST: PROTECTED ROUTE
# ═══════════════════════════════════════════════════════════════════

def test_protected_with_valid_token(client):
    """Protected route should work with valid token."""
    response = client.get("/protected", headers={"x-token": "valid-token"})
    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_protected_with_invalid_token(client):
    """Protected route should return 401 with invalid token."""
    response = client.get("/protected", headers={"x-token": "bad-token"})
    assert response.status_code == 401


def test_protected_without_token(client):
    """Protected route should return 401 without token."""
    response = client.get("/protected")
    assert response.status_code == 401


# ═══════════════════════════════════════════════════════════════════
# TEST: DEPENDENCY OVERRIDE (Mock dependencies)
# ═══════════════════════════════════════════════════════════════════

def test_with_dependency_override(client):
    """
    Override a dependency for testing — FastAPI's killer feature.
    Like Jest.fn() or sinon.stub() but at the framework level.
    """
    # Create a fake user dependency
    def override_get_current_user():
        return {"id": 99, "name": "Mock User", "role": "tester"}

    # Override the real dependency
    app.dependency_overrides[get_current_user] = override_get_current_user

    response = client.get("/protected")
    assert response.status_code == 200
    assert response.json()["message"] == "Hello Mock User"
    assert response.json()["role"] == "tester"

    # Clean up
    app.dependency_overrides.clear()


# ═══════════════════════════════════════════════════════════════════
# TEST: FULL CRUD FLOW (Integration Test)
# ═══════════════════════════════════════════════════════════════════

def test_full_crud_flow(client):
    """End-to-end test: create → read → update → delete."""
    # CREATE
    create_resp = client.post("/items", json={
        "name": "Flow Item",
        "price": 50.0,
        "category": "test",
    })
    assert create_resp.status_code == 201
    item_id = create_resp.json()["id"]

    # READ
    get_resp = client.get(f"/items/{item_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["name"] == "Flow Item"

    # UPDATE
    update_resp = client.put(f"/items/{item_id}", json={"price": 75.0})
    assert update_resp.status_code == 200
    assert update_resp.json()["price"] == 75.0

    # LIST
    list_resp = client.get("/items")
    assert len(list_resp.json()) == 1

    # DELETE
    del_resp = client.delete(f"/items/{item_id}")
    assert del_resp.status_code == 204

    # VERIFY DELETED
    assert client.get(f"/items/{item_id}").status_code == 404
    assert len(client.get("/items").json()) == 0
