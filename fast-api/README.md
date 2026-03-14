# FastAPI Learning Roadmap: Node.js Developer Edition

## From Express to FastAPI — Complete Guide with Code

A structured, chapter-wise learning path to master FastAPI, covering fundamentals through production deployment and AI integration. Each chapter has a **theory.md** (concepts) and **main.py** (working code).

---

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate    # Linux/Mac
# venv\Scripts\activate     # Windows

# 2. Install core dependencies
pip install fastapi uvicorn[standard] pydantic[email]

# 3. Run any chapter
cd 01-fundamentals
uvicorn main:app --reload --port 8000

# 4. Open Swagger docs
# http://localhost:8000/docs
```

---

## Roadmap

### Phase 1: Core Fundamentals

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 01 | **[FastAPI Fundamentals](01-fundamentals/)** | Routes, path/query params, request body, status codes, auto docs | `theory.md` `main.py` |
| 02 | **[Pydantic & Validation](02-pydantic-validation/)** | BaseModel, Field, validators, nested models, enums, serialization | `theory.md` `main.py` |
| 03 | **[Dependency Injection & Middleware](03-dependency-injection-middleware/)** | Depends(), CORS, custom middleware, class dependencies, lifespan | `theory.md` `main.py` |
| 04 | **[Authentication](04-authentication/)** | OAuth2, JWT, bcrypt, RBAC, refresh tokens, protected routes | `theory.md` `main.py` |

### Phase 2: Databases

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 05 | **[SQL Databases](05-sql-databases/)** | SQLAlchemy ORM, PostgreSQL/SQLite, relationships, CRUD, migrations | `theory.md` `main.py` |
| 06 | **[NoSQL Databases](06-nosql-databases/)** | MongoDB, Motor (async), Beanie ODM, aggregation pipelines | `theory.md` `main.py` |

### Phase 3: Advanced Patterns

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 07 | **[Advanced Patterns](07-advanced-patterns/)** | Background tasks, WebSockets, file upload/download, SSE streaming, APIRouter | `theory.md` `main.py` |
| 08 | **[Testing](08-testing/)** | pytest, TestClient, fixtures, dependency overrides, integration tests | `theory.md` `main.py` `test_app.py` |

### Phase 4: Production & Cloud

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 09 | **[Cloud Deployment](09-cloud-deployment/)** | Docker, Docker Compose, env config, health checks, AWS/GCP/CI-CD | `theory.md` `main.py` `Dockerfile` `docker-compose.yml` |

### Phase 5: AI/ML Integration

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 10 | **[AI Integration](10-ai-integration/)** | OpenAI API, streaming chat, embeddings, RAG, LangChain, summarization | `theory.md` `main.py` |

### Phase 6: Capstone

| # | Chapter | Topics | Key Files |
|---|---------|--------|-----------|
| 11 | **[Production Project](11-production-project/)** | Full project structure, service layer, modular routes, real-world patterns | `theory.md` `app/` |

---

## Chapter Dependencies (Install per chapter)

```bash
# Ch 01-03: Core
pip install fastapi uvicorn[standard]

# Ch 02: Email validation
pip install pydantic[email]

# Ch 04: Authentication
pip install python-jose[cryptography] passlib[bcrypt]

# Ch 05: SQL Database
pip install sqlalchemy

# Ch 06: MongoDB
pip install motor beanie

# Ch 07: File uploads
pip install python-multipart aiofiles

# Ch 08: Testing
pip install pytest httpx

# Ch 09: Cloud config
pip install pydantic-settings

# Ch 10: AI/ML
pip install openai langchain langchain-openai chromadb

# Ch 11: Production (all combined)
pip install fastapi uvicorn[standard] pydantic[email] pydantic-settings sqlalchemy python-jose[cryptography] passlib[bcrypt]
```

---

## Express → FastAPI Cheat Sheet

| Concept | Express.js | FastAPI |
|---------|-----------|---------|
| Create app | `const app = express()` | `app = FastAPI()` |
| GET route | `app.get('/path', handler)` | `@app.get("/path")` |
| Request body | `req.body` | Pydantic model parameter |
| URL params | `req.params.id` | `def func(id: int):` |
| Query params | `req.query.page` | `def func(page: int = 1):` |
| Middleware | `app.use(fn)` | `@app.middleware("http")` |
| Auth middleware | custom middleware | `Depends(get_current_user)` |
| Router | `express.Router()` | `APIRouter()` |
| Validation | Joi / Zod | Pydantic (built-in) |
| ORM | Sequelize / Prisma | SQLAlchemy |
| MongoDB | Mongoose | Motor + Beanie |
| Testing | Jest + Supertest | pytest + TestClient |
| Env config | dotenv | pydantic-settings |
| Run server | `node server.js` | `uvicorn main:app` |
| Auto-reload | `nodemon` | `uvicorn --reload` |
| API Docs | Swagger plugin | Built-in at `/docs` |

---

## Suggested Learning Order

1. Read `theory.md` for the concept
2. Run `main.py` and explore the Swagger docs at `/docs`
3. Modify the code and experiment
4. Move to the next chapter

Each chapter builds on the previous one. The final chapter (11) combines everything into production-grade structure.
