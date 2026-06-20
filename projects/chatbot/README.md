# Document Chatbot Project

Build a chatbot that can answer questions about your documents using RAG.

## Features

- 📄 Upload and process documents (TXT, PDF, DOCX)
- 💬 Conversational interface
- 🔍 Retrieves relevant context
- 📚 Cites sources
- 💾 Persistent vector store
- 🌐 Web UI with Streamlit

## Quick Start

```bash
# Navigate to project directory
cd projects/chatbot

# Run the chatbot
python app.py

# Or use Streamlit UI
streamlit run streamlit_app.py
```

## Project Structure

```
chatbot/
├── app.py              # Main CLI application
├── streamlit_app.py    # Web UI
├── chatbot.py          # Core chatbot logic
├── utils.py            # Helper functions
├── data/               # Place documents here
└── chroma_db/          # Vector store (created automatically)
```

## Usage

### 1. Add Documents

Place your documents in the `data/` folder:
```
data/
├── manual.pdf
├── faq.txt
└── guide.docx
```

### 2. Run Chatbot

```bash
python app.py
```

### 3. Ask Questions

```
You: What is covered in the manual?
Bot: Based on the documents, the manual covers...

You: How do I get started?
Bot: According to the guide...
```

## Configuration

Edit `config.yaml`:

```yaml
model:
  name: llama3.2
  temperature: 0

retrieval:
  chunk_size: 1000
  chunk_overlap: 200
  k: 4

vectorstore:
  persist_directory: ./chroma_db
```

## Customization

### Change LLM Model

```python
# In chatbot.py
llm = Ollama(model="llama3.1:8b")  # Use larger model
```

### Adjust Retrieval

```python
# More context
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

# Smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
```

### Custom Prompts

```python
template = """You are a helpful assistant. Answer based on the context.

Context: {context}

Question: {question}

Answer in a friendly, conversational tone:"""
```

## Features to Add

- [ ] Multi-language support
- [ ] Export conversation history
- [ ] Document upload via UI
- [ ] Advanced filtering
- [ ] Feedback collection

## Troubleshooting

**Documents not loading?**
- Check file format (TXT, PDF, DOCX)
- Verify files are in `data/` folder
- Check file encoding (use UTF-8)

**Poor answers?**
- Adjust chunk size
- Increase retrieval k
- Improve document quality
- Try different model

**Slow responses?**
- Reduce k
- Use smaller model
- Optimize chunk count

## Next Steps

1. Add your documents
2. Test with different questions
3. Tune parameters for your use case
4. Deploy to production

See [RAG Documentation](../../docs/04_rag.md) for more details.
