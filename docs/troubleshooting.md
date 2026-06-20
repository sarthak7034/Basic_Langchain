# Troubleshooting Guide

Common issues and solutions for the AgentAI project.

## Installation Issues

### Python Version Error

**Problem**: `Python 3.10 or higher required`

**Solution**:
```bash
# Check version
python --version

# If too old, download from python.org
# Or use pyenv to manage versions
```

### Pip Install Fails

**Problem**: Packages fail to install

**Solution**:
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Clear cache
pip cache purge

# Install with verbose output
pip install -r requirements.txt -v

# Try one package at a time
pip install langchain
```

### Virtual Environment Issues

**Problem**: `venv\Scripts\activate` not working

**Solution**:
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# If permission error (PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative: use conda
conda create -n agentai python=3.11
conda activate agentai
```

## Ollama Issues

### Ollama Not Found

**Problem**: `ollama: command not found`

**Solution**:
1. Download from https://ollama.ai
2. Install for your OS
3. Verify: `ollama --version`
4. Restart terminal

### Ollama Not Running

**Problem**: `Connection refused to localhost:11434`

**Solution**:
```bash
# Start Ollama
ollama serve

# Check if running
curl http://localhost:11434
# Should return "Ollama is running"

# Windows: Check Task Manager for Ollama
# Mac/Linux: ps aux | grep ollama
```

### Model Not Found

**Problem**: `model 'llama3.2' not found`

**Solution**:
```bash
# List installed models
ollama list

# Pull the model
ollama pull llama3.2

# Verify
ollama list | grep llama3.2

# Try running it
ollama run llama3.2 "Hello"
```

### Ollama Slow/Hanging

**Problem**: Ollama taking too long to respond

**Solution**:
```bash
# Check system resources
# RAM: Need 8GB+ free
# CPU: High usage is normal

# Try smaller model
ollama pull llama3.2  # 2B parameters, faster

# Stop other models
ollama ps
ollama stop model-name

# Restart Ollama
# Windows: Close from system tray, restart
# Mac/Linux: killall ollama && ollama serve
```

### Port Already in Use

**Problem**: `Port 11434 already in use`

**Solution**:
```bash
# Windows: Find process
netstat -ano | findstr :11434

# Kill process (replace PID)
taskkill /PID <pid> /F

# Or change Ollama port
set OLLAMA_HOST=0.0.0.0:11435
ollama serve
```

## LangChain Issues

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```bash
# Verify virtual environment is active
# Should see (venv) in prompt

# If not active
venv\Scripts\activate

# Reinstall
pip install langchain langchain-community
```

### Deprecation Warnings

**Problem**: Lots of deprecation warnings

**Solution**:
```python
# Update to latest versions
pip install --upgrade langchain langchain-community

# Or ignore warnings
import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
```

### API Key Errors

**Problem**: `API key not found`

**Solution**:
```bash
# For local Ollama, you don't need API keys

# If using OpenAI/Anthropic
# Create .env file
copy .env.example .env

# Edit .env and add keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## Agent Issues

### Agent Loops Forever

**Problem**: Agent keeps calling tools without finishing

**Solution**:
```python
# Set max iterations
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5,  # Limit loops
    max_execution_time=60  # Timeout after 60s
)
```

### Agent Uses Wrong Tool

**Problem**: Agent calls inappropriate tools

**Solution**:
1. **Improve tool descriptions**:
```python
@tool
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.
    
    Use ONLY for math calculations like:
    - "2 + 2"
    - "15 * 3"
    - "(100 - 20) / 4"
    
    DO NOT use for:
    - Text manipulation
    - Dates/times
    - File operations
    """
    return str(eval(expression))
```

2. **Reduce number of tools** (3-5 is ideal)

3. **Set temperature to 0** for consistency

### Parsing Errors

**Problem**: `Could not parse LLM output`

**Solution**:
```python
# Enable error handling
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True  # Auto-retry on parse errors
)

# Or use structured agent
from langchain.agents import create_structured_chat_agent
```

## RAG Issues

### Poor Retrieval Results

**Problem**: Retrieved documents not relevant

**Solution**:
```python
# 1. Adjust chunk size
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Try different sizes
    chunk_overlap=100
)

# 2. Increase k
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 6}  # Get more documents
)

# 3. Check embeddings
docs = retriever.get_relevant_documents("test query")
for doc in docs:
    print(doc.page_content[:100])
```

### Vector Store Empty

**Problem**: No results from similarity search

**Solution**:
```python
# Check if documents loaded
collection = vectorstore._collection
print(f"Document count: {collection.count()}")

# Rebuild if needed
if collection.count() == 0:
    documents = load_documents()
    splits = split_documents(documents)
    vectorstore = Chroma.from_documents(splits, embeddings)
```

### Slow Queries

**Problem**: RAG queries take too long

**Solution**:
```python
# 1. Reduce k
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# 2. Use FAISS instead of Chroma
from langchain_community.vectorstores import FAISS
vectorstore = FAISS.from_documents(splits, embeddings)

# 3. Optimize chunk count
# Fewer, larger chunks = faster (but less precise)
```

### ChromaDB Errors

**Problem**: `chromadb.errors.IDAlreadyExistsError`

**Solution**:
```bash
# Delete and rebuild vector store
rm -rf chroma_db
python chatbot.py  # Will rebuild
```

## Memory Issues

### Out of Memory

**Problem**: System runs out of RAM

**Solution**:
1. **Use smaller model**:
```bash
ollama pull llama3.2  # 2B model, uses less RAM
```

2. **Reduce context**:
```python
# Limit retrieval
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Use summary memory
from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=llm)
```

3. **Close other applications**

### Disk Space Issues

**Problem**: Running out of disk space

**Solution**:
```bash
# Check model sizes
ollama list

# Remove unused models
ollama rm model-name

# Clean ChromaDB
rm -rf chroma_db

# Clean pip cache
pip cache purge
```

## Performance Issues

### Slow Responses

**Problem**: Everything is slow

**Solution**:
1. **Use faster model**: `llama3.2` (2B)
2. **Reduce context**: Lower k, smaller chunks
3. **Enable caching**:
```python
from langchain.cache import InMemoryCache
import langchain
langchain.llm_cache = InMemoryCache()
```
4. **Check system resources**: Task Manager / Activity Monitor

### Timeout Errors

**Problem**: `Timeout waiting for response`

**Solution**:
```python
# Increase timeout
llm = Ollama(
    model="llama3.2",
    timeout=120  # 2 minutes
)

# For agents
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_execution_time=120
)
```

## Windows-Specific Issues

### Path Issues

**Problem**: File paths not working

**Solution**:
```python
# Use os.path
import os
path = os.path.join("data", "file.txt")

# Or pathlib
from pathlib import Path
path = Path("data") / "file.txt"

# Use raw strings for Windows paths
path = r"C:\Users\Name\Documents\file.txt"
```

### Encoding Issues

**Problem**: `UnicodeDecodeError`

**Solution**:
```python
# Specify encoding
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Or for TextLoader
loader = TextLoader("file.txt", encoding="utf-8")
```

## Still Having Issues?

### Check Logs

```python
# Enable verbose mode
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # See what's happening
)

# Enable LangChain debugging
import langchain
langchain.debug = True
```

### Minimal Reproducible Example

```python
# Test with minimal code
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2")
print(llm.invoke("Say 'Hello'"))

# If this works, issue is in your code
# If this fails, issue is with setup
```

### Verify Installation

```bash
# Run test script
python test_setup.py

# Should pass all tests
```

### Clean Install

```bash
# Complete reset
deactivate
rm -rf venv
rm -rf chroma_db

# Start fresh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python test_setup.py
```

## Get More Help

- **LangChain**: https://python.langchain.com/docs/troubleshooting
- **Ollama**: https://github.com/ollama/ollama/issues
- **Check examples**: `examples/` folder has working code
- **Review docs**: Detailed guides in `docs/` folder

## Common Error Messages

| Error | Likely Cause | Solution |
|-------|-------------|----------|
| `Connection refused` | Ollama not running | Run `ollama serve` |
| `Model not found` | Model not installed | Run `ollama pull model-name` |
| `ModuleNotFoundError` | Package not installed | Run `pip install package-name` |
| `Could not parse` | Agent output format wrong | Add `handle_parsing_errors=True` |
| `Timeout` | Query too complex/slow | Increase timeout or use smaller model |
| `Out of memory` | Model too large | Use `llama3.2` instead |
| `API key not found` | Missing .env | Create .env with keys (if using cloud LLMs) |

Remember: Most issues are solved by ensuring Ollama is running and the model is installed!
