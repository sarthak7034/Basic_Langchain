# Setup Guide

Complete setup instructions for the Agentic AI Learning Project.

## System Requirements

- **OS**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Python**: 3.10 or higher
- **Internet**: Required for initial downloads

## Step 1: Install Python

### Windows
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer, check "Add Python to PATH"
3. Verify: `python --version`

### macOS
```bash
# Using Homebrew
brew install python@3.11

# Verify
python3 --version
```

### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.11 python3-pip python3-venv

# Verify
python3 --version
```

## Step 2: Install Ollama (Local LLM Runtime)

Ollama lets you run large language models locally for free.

### Windows
1. Visit [ollama.ai](https://ollama.ai)
2. Download Ollama for Windows
3. Run the installer
4. Verify: Open terminal and run `ollama --version`

### macOS
```bash
# Download and install
curl -fsSL https://ollama.ai/install.sh | sh

# Or use Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Verify Ollama Installation
```bash
# Start Ollama (if not running)
ollama serve

# In a new terminal, pull a model
ollama pull llama3.2

# Test it
ollama run llama3.2 "Hello! Explain what you are in one sentence."
```

## Step 3: Setup Project

### Clone or Create Directory
```bash
# Navigate to your workspace
cd c:\Users\sarth\OneDrive\Desktop\AgentAI

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Install Dependencies
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

This will take 5-10 minutes.

## Step 4: Configure Environment

```bash
# Copy the example environment file
copy .env.example .env

# Edit .env with your preferred text editor
notepad .env
```

Basic configuration (free, local-only):
```env
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.2
```

## Step 5: Download Models

### Recommended Models for Learning

```bash
# Small, fast model (good for testing)
ollama pull llama3.2

# Larger, more capable model
ollama pull llama3.1:8b

# Code-specialized model
ollama pull codellama

# List installed models
ollama list
```

### Model Size Guide
- `llama3.2` (2B params): ~1.5GB, fastest, good for learning
- `llama3.1:8b` (8B params): ~4.7GB, balanced
- `llama3:70b` (70B params): ~40GB, most capable (requires powerful hardware)

## Step 6: Verify Installation

Create a test script:

```python
# test_setup.py
import sys
print(f"Python version: {sys.version}")

try:
    import langchain
    print(f"✓ LangChain installed: {langchain.__version__}")
except ImportError:
    print("✗ LangChain not found")

try:
    import ollama
    print(f"✓ Ollama client installed")
except ImportError:
    print("✗ Ollama client not found")

try:
    import chromadb
    print(f"✓ ChromaDB installed")
except ImportError:
    print("✗ ChromaDB not found")

try:
    from langchain_community.llms import Ollama
    llm = Ollama(model="llama3.2")
    response = llm.invoke("Say 'Setup successful!' and nothing else.")
    print(f"✓ Ollama connection: {response.strip()}")
except Exception as e:
    print(f"✗ Ollama connection failed: {e}")

print("\n🎉 Setup complete! Ready to start learning.")
```

Run the test:
```bash
python test_setup.py
```

## Optional: LangSmith Setup

LangSmith provides monitoring and debugging for agents (free tier available).

1. Visit [smith.langchain.com](https://smith.langchain.com)
2. Create a free account
3. Get your API key
4. Add to `.env`:
```env
LANGSMITH_API_KEY=your-key-here
LANGSMITH_PROJECT=agentic-ai-learning
LANGSMITH_TRACING_V2=true
```

## Optional: Cloud LLM Providers

For comparison with cloud models:

### OpenAI
1. Get API key from [platform.openai.com](https://platform.openai.com)
2. Add to `.env`: `OPENAI_API_KEY=sk-...`

### Anthropic (Claude)
1. Get API key from [console.anthropic.com](https://console.anthropic.com)
2. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-...`

## Troubleshooting

### Ollama Not Running
```bash
# Windows: Start Ollama from Start Menu
# Or in terminal:
ollama serve
```

### Port Already in Use
```bash
# Check what's using port 11434
netstat -ano | findstr :11434

# Change Ollama port
set OLLAMA_HOST=0.0.0.0:11435
```

### Python Package Conflicts
```bash
# Create fresh environment
deactivate
rm -rf venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Model Download Fails
```bash
# Check Ollama is running
ollama list

# Try pulling again
ollama pull llama3.2

# Check available disk space
```

## Next Steps

Setup complete! Continue to:
- [LangChain Basics](01_langchain_basics.md) - Learn the fundamentals
- [Run First Example](../examples/01_basic_chain/README.md) - Try your first chain

## Quick Reference

```bash
# Activate environment
venv\Scripts\activate

# Start Ollama
ollama serve

# List models
ollama list

# Run example
python examples/01_basic_chain/simple_chain.py

# Start Jupyter
jupyter notebook

# Deactivate environment
deactivate
```
