"""
Setup Test Script
=================
Verifies that all components are properly installed and configured.
"""

import sys
import os

def test_python_version():
    """Test Python version."""
    print("🐍 Python version:", sys.version.split()[0])
    major, minor = sys.version_info[:2]
    
    if major == 3 and minor >= 10:
        print("✅ Python version OK (3.10+)")
        return True
    else:
        print("❌ Python 3.10+ required")
        return False

def test_langchain():
    """Test LangChain installation."""
    try:
        import langchain
        print(f"✅ LangChain installed: {langchain.__version__}")
        return True
    except ImportError as e:
        print(f"❌ LangChain not found: {e}")
        return False

def test_ollama_client():
    """Test Ollama Python client."""
    try:
        import ollama
        print("✅ Ollama client installed")
        return True
    except ImportError as e:
        print(f"❌ Ollama client not found: {e}")
        return False

def test_chromadb():
    """Test ChromaDB installation."""
    try:
        import chromadb
        print("✅ ChromaDB installed")
        return True
    except ImportError as e:
        print(f"❌ ChromaDB not found: {e}")
        return False

def test_streamlit():
    """Test Streamlit installation."""
    try:
        import streamlit
        print(f"✅ Streamlit installed")
        return True
    except ImportError as e:
        print(f"⚠️  Streamlit not found (optional): {e}")
        return True  # Optional, don't fail

def test_ollama_connection():
    """Test Ollama server connection."""
    try:
        from langchain_community.llms import Ollama
        print("\n🔌 Testing Ollama connection...")
        
        llm = Ollama(model="llama3.2", base_url="http://localhost:11434")
        response = llm.invoke("Say 'Setup successful!' and nothing else.", timeout=30)
        
        print(f"✅ Ollama connected: {response.strip()}")
        return True
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check Ollama is running: ollama serve")
        print("   2. Verify model installed: ollama list")
        print("   3. Pull model if needed: ollama pull llama3.2")
        return False

def test_environment():
    """Test environment configuration."""
    print("\n📁 Checking environment...")
    
    # Check if .env exists
    if os.path.exists(".env"):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (optional)")
        print("   Copy .env.example to .env if needed")
    
    # Check if virtual environment is active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment active")
    else:
        print("⚠️  Virtual environment not detected")
        print("   Recommended: python -m venv venv && venv\\Scripts\\activate")
    
    return True

def test_directories():
    """Test required directories."""
    print("\n📂 Checking project structure...")
    
    required = ['docs', 'examples', 'projects']
    optional = ['data', 'chroma_db']
    
    for dir_name in required:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ found")
        else:
            print(f"❌ {dir_name}/ missing")
    
    for dir_name in optional:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ found (optional)")
    
    return True

def main():
    """Run all tests."""
    print("=" * 70)
    print("🧪 Testing AgentAI Setup")
    print("=" * 70)
    print()
    
    results = []
    
    # Core tests
    print("📦 Testing Package Installations")
    print("-" * 70)
    results.append(test_python_version())
    results.append(test_langchain())
    results.append(test_ollama_client())
    results.append(test_chromadb())
    results.append(test_streamlit())
    
    # Environment tests
    results.append(test_environment())
    results.append(test_directories())
    
    # Connection test
    print()
    results.append(test_ollama_connection())
    
    # Summary
    print("\n" + "=" * 70)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print("🎉 All tests passed! Setup complete!")
        print("\n✨ Next steps:")
        print("   1. Read QUICKSTART.md for quick start guide")
        print("   2. Run: python examples/01_basic_chain/simple_chain.py")
        print("   3. Explore docs/ folder for tutorials")
        return 0
    else:
        print(f"⚠️  {passed}/{total} tests passed")
        print("\n🔧 Please fix the issues above before continuing")
        print("   Check docs/00_setup.md for detailed setup instructions")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
