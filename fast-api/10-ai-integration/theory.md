# Chapter 10: AI/ML Integration

## Overview

This chapter covers integrating AI/ML capabilities into your FastAPI backend:

1. **OpenAI API** — ChatGPT, embeddings, image generation
2. **LangChain** — Build AI chains and agents
3. **Streaming AI Responses** — Real-time token streaming (like ChatGPT UI)
4. **Serving ML Models** — Load and serve your own models
5. **RAG (Retrieval Augmented Generation)** — AI + your own data

## Node.js → Python AI Mapping

| Node.js | Python (FastAPI) |
|---|---|
| `openai` npm package | `openai` Python package |
| `langchain` npm | `langchain` Python (more mature) |
| TensorFlow.js | PyTorch / TensorFlow |
| `@huggingface/inference` | `transformers` (Hugging Face) |

## 1. OpenAI Integration

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# Chat completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content, end="")
```

## 2. Streaming AI Responses (SSE)

The ChatGPT typing effect uses **Server-Sent Events (SSE)**:

```python
from fastapi.responses import StreamingResponse

async def ai_stream():
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[...],
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield f"data: {json.dumps({'content': content})}\n\n"

@app.post("/chat/stream")
def chat_stream(prompt: str):
    return StreamingResponse(ai_stream(), media_type="text/event-stream")
```

## 3. LangChain Basics

LangChain lets you build complex AI workflows:

```python
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Explain {topic} in simple terms")
chain = prompt | llm

result = chain.invoke({"topic": "quantum computing"})
```

## 4. RAG (Retrieval Augmented Generation)

RAG = feed your own documents to the AI:

```
User Question → Search Your Documents → Found Context + Question → LLM → Answer
```

Components:
1. **Embeddings** — convert text to vectors
2. **Vector Store** — store and search vectors (ChromaDB, Pinecone, Weaviate)
3. **Retriever** — find relevant documents
4. **LLM** — generate answer using found context

## 5. Serving Your Own ML Models

```python
import torch

# Load model once at startup
model = torch.load("model.pth")
model.eval()

@app.post("/predict")
def predict(data: InputData):
    tensor = preprocess(data)
    with torch.no_grad():
        prediction = model(tensor)
    return {"prediction": prediction.tolist()}
```

## Dependencies

```bash
# OpenAI
pip install openai

# LangChain
pip install langchain langchain-openai

# Vector store for RAG
pip install chromadb

# ML model serving
pip install torch transformers
```

## Important Notes

- **API Keys**: Always use environment variables, never hardcode
- **Rate Limiting**: OpenAI has rate limits — implement caching and queuing
- **Cost Management**: Track token usage, set spending limits
- **Latency**: AI calls are slow (1-10s) — use background tasks or streaming
- **Caching**: Cache common queries to reduce API costs
