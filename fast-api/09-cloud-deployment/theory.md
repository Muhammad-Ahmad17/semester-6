# Chapter 09: Cloud Deployment

## Deployment Options

| Platform | Difficulty | Cost | Best For |
|---|---|---|---|
| Docker + VPS | Medium | Low ($5-20/mo) | Full control |
| AWS (ECS/Lambda) | High | Pay-per-use | Enterprise scale |
| Google Cloud Run | Medium | Pay-per-use | Serverless containers |
| Azure Container Apps | Medium | Pay-per-use | Microsoft ecosystem |
| Railway / Render | Low | Free tier | Quick deploys, side projects |
| Vercel (via serverless) | Low | Free tier | Serverless functions |

## 1. Docker (Foundation for All Cloud Deploys)

### Dockerfile Explained

```dockerfile
# Stage 1: Base image with Python
FROM python:3.12-slim

# Set working directory (like `cd /app` in the container)
WORKDIR /app

# Copy requirements first (Docker caches this layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose port (documentation, not enforcement)
EXPOSE 8000

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Commands
```bash
# Build the image
docker build -t myapi .

# Run locally
docker run -p 8000:8000 myapi

# Run with environment variables
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... myapi

# Docker Compose (multi-container: app + database)
docker compose up -d
```

### Multi-Stage Build (Smaller Image)
```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 2. Docker Compose (App + DB + Redis)

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:16
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

volumes:
  pgdata:
```

## 3. Environment Variables & Secrets

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    redis_url: str = "redis://localhost:6379"

    model_config = {"env_file": ".env"}

settings = Settings()
```

**.env file** (NEVER commit this):
```
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
SECRET_KEY=super-secret-production-key
DEBUG=false
```

## 4. AWS Deployment Options

### Option A: AWS ECS (Elastic Container Service)
1. Push Docker image to ECR (Elastic Container Registry)
2. Create ECS Task Definition
3. Deploy on Fargate (serverless containers)

### Option B: AWS Lambda + API Gateway
- Use **Mangum** adapter: `handler = Mangum(app)`
- Deploy as a Lambda function
- API Gateway routes to Lambda

### Option C: AWS EC2 (Traditional VPS)
- SSH into EC2 instance
- Install Docker, pull image, run

## 5. Google Cloud Run (Recommended for Simplicity)

```bash
# Build and push to Google Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/myapi

# Deploy to Cloud Run
gcloud run deploy myapi \
  --image gcr.io/PROJECT_ID/myapi \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=...,SECRET_KEY=...
```

## 6. CI/CD with GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Cloud Run
        # ... deployment steps
```

## Production Checklist

- [ ] Environment variables for all secrets
- [ ] HTTPS (TLS) enabled
- [ ] CORS properly configured
- [ ] Rate limiting
- [ ] Health check endpoint (`/health`)
- [ ] Structured logging (JSON)
- [ ] Error monitoring (Sentry)
- [ ] Database connection pooling
- [ ] Graceful shutdown handling
- [ ] Docker image is minimal (multi-stage build)
