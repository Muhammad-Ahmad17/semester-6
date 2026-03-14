# Chapter 04: Authentication & Authorization

## Overview

Authentication (AuthN) = **Who are you?**
Authorization (AuthZ) = **What can you do?**

### Node.js → FastAPI Mapping

| Express.js | FastAPI |
|---|---|
| `passport.js` | FastAPI's built-in `OAuth2PasswordBearer` |
| `jsonwebtoken` (npm) | `python-jose` or `PyJWT` |
| `bcrypt` (npm) | `passlib` with bcrypt |
| `express-session` | Not needed (JWT is stateless) |
| Auth middleware | `Depends()` with security schemes |

## JWT (JSON Web Token) — How It Works

```
1. Client sends username + password → POST /token
2. Server verifies credentials, creates JWT, sends it back
3. Client stores JWT (localStorage, cookie)
4. Client sends JWT in Authorization header for every request
5. Server validates JWT and extracts user info

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### JWT Structure
```
header.payload.signature

Header:  {"alg": "HS256", "typ": "JWT"}
Payload: {"sub": "user@email.com", "exp": 1234567890, "role": "admin"}
Signature: HMAC-SHA256(header + payload, SECRET_KEY)
```

## OAuth2 Password Flow

FastAPI has **built-in OAuth2 support** that auto-generates a login form in Swagger UI:

```python
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# This tells FastAPI: "look for a Bearer token in the Authorization header"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # form_data.username, form_data.password
    ...

@app.get("/me")
def get_me(token: str = Depends(oauth2_scheme)):
    # token is extracted from "Authorization: Bearer <token>"
    ...
```

## Password Hashing

**NEVER store plain-text passwords.** Use bcrypt:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed = pwd_context.hash("mypassword")        # hash
verified = pwd_context.verify("mypassword", hashed)  # verify
```

## Role-Based Access Control (RBAC)

```python
def require_role(*roles):
    def checker(user = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(403, "Insufficient permissions")
        return user
    return checker

@app.get("/admin", dependencies=[Depends(require_role("admin"))])
def admin_only():
    ...
```

## Dependencies for this Chapter

```bash
pip install python-jose[cryptography] passlib[bcrypt]
```
