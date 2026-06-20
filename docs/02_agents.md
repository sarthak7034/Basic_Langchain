# Building Agents with LangChain

Learn how to build autonomous agents that can use tools and make decisions.

## What is an Agent?

An **agent** is an LLM that can:
1. **Reason** about what to do next
2. **Use tools** to interact with external systems
3. **Observe** results and adapt
4. **Iterate** until the task is complete

Unlike chains (which have fixed logic), agents decide their own execution flow.

## Agent Types

### 1. ReAct Agent (Recommended)

**Re**asoning + **Act**ing pattern - the most common and effective.

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.prompts import PromptTemplate

# Initialize LLM
llm = Ollama(model="llama3.2", temperature=0)

# Define tools
search = DuckDuckGoSearchRun()
tools = [search]

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

Question: {input}
{agent_scratchpad}
""")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Run
result = agent_executor.invoke({
    "input": "What is the current weather in San Francisco?"
})
print(result["output"])
```

**How ReAct Works:**
1. **Think**: Agent reasons about what to do
2. **Act**: Agent calls a tool
3. **Observe**: Agent sees the result
4. **Repeat**: Until task is solved

### 2. OpenAI Functions Agent

Uses function calling (structured output) for more reliable tool use.

```python
from langchain.agents import create_openai_functions_agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")
tools = [search_tool, calculator_tool]

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

### 3. Structured Chat Agent

Better for multi-input tools.

```python
from langchain.agents import create_structured_chat_agent

agent = create_structured_chat_agent(llm, tools, prompt)
```

## Creating Custom Tools

### Method 1: Using @tool Decorator

```python
from langchain.tools import tool

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    return a * b
```

### Method 2: BaseTool Class

```python
from langchain.tools import BaseTool
from typing import Optional
from pydantic import Field

class CustomSearchTool(BaseTool):
    name: str = "custom_search"
    description: str = "Useful for searching information on the web"
    
    def _run(self, query: str) -> str:
        """Execute the tool."""
        # Your custom logic here
        return f"Search results for: {query}"
    
    async def _arun(self, query: str) -> str:
        """Async version."""
        raise NotImplementedError("Async not supported")

# Use it
tool = CustomSearchTool()
result = tool.run("Python tutorials")
```

### Method 3: Tool Function

```python
from langchain.tools import Tool

def search_api(query: str) -> str:
    # Your API logic
    return f"Results for {query}"

search_tool = Tool(
    name="Web Search",
    func=search_api,
    description="Search the web for current information"
)
```

## Built-in Tools

LangChain provides many ready-to-use tools:

```python
from langchain_community.tools import (
    DuckDuckGoSearchRun,
    WikipediaQueryRun,
    PythonREPLTool,
    ShellTool,
)
from langchain_community.utilities import WikipediaAPIWrapper

# Web search (free, no API key)
search = DuckDuckGoSearchRun()

# Wikipedia
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# Python REPL (be careful with this!)
python_repl = PythonREPLTool()

# Shell commands (use with caution)
shell = ShellTool()
```

## Agent Memory

Give agents memory of past interactions:

```python
from langchain.memory import ConversationBufferMemory

# Create memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Add to agent
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True
)

# Conversational agent
agent_executor.invoke({"input": "Hi, I'm Alice"})
agent_executor.invoke({"input": "What's my name?"})
# Agent remembers: "Your name is Alice"
```

## Error Handling

### Max Iterations

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    max_iterations=5,  # Prevent infinite loops
    max_execution_time=30,  # Timeout after 30 seconds
    verbose=True
)
```

### Handle Errors

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    handle_parsing_errors=True,  # Recover from parsing errors
    verbose=True
)
```

### Early Stopping

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    early_stopping_method="generate",  # or "force"
    verbose=True
)
```

## Practical Example: Research Assistant

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.llms import Ollama
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
import datetime

# Custom tool for current date
@tool
def get_current_date() -> str:
    """Returns the current date."""
    return datetime.datetime.now().strftime("%Y-%m-%d")

# Initialize
llm = Ollama(model="llama3.2", temperature=0)

# Tools
tools = [
    DuckDuckGoSearchRun(),
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    get_current_date,
]

# Prompt
prompt = PromptTemplate.from_template("""
You are a research assistant. Answer questions thoroughly using available tools.

Tools:
{tools}

Tool Names: {tool_names}

Format:
Question: {input}
Thought: [your reasoning]
Action: [tool name]
Action Input: [tool input]
Observation: [tool output]
... (repeat as needed)
Thought: I have enough information
Final Answer: [comprehensive answer]

Question: {input}
{agent_scratchpad}
""")

# Create and run agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

# Example queries
result = agent_executor.invoke({
    "input": "What major AI announcements were made this week?"
})
print(result["output"])
```

## Agent vs Chain: When to Use What

### Use Chains When:
- Fixed, predictable workflow
- No need for dynamic decision-making
- Performance is critical (chains are faster)
- Simple input → output transformation

### Use Agents When:
- Need to use external tools/APIs
- Workflow depends on intermediate results
- Multiple possible paths to solution
- Research or exploration tasks

## Best Practices

### 1. Clear Tool Descriptions

```python
# ❌ Bad
@tool
def tool1(x: str) -> str:
    """A tool."""
    return x

# ✅ Good
@tool
def web_search(query: str) -> str:
    """
    Search the web for current information.
    
    Use this when you need:
    - Recent news or events
    - Current facts or statistics
    - Real-time information
    
    Args:
        query: The search query (be specific)
    
    Returns:
        Search results as text
    """
    return search_api(query)
```

### 2. Limit Tool Count

```python
# ❌ Too many tools confuses the agent
tools = [tool1, tool2, tool3, tool4, tool5, tool6, tool7, tool8]

# ✅ Keep it focused (3-5 tools ideal)
tools = [web_search, calculator, wikipedia]
```

### 3. Set Temperature to 0

```python
# Agents need consistent reasoning
llm = Ollama(model="llama3.2", temperature=0)
```

### 4. Use Verbose Mode for Debugging

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,  # See agent's thinking
    return_intermediate_steps=True  # Get full reasoning chain
)

result = agent_executor.invoke({"input": "question"})
print(result["intermediate_steps"])
```

### 5. Validate Tool Outputs

```python
@tool
def risky_calculation(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        # Validate input
        if not all(c in "0123456789+-*/(). " for c in expression):
            return "Error: Invalid characters in expression"
        
        result = eval(expression)  # Still risky, use safer alternatives
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"
```

## Debugging Agents

### 1. Enable Verbose Output

```python
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### 2. Check Intermediate Steps

```python
result = agent_executor.invoke(
    {"input": "question"},
    return_intermediate_steps=True
)

for step in result["intermediate_steps"]:
    print(f"Action: {step[0].tool}")
    print(f"Input: {step[0].tool_input}")
    print(f"Output: {step[1]}")
    print("---")
```

### 3. Use LangSmith

```python
import os
os.environ["LANGSMITH_TRACING_V2"] = "true"
# Every agent execution logged to LangSmith dashboard
```

### 4. Test Tools Independently

```python
# Before using in agent, test tools directly
tool = DuckDuckGoSearchRun()
result = tool.run("test query")
print(result)
```

## Common Pitfalls

### 1. Parsing Errors
**Problem**: Agent output doesn't match expected format  
**Solution**: Use `handle_parsing_errors=True` or structured agents

### 2. Infinite Loops
**Problem**: Agent keeps calling tools without finishing  
**Solution**: Set `max_iterations` and review tool descriptions

### 3. Wrong Tool Selection
**Problem**: Agent uses wrong tool for the task  
**Solution**: Improve tool descriptions, reduce tool count

### 4. Hallucinated Tool Calls
**Problem**: Agent tries to call tools that don't exist  
**Solution**: Use function calling models or more explicit prompts

## Advanced Patterns

### Multi-Agent Collaboration

```python
# Research agent
research_agent = create_react_agent(llm, [search, wikipedia], research_prompt)

# Writing agent
writing_agent = create_react_agent(llm, [style_tool], writing_prompt)

# Coordinate them
def research_and_write(topic: str):
    # Research phase
    research = research_executor.invoke({"input": f"Research {topic}"})
    
    # Writing phase
    article = writing_executor.invoke({
        "input": f"Write article about {topic}",
        "research": research["output"]
    })
    
    return article
```

### Tool Chaining

```python
@tool
def search_and_summarize(query: str) -> str:
    """Search web and return summarized results."""
    search_results = search_tool.run(query)
    summary = summarize_tool.run(search_results)
    return summary
```

### Conditional Tools

```python
def get_tools_for_task(task_type: str):
    if task_type == "research":
        return [search, wikipedia]
    elif task_type == "calculation":
        return [calculator, python_repl]
    else:
        return [search]

tools = get_tools_for_task("research")
agent = create_react_agent(llm, tools, prompt)
```

## Next Steps

- [Learn LangGraph](03_langgraph.md) for more complex agent workflows
- [Build RAG Systems](04_rag.md) for document-based agents
- [Try agent examples](../examples/02_simple_agent/)

## Key Takeaways

✅ **Agents use tools to interact with the world**  
✅ **ReAct pattern is most common and effective**  
✅ **Clear tool descriptions are critical**  
✅ **Start simple, add complexity gradually**  
✅ **Always set max_iterations to prevent infinite loops**
