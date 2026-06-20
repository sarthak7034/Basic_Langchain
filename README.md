# Agentic AI Learning Project with LangChain

A comprehensive, free, and local learning resource for building agentic AI systems using the LangChain ecosystem.

## 🎯 Project Overview

This project provides hands-on examples and tutorials for learning agentic AI development from beginner to intermediate level. All examples run locally and use free models and tools.

## 📚 What You'll Learn

1. **LangChain Fundamentals** - Core concepts, chains, and prompts
2. **Agent Architecture** - ReAct, function calling, and tool usage
3. **LangGraph** - Building stateful, multi-step agents
4. **LangSmith** - Debugging and monitoring agents (optional)
5. **RAG Systems** - Retrieval Augmented Generation
6. **Multi-Agent Systems** - Coordinating multiple agents

## 🛠️ Tech Stack

- **Python 3.10+** - Primary language
- **LangChain** - Agent framework
- **LangGraph** - State machine for complex agents
- **Ollama** - Local LLM runtime (free)
- **ChromaDB** - Vector database
- **Streamlit** - UI for demos
- **FastAPI** - API endpoints (optional)

## 📋 Prerequisites

- Basic Python knowledge
- Understanding of APIs and JSON
- Familiarity with command line
- 8GB+ RAM (16GB recommended for larger models)

## 🚀 Quick Start

```bash
# 1. Clone/navigate to this directory
cd AgentAI

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Ollama (for local LLMs)
# Visit https://ollama.ai and download for your OS

# 5. Pull a model
ollama pull llama3.2

# 6. Run your first example
python examples/01_basic_chain/simple_chain.py
```

## 📖 Learning Path

### Week 1: Foundations
- [ ] Setup environment
- [ ] Understand LLM basics
- [ ] Create your first chain
- [ ] Work with prompts and templates

### Week 2: Basic Agents
- [ ] Build a ReAct agent
- [ ] Create custom tools
- [ ] Handle agent memory
- [ ] Debug agent reasoning

### Week 3: Advanced Patterns
- [ ] Implement RAG system
- [ ] Build multi-step workflows
- [ ] Create conversational agents
- [ ] Add error handling

### Week 4: Production Concepts
- [ ] LangGraph state machines
- [ ] Agent orchestration
- [ ] Monitoring and logging
- [ ] Performance optimization

## 📁 Project Structure

```
AgentAI/
├── docs/                    # Detailed documentation
│   ├── 00_setup.md         # Environment setup
│   ├── 01_langchain_basics.md
│   ├── 02_agents.md
│   ├── 03_langgraph.md
│   ├── 04_rag.md
│   └── 05_production.md
├── examples/               # Hands-on examples
│   ├── 01_basic_chain/
│   ├── 02_simple_agent/
│   ├── 03_tools/
│   ├── 04_memory/
│   ├── 05_rag/
│   ├── 06_langgraph/
│   └── 07_multi_agent/
├── projects/              # Practice projects
│   ├── chatbot/
│   ├── research_assistant/
│   └── code_analyzer/
├── tests/                 # Test files
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

Create a `.env` file for configuration:

```env
# Optional: Use OpenAI/Anthropic for comparison
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Local model settings
OLLAMA_BASE_URL=http://localhost:11434
DEFAULT_MODEL=llama3.2
```

## 💡 Example Projects

1. **Personal Assistant** - Task management and reminders
2. **Research Assistant** - Web search and summarization
3. **Code Analyzer** - Code review and suggestions
4. **Document Q&A** - RAG-based document chatbot
5. **Multi-Agent System** - Coordinated agent workflows

## 🔗 Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Ollama Models](https://ollama.ai/library)
- [LangSmith](https://smith.langchain.com/)

## 🤝 Contributing

This is a learning project. Feel free to:
- Add new examples
- Improve documentation
- Share your projects
- Report issues

## 📝 License

MIT License - Free to use for learning and commercial purposes

## 🆘 Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues and solutions.

---

**Ready to start?** Head to [docs/00_setup.md](docs/00_setup.md) for detailed setup instructions!
