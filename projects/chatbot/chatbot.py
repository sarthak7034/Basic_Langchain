"""
Document Chatbot with RAG
=========================
Core chatbot implementation using Retrieval Augmented Generation
"""

import os
from typing import List, Dict
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    DirectoryLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.llms import Ollama
from langchain.memory import ConversationBufferMemory

class DocumentChatbot:
    """RAG-based chatbot for document Q&A."""
    
    def __init__(
        self,
        data_dir: str = "./data",
        persist_dir: str = "./chroma_db",
        model: str = "llama3.2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        k: int = 4
    ):
        """
        Initialize the chatbot.
        
        Args:
            data_dir: Directory containing documents
            persist_dir: Directory to store vector database
            model: Ollama model name
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
            k: Number of documents to retrieve
        """
        self.data_dir = data_dir
        self.persist_dir = persist_dir
        self.model = model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.k = k
        
        self.vectorstore = None
        self.chain = None
        self.memory = None
        
    def load_documents(self) -> List:
        """Load documents from data directory."""
        print(f"📂 Loading documents from {self.data_dir}...")
        
        documents = []
        
        # Load text files
        try:
            text_loader = DirectoryLoader(
                self.data_dir,
                glob="**/*.txt",
                loader_cls=TextLoader,
                show_progress=True
            )
            documents.extend(text_loader.load())
        except Exception as e:
            print(f"  ⚠️ Error loading text files: {e}")
        
        # Load PDFs
        try:
            pdf_files = [f for f in os.listdir(self.data_dir) if f.endswith('.pdf')]
            for pdf_file in pdf_files:
                pdf_path = os.path.join(self.data_dir, pdf_file)
                pdf_loader = PyPDFLoader(pdf_path)
                documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"  ⚠️ Error loading PDF files: {e}")
        
        print(f"✅ Loaded {len(documents)} documents")
        return documents
    
    def split_documents(self, documents: List) -> List:
        """Split documents into chunks."""
        print("✂️ Splitting documents...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )
        
        splits = text_splitter.split_documents(documents)
        print(f"✅ Created {len(splits)} chunks")
        return splits
    
    def create_vectorstore(self, splits: List):
        """Create vector store from document splits."""
        print("🔢 Creating embeddings and vector store...")
        
        embeddings = OllamaEmbeddings(
            model=self.model,
            base_url="http://localhost:11434"
        )
        
        self.vectorstore = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=self.persist_dir
        )
        
        print(f"✅ Vector store created at {self.persist_dir}")
    
    def load_vectorstore(self):
        """Load existing vector store."""
        print(f"📂 Loading vector store from {self.persist_dir}...")
        
        embeddings = OllamaEmbeddings(
            model=self.model,
            base_url="http://localhost:11434"
        )
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=embeddings
        )
        
        print("✅ Vector store loaded")
    
    def initialize_chain(self):
        """Initialize the conversational chain."""
        print("🔗 Setting up conversation chain...")
        
        llm = Ollama(
            model=self.model,
            temperature=0,
            base_url="http://localhost:11434"
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": self.k}
        )
        
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            verbose=False
        )
        
        print("✅ Chain initialized")
    
    def setup(self, force_rebuild: bool = False):
        """
        Setup the chatbot.
        
        Args:
            force_rebuild: Force rebuilding vector store even if it exists
        """
        # Check if vector store exists
        if os.path.exists(self.persist_dir) and not force_rebuild:
            print("ℹ️ Found existing vector store")
            self.load_vectorstore()
        else:
            # Create new vector store
            if not os.path.exists(self.data_dir):
                raise ValueError(f"Data directory not found: {self.data_dir}")
            
            documents = self.load_documents()
            if not documents:
                raise ValueError(f"No documents found in {self.data_dir}")
            
            splits = self.split_documents(documents)
            self.create_vectorstore(splits)
        
        self.initialize_chain()
        print("✅ Chatbot ready!")
    
    def ask(self, question: str) -> Dict:
        """
        Ask a question to the chatbot.
        
        Args:
            question: User question
            
        Returns:
            Dict with 'answer' and 'sources'
        """
        if not self.chain:
            raise ValueError("Chatbot not initialized. Call setup() first.")
        
        result = self.chain.invoke({"question": question})
        
        return {
            "answer": result["answer"],
            "sources": result.get("source_documents", [])
        }
    
    def reset_conversation(self):
        """Reset conversation history."""
        if self.memory:
            self.memory.clear()
            print("🔄 Conversation reset")
    
    def get_stats(self) -> Dict:
        """Get chatbot statistics."""
        stats = {
            "model": self.model,
            "chunk_size": self.chunk_size,
            "retrieval_k": self.k,
        }
        
        if self.vectorstore:
            # Try to get collection count
            try:
                collection = self.vectorstore._collection
                stats["document_count"] = collection.count()
            except:
                stats["document_count"] = "Unknown"
        
        return stats

def main():
    """Example usage."""
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Create sample document
    sample_doc = """
    LangChain is a framework for developing applications powered by language models.
    
    Key Features:
    - Chains: Link multiple LLM calls together
    - Agents: Let LLMs make decisions about which tools to use
    - Memory: Maintain state across conversations
    - Retrieval: Connect to external data sources
    
    LangGraph extends LangChain with graph-based workflows for complex agents.
    """
    
    with open("./data/sample.txt", "w") as f:
        f.write(sample_doc)
    
    print("=" * 70)
    print("Document Chatbot Example")
    print("=" * 70)
    
    # Initialize chatbot
    bot = DocumentChatbot()
    bot.setup()
    
    # Print stats
    stats = bot.get_stats()
    print(f"\n📊 Stats: {stats}")
    
    # Example questions
    questions = [
        "What is LangChain?",
        "What are the key features?",
        "What is LangGraph?",
    ]
    
    print("\n" + "=" * 70)
    print("Example Questions")
    print("=" * 70)
    
    for question in questions:
        print(f"\n❓ Question: {question}")
        result = bot.ask(question)
        print(f"💬 Answer: {result['answer']}")
        
        if result['sources']:
            print(f"\n📚 Sources ({len(result['sources'])}):")
            for i, doc in enumerate(result['sources'][:2], 1):
                preview = doc.page_content[:100].replace('\n', ' ')
                print(f"  {i}. {preview}...")
    
    print("\n✅ Example completed!")

if __name__ == "__main__":
    main()
