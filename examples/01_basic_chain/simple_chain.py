"""
Simple Chain Example
====================
Demonstrates basic LangChain chain using LCEL (LangChain Expression Language)
"""

from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def main():
    print("🔗 Simple Chain Example\n")
    
    # Initialize Ollama LLM
    print("📡 Connecting to Ollama...")
    llm = Ollama(model="llama3.2", temperature=0.7)
    
    # Create a prompt template
    prompt = PromptTemplate.from_template(
        "Explain {concept} to a {level} developer in {lines} lines or less."
    )
    
    # Create output parser
    output_parser = StrOutputParser()
    
    # Chain them together using LCEL (pipe operator)
    chain = prompt | llm | output_parser
    
    # Example 1: Explain decorators
    print("\n📚 Example 1: Python Decorators")
    print("-" * 50)
    result = chain.invoke({
        "concept": "Python decorators",
        "level": "beginner",
        "lines": "3"
    })
    print(result)
    
    # Example 2: Explain async/await
    print("\n📚 Example 2: Async/Await")
    print("-" * 50)
    result = chain.invoke({
        "concept": "async/await in Python",
        "level": "intermediate",
        "lines": "5"
    })
    print(result)
    
    # Example 3: Multiple invocations
    print("\n📚 Example 3: Batch Processing")
    print("-" * 50)
    concepts = [
        {"concept": "list comprehensions", "level": "beginner", "lines": "2"},
        {"concept": "context managers", "level": "intermediate", "lines": "3"},
    ]
    
    for item in concepts:
        result = chain.invoke(item)
        print(f"\n{item['concept'].title()}:")
        print(result)
    
    print("\n✅ Chain example completed!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is running (run 'ollama serve' in terminal)")
        print("2. llama3.2 model is installed (run 'ollama pull llama3.2')")
