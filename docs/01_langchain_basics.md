# LangChain Basics

Learn the fundamental concepts of LangChain for building LLM applications.

## What is LangChain?

LangChain is a framework for developing applications powered by language models. It provides:

1. **Composability** - Chain together LLM calls and other tools
2. **Abstraction** - Consistent interface across different LLMs
3. **Memory** - Maintain conversation state
4. **Tools** - Connect LLMs to external data and APIs
5. **Agents** - Let LLMs decide what actions to take

## Core Components

### 1. LLMs and Chat Models

The foundation of any LangChain application.

```python
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

# Basic LLM
llm = Ollama(model="llama3.2")
response = llm.invoke("What is Python?")
print(response)

# Chat model (maintains conversation format)
chat = ChatOllama(model="llama3.2")
from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="You are a helpful coding assistant."),
    HumanMessage(content="Explain list comprehensions in Python.")
]
response = chat.invoke(messages)
print(response.content)
```

**Key Differences:**
- `LLM`: Simple text-in, text-out
- `ChatModel`: Supports system/user/assistant message format

### 2. Prompt Templates

Reusable prompts with variable placeholders.

```python
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

# Simple template
template = PromptTemplate.from_template(
    "Explain {concept} to a {level} developer in {lines} lines."
)
prompt = template.format(
    concept="decorators",
    level="beginner",
    lines="3"
)

# Chat template
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are an expert in {domain}."),
    ("human", "Explain {topic} with examples."),
])
messages = chat_template.format_messages(
    domain="web development",
    topic="REST APIs"
)
```

**Benefits:**
- Reusability across application
- Type safety with input variables
- Easy testing and modification

### 3. Chains

Sequence multiple steps together.

```python
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser

# Create components
llm = Ollama(model="llama3.2")
prompt = PromptTemplate.from_template("Tell me a joke about {topic}")
output_parser = StrOutputParser()

# Chain them together using LCEL (LangChain Expression Language)
chain = prompt | llm | output_parser

# Invoke
result = chain.invoke({"topic": "programming"})
print(result)
```

**LCEL Benefits:**
- Readable, composable syntax
- Automatic batching and streaming
- Built-in retry and fallback

### 4. Output Parsers

Structure LLM output into usable formats.

```python
from langchain_core.output_parsers import JsonOutputParser, PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

# JSON parser
json_parser = JsonOutputParser()

prompt = PromptTemplate.from_template(
    "List 3 {language} frameworks in JSON format with 'name' and 'use_case' fields.\n{format_instructions}"
)
prompt = prompt.partial(format_instructions=json_parser.get_format_instructions())

chain = prompt | llm | json_parser
result = chain.invoke({"language": "Python"})
# Returns: [{"name": "Django", "use_case": "web"}, ...]

# Pydantic parser (type-safe)
class Framework(BaseModel):
    name: str = Field(description="Framework name")
    use_case: str = Field(description="Primary use case")
    popularity: int = Field(description="Popularity score 1-10")

pydantic_parser = PydanticOutputParser(pydantic_object=Framework)
```

### 5. Memory

Maintain conversation context.

```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain

# Buffer memory (stores all messages)
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

conversation.predict(input="Hi, my name is Alice")
conversation.predict(input="What's my name?")
# LLM will remember: "Your name is Alice"

# Summary memory (for long conversations)
summary_memory = ConversationSummaryMemory(llm=llm)
```

**Memory Types:**
- `ConversationBufferMemory` - Store all messages
- `ConversationBufferWindowMemory` - Keep last N messages
- `ConversationSummaryMemory` - Summarize older messages
- `ConversationKGMemory` - Extract knowledge graph

### 6. Retrieval

Load and query external documents.

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

# Load documents
loader = TextLoader("./data/docs.txt")
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(documents)

# Create embeddings and vector store
embeddings = OllamaEmbeddings(model="llama3.2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings
)

# Query
retriever = vectorstore.as_retriever()
docs = retriever.get_relevant_documents("What is LangChain?")
```

## LangChain Expression Language (LCEL)

Modern way to compose LangChain components.

### Basic Chain
```python
chain = prompt | llm | output_parser
result = chain.invoke({"input": "value"})
```

### Parallel Execution
```python
from langchain_core.runnables import RunnableParallel

# Run multiple chains in parallel
parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain,
    fact=fact_chain
)
result = parallel_chain.invoke({"topic": "AI"})
# Returns: {"joke": "...", "poem": "...", "fact": "..."}
```

### Branching
```python
from langchain_core.runnables import RunnableBranch

# Route based on input
branch = RunnableBranch(
    (lambda x: "code" in x["topic"], code_chain),
    (lambda x: "math" in x["topic"], math_chain),
    general_chain  # default
)
```

### Streaming
```python
for chunk in chain.stream({"topic": "Python"}):
    print(chunk, end="", flush=True)
```

## Best Practices

### 1. Use LCEL Over Legacy Chains
```python
# ❌ Old way
from langchain.chains import LLMChain
chain = LLMChain(llm=llm, prompt=prompt)

# ✅ New way
chain = prompt | llm | output_parser
```

### 2. Type Your Prompts
```python
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict

class Inputs(TypedDict):
    language: str
    concept: str

prompt = ChatPromptTemplate.from_template("Explain {concept} in {language}")
# Type hints help catch errors early
```

### 3. Handle Errors
```python
from langchain_core.runnables import RunnableWithFallbacks

primary_llm = Ollama(model="llama3.2")
fallback_llm = Ollama(model="llama3.2", temperature=0)

chain_with_fallback = RunnableWithFallbacks(
    runnable=primary_llm,
    fallbacks=[fallback_llm]
)
```

### 4. Use Caching
```python
from langchain.cache import InMemoryCache
import langchain

langchain.llm_cache = InMemoryCache()
# Identical prompts return cached results
```

## Common Patterns

### Sequential Processing
```python
# Step 1: Generate ideas
ideas_chain = idea_prompt | llm | output_parser

# Step 2: Evaluate ideas
eval_chain = eval_prompt | llm | json_parser

# Combine
full_chain = ideas_chain | eval_chain
```

### Map-Reduce
```python
from langchain.chains import MapReduceDocumentsChain

# Process each document independently, then combine
map_chain = prompt | llm
reduce_chain = summary_prompt | llm

map_reduce = MapReduceDocumentsChain(
    llm_chain=map_chain,
    reduce_documents_chain=reduce_chain
)
```

### Question-Answering
```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # "stuff", "map_reduce", "refine"
    retriever=vectorstore.as_retriever()
)

answer = qa_chain.invoke({"query": "What is LangChain?"})
```

## Debugging

### Enable Verbose Mode
```python
chain = prompt | llm | output_parser
chain.invoke({"input": "test"}, config={"verbose": True})
```

### Use LangSmith
```python
import os
os.environ["LANGSMITH_TRACING_V2"] = "true"
os.environ["LANGSMITH_PROJECT"] = "my-project"
# Automatically logs all chains to LangSmith
```

### Inspect Intermediate Steps
```python
from langchain_core.runnables import RunnablePassthrough

chain = (
    RunnablePassthrough.assign(step1=lambda x: print(f"Input: {x}") or x)
    | prompt
    | RunnablePassthrough.assign(step2=lambda x: print(f"Prompt: {x}") or x)
    | llm
)
```

## Next Steps

Now that you understand the basics:
1. [Build Your First Agent](02_agents.md)
2. [Try the examples](../examples/01_basic_chain/)
3. [Read LangChain docs](https://python.langchain.com/)

## Key Takeaways

✅ **LangChain provides composable building blocks for LLM apps**  
✅ **LCEL is the modern way to chain components**  
✅ **Prompts, memory, and retrieval are essential patterns**  
✅ **Start simple, add complexity as needed**
