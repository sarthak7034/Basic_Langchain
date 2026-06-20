"""
ReAct Agent Example
===================
Demonstrates a ReAct (Reasoning + Acting) agent with tools
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
import datetime

# Define custom tools
@tool
def get_current_date() -> str:
    """Returns the current date and time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.
    Examples: "2 + 2", "10 * 5", "(3 + 7) * 2"
    """
    try:
        # Safety check - only allow numbers and basic operators
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def word_counter(text: str) -> str:
    """Count the number of words in a text."""
    words = len(text.split())
    chars = len(text)
    return f"Words: {words}, Characters: {chars}"

def main():
    print("🤖 ReAct Agent Example\n")
    
    # Initialize LLM
    print("📡 Initializing Ollama...")
    llm = Ollama(model="llama3.2", temperature=0)
    
    # Initialize tools
    print("🔧 Setting up tools...")
    search = DuckDuckGoSearchRun()
    
    tools = [
        search,
        get_current_date,
        calculate,
        word_counter,
    ]
    
    # Create ReAct prompt
    prompt = PromptTemplate.from_template("""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
    
    # Create agent
    print("🏗️ Creating ReAct agent...")
    agent = create_react_agent(llm, tools, prompt)
    
    # Create agent executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )
    
    # Example queries
    queries = [
        "What is the current date and time?",
        "Calculate: (15 + 25) * 2",
        "How many words are in this sentence: 'The quick brown fox jumps over the lazy dog'?",
        "Search for the latest news about artificial intelligence",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"Query {i}: {query}")
        print('='*70)
        
        try:
            result = agent_executor.invoke({"input": query})
            print(f"\n✅ Final Answer: {result['output']}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
        
        print()
    
    print("✅ ReAct agent examples completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure Ollama is running: ollama serve")
        print("2. Check model is installed: ollama list")
        print("3. Try pulling model: ollama pull llama3.2")
