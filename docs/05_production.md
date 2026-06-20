# Production Tips & Best Practices

Guidelines for deploying agentic AI systems to production.

## Architecture Considerations

### 1. Separate Services

```
┌─────────────┐
│   Web UI    │ (Streamlit/React)
└──────┬──────┘
       │
┌──────▼──────┐
│   API       │ (FastAPI)
└──────┬──────┘
       │
┌──────▼──────┐
│   Agent     │ (LangChain)
└──────┬──────┘
       │
┌──────▼──────┐
│  Vector DB  │ (Chroma/Pinecone)
└─────────────┘
```

### 2. Use FastAPI for Agent API

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Agent API")

class Query(BaseModel):
    question: str
    session_id: Optional[str] = None

class Response(BaseModel):
    answer: str
    sources: list
    session_id: str

@app.post("/query", response_model=Response)
async def query_agent(query: Query):
    try:
        result = agent.ask(query.question, query.session_id)
        return Response(
            answer=result["answer"],
            sources=result["sources"],
            session_id=result["session_id"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## Performance Optimization

### 1. Caching

```python
from langchain.cache import RedisCache, InMemoryCache
import langchain

# In-memory (single server)
langchain.llm_cache = InMemoryCache()

# Redis (distributed)
langchain.llm_cache = RedisCache(
    redis_url="redis://localhost:6379"
)

# Result caching for identical queries
@lru_cache(maxsize=1000)
def cached_retrieval(query: str):
    return retriever.get_relevant_documents(query)
```

### 2. Async Operations

```python
from langchain.callbacks import AsyncIteratorCallbackHandler
import asyncio

async def async_generate(prompt: str):
    """Async LLM generation."""
    callback = AsyncIteratorCallbackHandler()
    
    task = asyncio.create_task(
        llm.agenerate([[prompt]], callbacks=[callback])
    )
    
    async for token in callback.aiter():
        yield token
    
    await task

# Parallel retrieval
async def parallel_retrieval(queries: list):
    tasks = [retriever.aget_relevant_documents(q) for q in queries]
    return await asyncio.gather(*tasks)
```

### 3. Streaming Responses

```python
from fastapi.responses import StreamingResponse

@app.post("/stream")
async def stream_response(query: Query):
    async def generate():
        async for chunk in agent.astream(query.question):
            yield f"data: {chunk}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

### 4. Connection Pooling

```python
from langchain_community.vectorstores import Chroma
import chromadb

# Reuse client
client = chromadb.HttpClient(
    host="localhost",
    port=8000,
    settings=chromadb.Settings(
        chroma_client_max_retries=3,
        chroma_client_timeout=30
    )
)

vectorstore = Chroma(
    client=client,
    collection_name="docs"
)
```

## Error Handling

### 1. Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_llm_with_retry(prompt: str):
    """LLM call with automatic retries."""
    return llm.invoke(prompt)
```

### 2. Graceful Degradation

```python
def safe_agent_call(query: str):
    """Agent call with fallback."""
    try:
        return agent.invoke(query)
    except RateLimitError:
        return {"error": "Rate limit exceeded, try again later"}
    except TimeoutError:
        return {"error": "Request timed out"}
    except Exception as e:
        logger.error(f"Agent error: {e}")
        return {"error": "Sorry, something went wrong"}
```

### 3. Input Validation

```python
from pydantic import BaseModel, validator, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    
    @validator('question')
    def validate_question(cls, v):
        if not v.strip():
            raise ValueError("Question cannot be empty")
        
        # Check for malicious content
        forbidden = ["<script>", "DROP TABLE"]
        if any(bad in v.lower() for bad in forbidden):
            raise ValueError("Invalid input")
        
        return v.strip()
```

## Monitoring & Logging

### 1. LangSmith Integration

```python
import os

# Enable tracing
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "production"
os.environ["LANGSMITH_API_KEY"] = "your-key"

# Automatically logs all chains, agents, and tools
```

### 2. Custom Logging

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_agent_interaction(query: str, response: str, metadata: dict):
    """Log agent interactions."""
    logger.info({
        "timestamp": datetime.utcnow().isoformat(),
        "query": query,
        "response_length": len(response),
        "metadata": metadata
    })
```

### 3. Metrics

```python
from prometheus_client import Counter, Histogram, start_http_server

# Define metrics
queries_total = Counter('agent_queries_total', 'Total queries')
query_duration = Histogram('agent_query_duration_seconds', 'Query duration')
errors_total = Counter('agent_errors_total', 'Total errors')

# Track metrics
@query_duration.time()
def process_query(query: str):
    queries_total.inc()
    try:
        result = agent.invoke(query)
        return result
    except Exception as e:
        errors_total.inc()
        raise

# Start metrics server
start_http_server(8000)
```

## Security

### 1. Input Sanitization

```python
import re

def sanitize_input(text: str) -> str:
    """Remove potentially harmful content."""
    # Remove special characters
    text = re.sub(r'[^\w\s\-.,!?]', '', text)
    
    # Limit length
    text = text[:1000]
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    return text
```

### 2. Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/query")
@limiter.limit("10/minute")
async def limited_query(request: Request, query: Query):
    return await query_agent(query)
```

### 3. Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials
    if not is_valid_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return token

@app.post("/query")
async def protected_query(
    query: Query,
    token: str = Depends(verify_token)
):
    return await query_agent(query)
```

### 4. Environment Variables

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment."""
    ollama_url: str
    model_name: str
    vector_db_url: str
    api_key: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Database Management

### 1. Connection Management

```python
from contextlib import contextmanager

@contextmanager
def get_vectorstore():
    """Context manager for vector store connections."""
    client = chromadb.HttpClient()
    try:
        vectorstore = Chroma(client=client)
        yield vectorstore
    finally:
        # Cleanup if needed
        pass

# Usage
with get_vectorstore() as vs:
    results = vs.similarity_search("query")
```

### 2. Migrations

```python
def migrate_vector_store():
    """Migrate vector store schema."""
    old_store = Chroma(persist_directory="./old_db")
    new_store = Chroma(persist_directory="./new_db")
    
    # Get all documents
    docs = old_store.get()
    
    # Re-embed with new embeddings
    new_store.add_documents(docs)
    
    print("Migration complete")
```

## Deployment

### 1. Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_URL=http://ollama:11434
      - CHROMA_URL=http://chroma:8000
    depends_on:
      - ollama
      - chroma

  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama

  chroma:
    image: chromadb/chroma
    ports:
      - "8001:8000"
    volumes:
      - chroma-data:/chroma/chroma

volumes:
  ollama-data:
  chroma-data:
```

### 2. Health Checks

```python
@app.get("/health")
async def health_check():
    """Comprehensive health check."""
    checks = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Check LLM
    try:
        llm.invoke("test")
        checks["checks"]["llm"] = "ok"
    except Exception as e:
        checks["checks"]["llm"] = f"error: {e}"
        checks["status"] = "unhealthy"
    
    # Check vector store
    try:
        vectorstore.similarity_search("test", k=1)
        checks["checks"]["vectorstore"] = "ok"
    except Exception as e:
        checks["checks"]["vectorstore"] = f"error: {e}"
        checks["status"] = "unhealthy"
    
    status_code = 200 if checks["status"] == "healthy" else 503
    return JSONResponse(content=checks, status_code=status_code)
```

## Cost Optimization

### 1. Prompt Optimization

```python
# Bad: verbose prompt
prompt = """You are a helpful assistant. Please read the following 
context carefully and provide a detailed answer to the question..."""

# Good: concise prompt
prompt = "Answer based on context:\n{context}\n\nQ: {question}\nA:"
```

### 2. Model Selection

```python
# Route by complexity
def select_model(query: str):
    if len(query.split()) < 10:
        return "llama3.2"  # Fast, cheap
    else:
        return "llama3.1:8b"  # More capable

model = select_model(user_query)
llm = Ollama(model=model)
```

### 3. Batch Processing

```python
# Process multiple queries together
queries = ["q1", "q2", "q3"]
responses = llm.batch(queries)
```

## Testing

### 1. Unit Tests

```python
import pytest

def test_agent_basic():
    response = agent.invoke("What is 2+2?")
    assert "4" in response["output"]

def test_retrieval():
    docs = retriever.get_relevant_documents("test")
    assert len(docs) > 0

@pytest.mark.asyncio
async def test_async_agent():
    response = await agent.ainvoke("test query")
    assert response is not None
```

### 2. Integration Tests

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_api_query():
    response = client.post(
        "/query",
        json={"question": "What is Python?"}
    )
    assert response.status_code == 200
    assert "answer" in response.json()
```

## Key Takeaways

✅ **Use async for better performance**  
✅ **Implement caching and connection pooling**  
✅ **Add comprehensive error handling**  
✅ **Monitor with LangSmith and metrics**  
✅ **Secure with authentication and rate limiting**  
✅ **Test thoroughly before deploying**  
✅ **Use Docker for consistent deployments**
