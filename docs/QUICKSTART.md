# 🚀 Quick Start Guide

Get up and running with Agentic AI in 10 minutes!

## Prerequisites Check

```bash
# Python installed?
python --version
# Should show 3.10 or higher

# Ollama installed?
ollama --version
```

## Installation Steps

### 1. Setup Python Environment (2 minutes)

```bash
# Navigate to project
cd AgentAI

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### 2. Install Dependencies (3 minutes)

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install packages
pip install -r requirements.txt
```

### 3. Setup Ollama (5 minutes)

```bash
# If Ollama not installed, download from https://ollama.ai

# Start Ollama (if not running)
ollama serve

# Open new terminal, pull model
ollama pull llama3.2

# Verify
ollama list
```

### 4. Test Installation

```bash
# Run test script
python test_setup.py
```

You should see:
```
✓ LangChain installed
✓ Ollama client installed
✓ ChromaDB installed
✓ Ollama connection: Setup successful!

🎉 Setup complete! Ready to start learning.
```

## Run Your First Example

```bash
# Simple chain
python examples/01_basic_chain/simple_chain.py

# Simple agent
python examples/02_simple_agent/react_agent.py

# Custom tools
python examples/02_simple_agent/custom_tools.py
```

## What's Next?

### Option 1: Follow Tutorial (Recommended for beginners)
```bash
# Read docs in order
docs/00_setup.md
docs/01_langchain_basics.md
docs/02_agents.md
docs/03_langgraph.md
docs/04_rag.md
```

### Option 2: Build a Project (Hands-on learners)
```bash
# Document chatbot
cd projects/chatbot
python chatbot.py
```

### Option 3: Explore Examples (Learn by doing)
```bash
# Browse examples folder
examples/01_basic_chain/
examples/02_simple_agent/
examples/05_rag/
```

## Common Issues

### "Ollama not found"
```bash
# Make sure Ollama is installed and running
ollama serve

# In new terminal
ollama list
```

### "Model not found"
```bash
# Pull the model
ollama pull llama3.2
```

### "Import errors"
```bash
# Make sure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "Slow responses"
```bash
# Try smaller model
ollama pull llama3.2

# Or adjust temperature
llm = Ollama(model="llama3.2", temperature=0)
```

## Learning Path

**Week 1**: Basics
- ✓ Setup complete
- □ Run all examples in `01_basic_chain/`
- □ Read `docs/01_langchain_basics.md`
- □ Create your first custom chain

**Week 2**: Agents
- □ Run examples in `02_simple_agent/`
- □ Read `docs/02_agents.md`
- □ Build a custom tool
- □ Create a research agent

**Week 3**: Advanced
- □ Learn LangGraph (`docs/03_langgraph.md`)
- □ Build RAG system (`docs/04_rag.md`)
- □ Complete chatbot project

**Week 4**: Practice
- □ Build 3 custom agents
- □ Create your own project
- □ Share your work!

## Commands Cheat Sheet

```bash
# Activate environment
venv\Scripts\activate

# Deactivate
deactivate

# Install package
pip install package-name

# Update requirements
pip freeze > requirements.txt

# Start Ollama
ollama serve

# List models
ollama list

# Pull model
ollama pull model-name

# Run example
python examples/folder/file.py

# Start Jupyter
jupyter notebook
```

## Get Help

- **Documentation**: Check `docs/` folder
- **Examples**: See `examples/` folder
- **Issues**: Common problems in docs/troubleshooting.md
- **LangChain Docs**: https://python.langchain.com
- **Ollama Docs**: https://ollama.ai

## Project Structure

```
AgentAI/
├── docs/                    # Learn here
│   ├── 00_setup.md
│   ├── 01_langchain_basics.md
│   ├── 02_agents.md
│   ├── 03_langgraph.md
│   └── 04_rag.md
├── examples/                # Practice here
│   ├── 01_basic_chain/
│   ├── 02_simple_agent/
│   └── 05_rag/
├── projects/                # Build here
│   ├── chatbot/
│   ├── research_assistant/
│   └── code_analyzer/
├── requirements.txt         # Dependencies
└── README.md               # Overview
```

## Quick Commands

```bash
# Full setup from scratch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
ollama pull llama3.2
python test_setup.py

# Run first example
python examples/01_basic_chain/simple_chain.py

# Start chatbot project
cd projects/chatbot
python chatbot.py
```

## Success!

You're now ready to build agentic AI systems! 🎉

**Next step**: Open `docs/01_langchain_basics.md` and start learning.

---

**Questions?** Read the docs or check examples for reference implementations.

**Having fun?** Build something cool and share it!
