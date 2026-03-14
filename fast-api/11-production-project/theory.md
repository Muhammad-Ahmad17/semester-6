# Chapter 11: Production-Grade Project Structure

## Overview

This chapter brings everything together into a **real-world project structure** — a full-featured REST API with clean architecture.

## Project: Task Management API (like Trello/Todoist backend)

### Features
- User registration & JWT authentication
- Project management (CRUD)
- Task management with assignments
- Role-based access control
- Database with relationships (SQLAlchemy)
- Background email notifications
- Health checks & structured config

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # App factory + lifespan + routers
│   ├── config.py             # Settings (env vars)
│   ├── database.py           # DB engine, session, Base
│   ├── models/               # SQLAlchemy models (DB tables)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── schemas/              # Pydantic models (API shapes)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── project.py
│   │   └── task.py
│   ├── routes/               # API route handlers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── projects.py
│   │   └── tasks.py
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── email.py
│   └── dependencies.py       # Shared dependencies (get_db, get_current_user)
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_projects.py
├── .env
├── .env.example
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Architecture Pattern: Service Layer

```
Route (Controller)  →  Service (Business Logic)  →  Repository (DB Access)
     ↓                        ↓                           ↓
  Validate input       Apply rules              Query database
  Call service         Check permissions         Return data
  Return response      Transform data
```

### Why This Structure?

| Concern | File | Responsibility |
|---|---|---|
| **HTTP handling** | `routes/` | Parse request, call service, return response |
| **Business logic** | `services/` | Validate rules, orchestrate operations |
| **Data access** | `models/` | Define tables, relationships |
| **API contracts** | `schemas/` | Define request/response shapes |
| **Wiring** | `dependencies.py` | DI for DB sessions, auth, etc. |
| **Config** | `config.py` | Environment variables |

### Express Project Comparison

```
Express                     FastAPI
──────                      ───────
src/controllers/     →      app/routes/
src/models/          →      app/models/
src/middleware/       →      app/dependencies.py
src/services/        →      app/services/
src/validators/      →      app/schemas/
src/config.js        →      app/config.py
src/app.js           →      app/main.py
```

## Key Principles

1. **Separation of Concerns**: Routes don't touch the DB directly
2. **Dependency Injection**: All dependencies are injectable and testable
3. **Configuration from Environment**: No hardcoded secrets
4. **Type Safety**: Pydantic validates everything at the boundary
5. **Testability**: Override any dependency for testing
