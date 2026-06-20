"""
Custom Tools Example
====================
Creating and using custom tools with agents
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.llms import Ollama
from langchain.tools import BaseTool, tool
from langchain_core.prompts import PromptTemplate
from typing import Optional
from pydantic import Field
import json
import random

# Method 1: Using @tool decorator
@tool
def flip_coin() -> str:
    """Flip a coin and return heads or tails."""
    return random.choice(["Heads", "Tails"])

@tool
def roll_dice(sides: int = 6) -> str:
    """
    Roll a dice with specified number of sides.
    
    Args:
        sides: Number of sides on the dice (default: 6)
    """
    result = random.randint(1, sides)
    return f"Rolled a {sides}-sided dice: {result}"

@tool
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]

# Method 2: Using BaseTool class
class TextStatsTool(BaseTool):
    name: str = "text_statistics"
    description: str = """
    Analyze text and return statistics including:
    - Word count
    - Character count
    - Sentence count
    - Average word length
    
    Input should be a text string.
    """
    
    def _run(self, text: str) -> str:
        """Execute the tool."""
        words = text.split()
        sentences = text.count('.') + text.count('!') + text.count('?')
        
        stats = {
            "word_count": len(words),
            "char_count": len(text),
            "sentence_count": max(1, sentences),
            "avg_word_length": round(sum(len(w) for w in words) / max(1, len(words)), 2)
        }
        
        return json.dumps(stats, indent=2)
    
    async def _arun(self, text: str) -> str:
        """Async version (not implemented)."""
        raise NotImplementedError("Async not supported")

class TemperatureConverterTool(BaseTool):
    name: str = "temperature_converter"
    description: str = """
    Convert temperature between Celsius and Fahrenheit.
    
    Input format: "25 C to F" or "77 F to C"
    """
    
    def _run(self, query: str) -> str:
        """Execute the tool."""
        try:
            parts = query.split()
            value = float(parts[0])
            from_unit = parts[1].upper()
            to_unit = parts[3].upper()
            
            if from_unit == 'C' and to_unit == 'F':
                result = (value * 9/5) + 32
                return f"{value}°C = {result:.2f}°F"
            elif from_unit == 'F' and to_unit == 'C':
                result = (value - 32) * 5/9
                return f"{value}°F = {result:.2f}°C"
            else:
                return "Invalid conversion. Use format: '25 C to F' or '77 F to C'"
        except Exception as e:
            return f"Error: {str(e)}. Use format: '25 C to F' or '77 F to C'"
    
    async def _arun(self, query: str) -> str:
        """Async version (not implemented)."""
        raise NotImplementedError("Async not supported")

def main():
    print("🔧 Custom Tools Example\n")
    
    # Initialize LLM
    print("📡 Initializing Ollama...")
    llm = Ollama(model="llama3.2", temperature=0)
    
    # Collect all tools
    tools = [
        flip_coin,
        roll_dice,
        reverse_text,
        TextStatsTool(),
        TemperatureConverterTool(),
    ]
    
    print(f"✓ Loaded {len(tools)} custom tools")
    print("\nAvailable tools:")
    for tool in tools:
        print(f"  - {tool.name}: {tool.description[:60]}...")
    
    # Create agent
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
    
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3,
        handle_parsing_errors=True
    )
    
    # Test queries
    queries = [
        "Flip a coin",
        "Roll a 20-sided dice",
        "Reverse the text: 'Hello World'",
        "Give me statistics for this text: 'The quick brown fox jumps over the lazy dog. It was amazing!'",
        "Convert 100 degrees Fahrenheit to Celsius",
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}: {query}")
        print('='*70)
        
        try:
            result = agent_executor.invoke({"input": query})
            print(f"\n✅ Result: {result['output']}")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    print("\n✅ Custom tools example completed!")
    
    # Show how to test tools directly
    print("\n" + "="*70)
    print("Testing tools directly (without agent)")
    print("="*70)
    
    print("\n1. Flip coin:", flip_coin.invoke({}))
    print("2. Roll dice:", roll_dice.invoke({"sides": 20}))
    print("3. Reverse text:", reverse_text.invoke({"text": "Python"}))
    print("4. Text stats:", TextStatsTool()._run("Testing the tool"))
    print("5. Temperature:", TemperatureConverterTool()._run("0 C to F"))

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
