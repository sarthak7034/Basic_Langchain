"""
Chat Model Example
==================
Using chat models with system and user messages
"""

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

def main():
    print("💬 Chat Model Example\n")
    
    # Initialize chat model
    print("📡 Connecting to Ollama chat model...")
    chat = ChatOllama(model="llama3.2", temperature=0.7)
    
    # Example 1: Simple chat with system message
    print("\n📚 Example 1: Code Review Assistant")
    print("-" * 50)
    
    messages = [
        SystemMessage(content="You are an expert code reviewer. Be concise and helpful."),
        HumanMessage(content="Review this Python code: def calc(x,y): return x+y")
    ]
    
    response = chat.invoke(messages)
    print(f"Assistant: {response.content}")
    
    # Example 2: Multi-turn conversation
    print("\n📚 Example 2: Conversation History")
    print("-" * 50)
    
    conversation = [
        SystemMessage(content="You are a helpful Python tutor."),
        HumanMessage(content="What is a lambda function?"),
    ]
    
    # First exchange
    response1 = chat.invoke(conversation)
    print(f"User: What is a lambda function?")
    print(f"Assistant: {response1.content}")
    
    # Add to conversation history
    conversation.append(AIMessage(content=response1.content))
    conversation.append(HumanMessage(content="Can you show me an example?"))
    
    # Second exchange
    response2 = chat.invoke(conversation)
    print(f"\nUser: Can you show me an example?")
    print(f"Assistant: {response2.content}")
    
    # Example 3: Different system prompts
    print("\n📚 Example 3: Personality Change")
    print("-" * 50)
    
    question = "What is recursion?"
    
    # Friendly tutor
    friendly = chat.invoke([
        SystemMessage(content="You are a friendly, encouraging teacher. Use emojis and simple language."),
        HumanMessage(content=question)
    ])
    print(f"Friendly tutor: {friendly.content}")
    
    print()
    
    # Technical expert
    technical = chat.invoke([
        SystemMessage(content="You are a technical expert. Be precise and formal."),
        HumanMessage(content=question)
    ])
    print(f"Technical expert: {technical.content}")
    
    print("\n✅ Chat model example completed!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure Ollama is running with llama3.2 model installed.")
