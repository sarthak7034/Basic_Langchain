# RAG: Retrieval Augmented Generation

Learn how to build systems that can answer questions about your documents.

## What is RAG?

**RAG (Retrieval Augmented Generation)** combines:
1. **Retrieval** - Find relevant information from documents
2. **Generation** - Use LLM to generate answers based on retrieved context

This lets LLMs answer questions about information they weren't trained on.

## Why Use RAG?

✅ **Ground LLM responses in your data**  
✅ **Reduce hallucinations**  
✅ **Keep information up-to-date without retraining**  
✅ **Add citations and sources**  
✅ **Work with private/proprietary data**

## Basic RAG Architecture

```
Documents → Split → Embed → Store in Vector DB
                                    ↓
Query → Embed → Retrieve Similar → LLM → Answer
```

## Step-by-Step RAG Implementation

### 1. Load Documents

```python
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
)

# Load single file
loader = TextLoader("./data/document.txt")
documents = loader.load()

# Load PDF
pdf_loader = PyPDFLoader("./data/report.pdf")
pdf_docs = pdf_loader.load()

# Load entire directory
dir_loader = DirectoryLoader(
    "./data/",
    glob="**/*.txt",
    show_progress=True
)
all_docs = dir_loader.load()
```

### 2. Split Documents

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,        # Characters per chunk
    chunk_overlap=200,      # Overlap between chunks
    length_function=len,
    separators=["\n\n", "\n", " ", ""]
)

splits = text_splitter.split_documents(documents)
print(f"Split into {len(splits)} chunks")
```

**Why Split?**
- LLMs have context limits
- Smaller chunks = more precise retrieval
- Overlap preserves context across boundaries

### 3. Create Embeddings

```python
from langchain_community.embeddings import OllamaEmbeddings

# Using local Ollama (free)
embeddings = OllamaEmbeddings(
    model="llama3.2",
    base_url="http://localhost:11434"
)

# Test embeddings
vector = embeddings.embed_query("Hello world")
print(f"Embedding dimension: {len(vector)}")
```

### 4. Store in Vector Database

```python
from langchain_community.vectorstores import Chroma

# Create vector store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"  # Save to disk
)

# Or load existing
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)
```

### 5. Retrieve Documents

```python
# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}  # Return top 4 results
)

# Query
docs = retriever.get_relevant_documents("What is LangChain?")
for doc in docs:
    print(f"Content: {doc.page_content[:100]}...")
    print(f"Source: {doc.metadata}")
```

### 6. Generate Answer

```python
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

llm = Ollama(model="llama3.2", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain.invoke({"query": "What is RAG?"})
print(f"Answer: {result['result']}")
print(f"Sources: {result['source_documents']}")
```

## Complete RAG Example

```python
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama

def build_rag_system(docs_path: str):
    """Build complete RAG system."""
    
    # 1. Load documents
    loader = TextLoader(docs_path)
    documents = loader.load()
    
    # 2. Split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(documents)
    
    # 3. Create embeddings
    embeddings = OllamaEmbeddings(model="llama3.2")
    
    # 4. Create vector store
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings
    )
    
    # 5. Create retriever
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 6. Create QA chain
    llm = Ollama(model="llama3.2", temperature=0)
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    
    return qa_chain

# Use it
qa = build_rag_system("./data/docs.txt")
result = qa.invoke({"query": "What is the main topic?"})
print(result['result'])
```

## Advanced RAG Patterns

### 1. Conversational RAG

```python
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

conversational_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True
)

# Multi-turn conversation
result1 = conversational_chain({"question": "What is RAG?"})
result2 = conversational_chain({"question": "How does it work?"})
# Chain remembers context
```

### 2. Custom Prompts

```python
from langchain_core.prompts import PromptTemplate

template = """Use the following context to answer the question. 
If you don't know, say "I don't have enough information."

Context: {context}

Question: {question}

Answer: Let me help you with that."""

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)
```

### 3. Multiple Retrievers

```python
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever

# Semantic retriever (vector-based)
semantic_retriever = vectorstore.as_retriever()

# Keyword retriever (BM25)
keyword_retriever = BM25Retriever.from_documents(splits)

# Combine both
ensemble_retriever = EnsembleRetriever(
    retrievers=[semantic_retriever, keyword_retriever],
    weights=[0.5, 0.5]  # Equal weight
)
```

### 4. Re-ranking

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Create compressor
compressor = LLMChainExtractor.from_llm(llm)

# Wrap retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=retriever
)

# Returns only relevant parts of documents
docs = compression_retriever.get_relevant_documents("query")
```

### 5. Parent Document Retriever

```python
from langchain.retrievers import ParentDocumentRetriever
from langchain.storage import InMemoryStore

# Store for parent documents
store = InMemoryStore()

# Retrieve small chunks, return full parent documents
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=small_splitter,
    parent_splitter=large_splitter
)
```

## RAG Chain Types

### 1. Stuff (Default)
Put all context in one prompt.

```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Simple, works for small contexts
    retriever=retriever
)
```

**Use when**: Small number of documents, fast responses needed

### 2. Map Reduce
Process each document separately, then combine.

```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_reduce",  # Scalable, parallel
    retriever=retriever
)
```

**Use when**: Many documents, can parallelize

### 3. Refine
Iteratively update answer with each document.

```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="refine",  # More nuanced answers
    retriever=retriever
)
```

**Use when**: Need comprehensive analysis

### 4. Map Rerank
Score each answer, return best.

```python
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="map_rerank",  # Most relevant answer
    retriever=retriever
)
```

**Use when**: Need confidence scores

## Vector Databases

### ChromaDB (Default - Easy)

```python
from langchain_community.vectorstores import Chroma

vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
```

### FAISS (Fast)

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(splits, embeddings)

# Save
vectorstore.save_local("faiss_index")

# Load
vectorstore = FAISS.load_local("faiss_index", embeddings)
```

### Pinecone (Cloud, Scalable)

```python
from langchain_community.vectorstores import Pinecone
import pinecone

pinecone.init(api_key="your-key", environment="us-east-1")
vectorstore = Pinecone.from_documents(splits, embeddings, index_name="my-index")
```

## Optimizing RAG

### 1. Chunk Size

```python
# Small chunks (200-500): More precise, but may lack context
# Large chunks (1000-2000): More context, but less precise

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200  # 10-20% of chunk size
)
```

### 2. Retrieval K

```python
# k = 3-5: Fast, focused
# k = 10+: Comprehensive, slower

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
```

### 3. Embedding Models

```python
# Small, fast
embeddings = OllamaEmbeddings(model="llama3.2")

# Larger, more accurate
from sentence_transformers import SentenceTransformer
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
```

### 4. Metadata Filtering

```python
# Add metadata during ingestion
splits[0].metadata["source"] = "document1.pdf"
splits[0].metadata["date"] = "2024-01-01"

# Filter during retrieval
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "filter": {"source": "document1.pdf"}
    }
)
```

## Best Practices

### 1. Evaluate Retrieval Quality

```python
# Check what's being retrieved
docs = retriever.get_relevant_documents("test query")
for i, doc in enumerate(docs):
    print(f"\n{i+1}. {doc.page_content[:200]}...")
```

### 2. Add Citations

```python
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain.invoke({"query": "question"})
print(f"Answer: {result['result']}")
print("\nSources:")
for doc in result['source_documents']:
    print(f"- {doc.metadata.get('source', 'Unknown')}")
```

### 3. Handle "I Don't Know"

```python
template = """Answer based on the context. If the context doesn't contain 
the answer, say "I don't have that information in the documents."

Context: {context}
Question: {question}
Answer:"""
```

### 4. Clean Documents

```python
def clean_text(text: str) -> str:
    """Clean text before embedding."""
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove special characters if needed
    # ...
    return text

documents = [clean_text(doc.page_content) for doc in documents]
```

## Common Issues

### Issue: Poor Retrieval

**Solution**: Adjust chunk size, try different embeddings

### Issue: Out of Context

**Solution**: Increase k, use larger chunks, try map_reduce

### Issue: Slow Queries

**Solution**: Reduce k, use FAISS, optimize chunk count

### Issue: Hallucinations

**Solution**: Improve prompts, add "I don't know" handling, increase context

## Next Steps

- [Production Tips](05_production.md)
- [Try RAG examples](../examples/05_rag/)
- [Build a chatbot](../projects/chatbot/)

## Key Takeaways

✅ **RAG = Retrieval + Generation**  
✅ **Load → Split → Embed → Store → Retrieve → Generate**  
✅ **Chunk size and overlap matter**  
✅ **Different chain types for different needs**  
✅ **Always evaluate and iterate**
