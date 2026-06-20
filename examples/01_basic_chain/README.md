# Basic Chain Examples

Learn the fundamentals of LangChain chains and LLM interactions.

## Files

- `simple_chain.py` - Basic chain using LCEL syntax
- `chat_model.py` - Using chat models with message history
- `streaming.py` - Stream responses in real-time
- `output_parser.py` - Structure LLM outputs

## Prerequisites

```bash
# Make sure Ollama is running
ollama serve

# Pull the model
ollama pull llama3.2

# Activate virtual environment
venv\Scripts\activate

# Install dependencies (if not done)
pip install -r ../../requirements.txt
```

## Run Examples

```bash
# Basic chain
python simple_chain.py

# Chat model
python chat_model.py

# Streaming
python streaming.py

# Output parsers
python output_parser.py
```

## What You'll Learn

1. **LCEL Syntax** - Modern chain composition with pipe operator
2. **Prompt Templates** - Reusable prompts with variables
3. **Chat vs LLM Models** - When to use each
4. **Output Parsing** - Structure LLM responses
5. **Streaming** - Real-time response generation

## Key Concepts

### LCEL (LangChain Expression Language)
```python
chain = prompt | llm | output_parser
result = chain.invoke({"input": "value"})
```

### Prompt Templates
```python
template = PromptTemplate.from_template("Explain {topic} in {style}")
```

### Chat Messages
```python
messages = [
    SystemMessage(content="You are a helpful assistant"),
    HumanMessage(content="Hello!")
]
```

## Next Steps

After completing these examples:
- Try [Simple Agent](../02_simple_agent/) examples
- Read [LangChain Basics](../../docs/01_langchain_basics.md) documentation
- Experiment with different prompts and models
