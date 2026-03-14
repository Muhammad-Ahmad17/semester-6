"""
Chapter 07: Advanced Patterns
===============================
pip install python-multipart aiofiles
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import (
    FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect,
    UploadFile, File, Form, HTTPException, APIRouter, Request,
)
from fastapi.responses import StreamingResponse, FileResponse, HTMLResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import asyncio
import json
import time
import os
from datetime import datetime, timezone

app = FastAPI(title="Chapter 07 - Advanced Patterns")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════
# SECTION 1: BACKGROUND TASKS
# ═══════════════════════════════════════════════════════════════════

# Simulated task log
task_log: list[dict] = []


def write_log(message: str):
    """Runs in background AFTER response is sent."""
    time.sleep(1)  # simulate slow I/O
    task_log.append({
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"[BG TASK] {message}")


def send_notification_email(email: str, subject: str, body: str):
    """Simulate sending an email (runs in background)."""
    time.sleep(2)  # simulate SMTP delay
    task_log.append({
        "message": f"Email sent to {email}: {subject}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    print(f"[EMAIL] Sent '{subject}' to {email}")


class NotificationRequest(BaseModel):
    email: str
    subject: str = "Hello"
    body: str = "This is a notification"


@app.post("/notifications/send")
def send_notification(
    notification: NotificationRequest,
    background_tasks: BackgroundTasks,
):
    """
    Sends response IMMEDIATELY, processes email in background.
    Express equivalent: res.json({...}); setImmediate(() => sendEmail(...))
    """
    background_tasks.add_task(
        send_notification_email,
        notification.email,
        notification.subject,
        notification.body,
    )
    background_tasks.add_task(write_log, f"Notification queued for {notification.email}")

    return {"message": "Notification queued", "email": notification.email}


@app.get("/notifications/log")
def get_task_log():
    """Check background task execution log."""
    return {"tasks_completed": len(task_log), "log": task_log[-20:]}


# ═══════════════════════════════════════════════════════════════════
# SECTION 2: WEBSOCKETS
# ═══════════════════════════════════════════════════════════════════

class ConnectionManager:
    """
    Manages WebSocket connections (like socket.io rooms).
    In production, use Redis pub/sub for multi-process support.
    """

    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room: str = "general"):
        await websocket.accept()
        if room not in self.active_connections:
            self.active_connections[room] = []
        self.active_connections[room].append(websocket)

    def disconnect(self, websocket: WebSocket, room: str = "general"):
        if room in self.active_connections:
            self.active_connections[room].remove(websocket)

    async def send_personal(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room: str = "general"):
        if room in self.active_connections:
            for connection in self.active_connections[room]:
                await connection.send_text(message)

    def get_stats(self) -> dict:
        return {
            room: len(connections)
            for room, connections in self.active_connections.items()
        }


manager = ConnectionManager()


@app.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str, username: str = "anonymous"):
    """
    WebSocket chat room.
    Connect: ws://localhost:8000/ws/general?username=Ahmad
    """
    await manager.connect(websocket, room)
    await manager.broadcast(
        json.dumps({"type": "join", "user": username, "room": room}),
        room,
    )

    try:
        while True:
            data = await websocket.receive_text()
            message = json.dumps({
                "type": "message",
                "user": username,
                "content": data,
                "room": room,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
            await manager.broadcast(message, room)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room)
        await manager.broadcast(
            json.dumps({"type": "leave", "user": username, "room": room}),
            room,
        )


@app.get("/ws/stats")
def websocket_stats():
    return manager.get_stats()


# ─── WebSocket Test Page ─────────────────────────────────────────
@app.get("/ws-test", response_class=HTMLResponse)
def websocket_test_page():
    """A simple HTML page to test WebSocket connections."""
    return """
    <!DOCTYPE html>
    <html><head><title>WebSocket Test</title></head>
    <body>
        <h2>WebSocket Chat Test</h2>
        <input id="room" value="general" placeholder="Room">
        <input id="username" value="TestUser" placeholder="Username">
        <button onclick="connect()">Connect</button>
        <br><br>
        <input id="message" placeholder="Type a message..." size="50">
        <button onclick="send()">Send</button>
        <pre id="log" style="background:#111;color:#0f0;padding:10px;height:300px;overflow:auto;"></pre>
        <script>
            let ws;
            function connect() {
                const room = document.getElementById('room').value;
                const user = document.getElementById('username').value;
                ws = new WebSocket(`ws://localhost:8000/ws/${room}?username=${user}`);
                ws.onmessage = (e) => {
                    document.getElementById('log').textContent += e.data + '\\n';
                };
                ws.onopen = () => log('Connected!');
                ws.onclose = () => log('Disconnected.');
            }
            function send() {
                const msg = document.getElementById('message').value;
                ws.send(msg);
                document.getElementById('message').value = '';
            }
            function log(msg) {
                document.getElementById('log').textContent += '--- ' + msg + ' ---\\n';
            }
        </script>
    </body></html>
    """


# ═══════════════════════════════════════════════════════════════════
# SECTION 3: FILE UPLOAD & DOWNLOAD
# ═══════════════════════════════════════════════════════════════════

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(..., description="File to upload"),
    description: str = Form(""),
):
    """
    Upload a file (like multer in Express).
    Use multipart/form-data in Postman or Swagger UI.
    """
    # Validate file size (5MB limit)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(413, "File too large (max 5MB)")

    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "application/pdf", "text/plain"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            415, f"Unsupported file type: {file.content_type}. Allowed: {allowed_types}"
        )

    # Save file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "description": description,
        "path": file_path,
    }


@app.post("/upload/multiple")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    """Upload multiple files at once."""
    results = []
    for file in files:
        contents = await file.read()
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(contents)
        results.append({"filename": file.filename, "size": len(contents)})
    return {"uploaded": len(results), "files": results}


@app.get("/download/{filename}")
def download_file(filename: str):
    """Download a previously uploaded file."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(404, "File not found")
    return FileResponse(file_path, filename=filename)


@app.get("/files")
def list_uploaded_files():
    """List all uploaded files."""
    files = []
    for f in os.listdir(UPLOAD_DIR):
        path = os.path.join(UPLOAD_DIR, f)
        files.append({
            "name": f,
            "size_bytes": os.path.getsize(path),
        })
    return {"files": files}


# ═══════════════════════════════════════════════════════════════════
# SECTION 4: STREAMING RESPONSES & SSE
# ═══════════════════════════════════════════════════════════════════

async def number_stream():
    """Generator that yields numbers with a delay (SSE format)."""
    for i in range(1, 21):
        data = json.dumps({"number": i, "timestamp": datetime.now(timezone.utc).isoformat()})
        yield f"data: {data}\n\n"
        await asyncio.sleep(0.5)
    yield "data: {\"done\": true}\n\n"


@app.get("/stream/numbers")
def stream_numbers():
    """
    Server-Sent Events (SSE) — server pushes data to client.
    Like EventSource in JavaScript:
    const es = new EventSource('/stream/numbers')
    es.onmessage = (e) => console.log(JSON.parse(e.data))
    """
    return StreamingResponse(
        number_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


async def large_data_generator():
    """Simulate streaming a large dataset."""
    yield "["
    for i in range(100):
        item = json.dumps({"id": i, "value": f"item_{i}"})
        prefix = "" if i == 0 else ","
        yield f"{prefix}{item}"
        await asyncio.sleep(0.05)
    yield "]"


@app.get("/stream/data")
def stream_large_data():
    """Stream a large JSON array without loading it all in memory."""
    return StreamingResponse(
        large_data_generator(),
        media_type="application/json",
    )


# ═══════════════════════════════════════════════════════════════════
# SECTION 5: APIRouter (Modular Routes)
# ═══════════════════════════════════════════════════════════════════

# In a real project, each router would be in its own file:
# routes/health.py, routes/demo.py, etc.

health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("/")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}


@health_router.get("/detailed")
def detailed_health():
    return {
        "status": "healthy",
        "uptime": "running",
        "websocket_rooms": manager.get_stats(),
        "uploaded_files": len(os.listdir(UPLOAD_DIR)),
        "background_tasks_completed": len(task_log),
    }


# Register the router (like app.use('/health', healthRouter) in Express)
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "Chapter 07 - Advanced Patterns",
        "sections": {
            "background_tasks": "/notifications/send",
            "websocket_test": "/ws-test",
            "file_upload": "/upload",
            "streaming": "/stream/numbers",
            "health": "/health",
        },
    }
