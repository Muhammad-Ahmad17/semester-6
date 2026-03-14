"""
Chapter 10: AI/ML Integration
===============================
pip install openai langchain langchain-openai chromadb
Run: uvicorn main:app --reload --port 8000

IMPORTANT: Set your OpenAI API key as an environment variable:
  export OPENAI_API_KEY=sk-your-key-here
Or create a .env file with: OPENAI_API_KEY=sk-your-key-here
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from typing import Optional
from contextlib import asynccontextmanager
from datetime import datetime, timezone
import json
import asyncio
import hashlib

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    max_tokens: int = 1024

    model_config = {"env_file": ".env"}

settings = Settings()


# ═══════════════════════════════════════════════════════════════════
# AI CLIENT SETUP
# ═══════════════════════════════════════════════════════════════════

openai_client = None
chroma_collection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global openai_client, chroma_collection

    # Initialize OpenAI client
    if settings.openai_api_key:
        from openai import OpenAI
        openai_client = OpenAI(api_key=settings.openai_api_key)
        print("OpenAI client initialized")
    else:
        print("WARNING: OPENAI_API_KEY not set. AI features will use mock responses.")

    # Initialize ChromaDB for RAG
    try:
        import chromadb
        chroma_client = chromadb.Client()
        chroma_collection = chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"},
        )
        print("ChromaDB initialized")
    except ImportError:
        print("ChromaDB not installed. RAG features disabled.")

    yield
    print("Shutting down AI services...")


app = FastAPI(title="Chapter 10 - AI/ML Integration", lifespan=lifespan)


# ═══════════════════════════════════════════════════════════════════
# REQUEST/RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════════

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., min_length=1)
    model: Optional[str] = None
    max_tokens: int = Field(default=1024, ge=1, le=4096)
    temperature: float = Field(default=0.7, ge=0, le=2.0)
    stream: bool = False


class ChatResponse(BaseModel):
    content: str
    model: str
    usage: dict
    created_at: str


class EmbeddingRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)


class DocumentInput(BaseModel):
    content: str = Field(..., min_length=1)
    metadata: dict = {}


class RAGQuery(BaseModel):
    question: str = Field(..., min_length=1)
    n_results: int = Field(default=3, ge=1, le=10)


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, max_length=50000)
    style: str = Field(default="concise", pattern="^(concise|detailed|bullet_points)$")


# ═══════════════════════════════════════════════════════════════════
# RESPONSE CACHE (Simple in-memory cache to reduce API costs)
# ═══════════════════════════════════════════════════════════════════

response_cache: dict[str, dict] = {}


def get_cache_key(messages: list[dict], model: str) -> str:
    content = json.dumps(messages) + model
    return hashlib.md5(content.encode()).hexdigest()


# ═══════════════════════════════════════════════════════════════════
# SECTION 1: BASIC CHAT COMPLETION
# ═══════════════════════════════════════════════════════════════════

@app.post("/ai/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    """
    Basic chat completion (like ChatGPT).
    Sends messages to OpenAI and returns the response.
    """
    model = request.model or settings.openai_model
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    # Check cache
    cache_key = get_cache_key(messages, model)
    if cache_key in response_cache:
        return response_cache[cache_key]

    if not openai_client:
        # Mock response when no API key
        return ChatResponse(
            content=f"[MOCK] Echo: {messages[-1]['content']}",
            model="mock",
            usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=request.max_tokens,
        temperature=request.temperature,
    )

    result = ChatResponse(
        content=response.choices[0].message.content,
        model=response.model,
        usage={
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        },
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    # Cache the response
    response_cache[cache_key] = result
    return result


# ═══════════════════════════════════════════════════════════════════
# SECTION 2: STREAMING CHAT (like ChatGPT typing effect)
# ═══════════════════════════════════════════════════════════════════

async def stream_openai_response(messages: list[dict], model: str, max_tokens: int, temperature: float):
    """
    Generator that yields SSE events as the AI generates tokens.
    Frontend can use EventSource or fetch() to consume this.
    """
    if not openai_client:
        # Mock streaming
        mock_response = f"[MOCK] I received: {messages[-1]['content']}"
        for word in mock_response.split():
            yield f"data: {json.dumps({'content': word + ' '})}\n\n"
            await asyncio.sleep(0.1)
        yield f"data: {json.dumps({'done': True})}\n\n"
        return

    stream = openai_client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            data = json.dumps({"content": chunk.choices[0].delta.content})
            yield f"data: {data}\n\n"

    yield f"data: {json.dumps({'done': True})}\n\n"


@app.post("/ai/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat — returns Server-Sent Events (SSE).

    Frontend usage:
    ```javascript
    const response = await fetch('/ai/chat/stream', {
        method: 'POST',
        body: JSON.stringify({ messages: [...] }),
        headers: { 'Content-Type': 'application/json' },
    });
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const text = decoder.decode(value);
        // parse SSE data lines
    }
    ```
    """
    model = request.model or settings.openai_model
    messages = [{"role": m.role, "content": m.content} for m in request.messages]

    return StreamingResponse(
        stream_openai_response(messages, model, request.max_tokens, request.temperature),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


# ═══════════════════════════════════════════════════════════════════
# SECTION 3: EMBEDDINGS
# ═══════════════════════════════════════════════════════════════════

@app.post("/ai/embeddings")
async def create_embedding(request: EmbeddingRequest):
    """
    Create a text embedding (vector representation).
    Used for: semantic search, similarity, RAG.
    """
    if not openai_client:
        # Mock embedding
        import random
        return {
            "embedding": [random.random() for _ in range(10)],
            "dimensions": 10,
            "model": "mock",
        }

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=request.text,
    )

    return {
        "embedding": response.data[0].embedding[:10],  # truncated for readability
        "dimensions": len(response.data[0].embedding),
        "model": response.model,
        "usage": {"total_tokens": response.usage.total_tokens},
    }


# ═══════════════════════════════════════════════════════════════════
# SECTION 4: RAG (Retrieval Augmented Generation)
# ═══════════════════════════════════════════════════════════════════

@app.post("/ai/rag/documents")
async def add_document(doc: DocumentInput):
    """
    Add a document to the vector store for RAG.
    The document is split, embedded, and stored in ChromaDB.
    """
    if not chroma_collection:
        raise HTTPException(503, "ChromaDB not initialized. Install: pip install chromadb")

    doc_id = hashlib.md5(doc.content.encode()).hexdigest()

    # ChromaDB handles embeddings automatically with its default model
    chroma_collection.add(
        documents=[doc.content],
        metadatas=[doc.metadata],
        ids=[doc_id],
    )

    return {
        "message": "Document added to vector store",
        "id": doc_id,
        "content_length": len(doc.content),
    }


@app.post("/ai/rag/query")
async def rag_query(query: RAGQuery):
    """
    RAG Query Flow:
    1. Search vector store for relevant documents
    2. Build a prompt with the found context
    3. Send to LLM for answer generation
    """
    if not chroma_collection:
        raise HTTPException(503, "ChromaDB not initialized")

    # Step 1: Retrieve relevant documents
    results = chroma_collection.query(
        query_texts=[query.question],
        n_results=query.n_results,
    )

    if not results["documents"][0]:
        return {
            "answer": "No relevant documents found. Please add documents first.",
            "sources": [],
        }

    # Step 2: Build context from retrieved documents
    context = "\n\n---\n\n".join(results["documents"][0])

    # Step 3: Generate answer with context
    system_prompt = (
        "You are a helpful assistant. Answer the user's question based ONLY on the "
        "provided context. If the context doesn't contain the answer, say so.\n\n"
        f"Context:\n{context}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query.question},
    ]

    if not openai_client:
        return {
            "answer": f"[MOCK] Based on {len(results['documents'][0])} documents: {query.question}",
            "sources": results["documents"][0],
            "distances": results.get("distances", [[]])[0],
        }

    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        max_tokens=settings.max_tokens,
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": results["documents"][0],
        "distances": results.get("distances", [[]])[0],
        "model": response.model,
    }


@app.get("/ai/rag/documents")
async def list_documents():
    """List all documents in the vector store."""
    if not chroma_collection:
        raise HTTPException(503, "ChromaDB not initialized")

    count = chroma_collection.count()
    return {"total_documents": count}


# ═══════════════════════════════════════════════════════════════════
# SECTION 5: UTILITY AI ENDPOINTS
# ═══════════════════════════════════════════════════════════════════

@app.post("/ai/summarize")
async def summarize_text(request: SummarizeRequest):
    """Summarize a long text using AI."""
    style_instructions = {
        "concise": "Provide a brief 2-3 sentence summary.",
        "detailed": "Provide a comprehensive summary covering all key points.",
        "bullet_points": "Summarize as a list of bullet points (max 10).",
    }

    messages = [
        {"role": "system", "content": f"You are a summarization expert. {style_instructions[request.style]}"},
        {"role": "user", "content": f"Summarize the following text:\n\n{request.text}"},
    ]

    if not openai_client:
        return {"summary": f"[MOCK] Summary of {len(request.text)} chars in {request.style} style", "style": request.style}

    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        max_tokens=settings.max_tokens,
    )

    return {
        "summary": response.choices[0].message.content,
        "style": request.style,
        "original_length": len(request.text),
        "usage": {
            "total_tokens": response.usage.total_tokens,
        },
    }


@app.post("/ai/translate")
async def translate_text(text: str, target_language: str = "Urdu"):
    """Translate text to a target language."""
    messages = [
        {"role": "system", "content": f"Translate the following text to {target_language}. Only output the translation."},
        {"role": "user", "content": text},
    ]

    if not openai_client:
        return {"translation": f"[MOCK] {text} → {target_language}", "target_language": target_language}

    response = openai_client.chat.completions.create(
        model=settings.openai_model,
        messages=messages,
        max_tokens=settings.max_tokens,
    )

    return {
        "original": text,
        "translation": response.choices[0].message.content,
        "target_language": target_language,
    }


# ═══════════════════════════════════════════════════════════════════
# SECTION 6: LANGCHAIN INTEGRATION
# ═══════════════════════════════════════════════════════════════════

@app.post("/ai/langchain/chain")
async def langchain_chain(topic: str, style: str = "simple"):
    """
    Demonstrates LangChain's chain pattern:
    Prompt → LLM → Output Parser
    """
    try:
        from langchain_openai import ChatOpenAI
        from langchain.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
    except ImportError:
        return {"error": "LangChain not installed. Run: pip install langchain langchain-openai"}

    if not settings.openai_api_key:
        return {"output": f"[MOCK] LangChain explanation of {topic} in {style} style"}

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.7,
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert teacher. Explain topics in a {style} way."),
        ("user", "Explain {topic}"),
    ])

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({"topic": topic, "style": style})

    return {"topic": topic, "style": style, "output": result}


# ═══════════════════════════════════════════════════════════════════
# ROOT
# ═══════════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return {
        "message": "Chapter 10 - AI/ML Integration",
        "openai_configured": bool(settings.openai_api_key),
        "chromadb_available": chroma_collection is not None,
        "endpoints": {
            "chat": "/ai/chat",
            "streaming_chat": "/ai/chat/stream",
            "embeddings": "/ai/embeddings",
            "rag_add": "POST /ai/rag/documents",
            "rag_query": "POST /ai/rag/query",
            "summarize": "/ai/summarize",
            "translate": "/ai/translate",
            "langchain": "/ai/langchain/chain",
        },
    }
