# Chapter 07: Advanced Patterns

## Topics Covered

1. **Background Tasks** — Fire-and-forget jobs (like Node.js `setImmediate`)
2. **WebSockets** — Real-time bidirectional communication (like `socket.io`)
3. **File Upload/Download** — Handling multipart files
4. **Streaming Responses** — SSE (Server-Sent Events) and streaming
5. **APIRouter** — Modular route organization (like Express Router)

## 1. Background Tasks

In Express, you might use `setTimeout` or a job queue (Bull). FastAPI has a built-in `BackgroundTasks`:

```python
from fastapi import BackgroundTasks

def send_email(to: str, body: str):
    # This runs AFTER the response is sent
    time.sleep(5)  # simulate slow operation
    print(f"Email sent to {to}")

@app.post("/register")
def register(bg: BackgroundTasks):
    bg.add_task(send_email, "user@test.com", "Welcome!")
    return {"message": "Registered!"}  # returns immediately
```

For heavy background work, use **Celery** or **ARQ** (Redis-based task queue).

## 2. WebSockets

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Echo: {data}")
```

- FastAPI WebSockets are **native** (not a plugin like socket.io)
- For rooms/broadcasting, manage connections manually or use `broadcaster` library

## 3. File Uploads

```python
from fastapi import UploadFile, File

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}
```

- `UploadFile` is async and memory-efficient (streams large files)
- Like `multer` in Express

## 4. APIRouter — Modular Routes

Like `express.Router()`:

```python
# routes/users.py
router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
def list_users():
    ...

# main.py
app.include_router(router)
```

## 5. Streaming Responses & SSE

```python
from fastapi.responses import StreamingResponse

async def event_generator():
    for i in range(10):
        yield f"data: message {i}\n\n"
        await asyncio.sleep(1)

@app.get("/stream")
def stream():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```
