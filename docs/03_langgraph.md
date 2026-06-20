# LangGraph: Building Stateful Agents

LangGraph enables you to build complex, stateful, multi-actor applications with LLMs using a graph-based approach.

## Why LangGraph?

Standard LangChain agents have limitations:
- Limited control over agent flow
- Hard to add complex logic
- Difficult to handle errors and retries
- Can't easily create multi-agent systems

**LangGraph solves this by treating agent workflows as state machines.**

## Core Concepts

### 1. State
The data that flows through your graph.

```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    messages: Annotated[list, "The conversation messages"]
    next: str  # Next node to execute
    final_answer: str  # Result
```

### 2. Nodes
Functions that process state.

```python
def research_node(state: AgentState) -> AgentState:
    """Research information."""
    query = state["messages"][-1]
    results = search_tool.run(query)
    state["messages"].append(f"Research: {results}")
    return state

def analyze_node(state: AgentState) -> AgentState:
    """Analyze research."""
    analysis = llm.invoke(state["messages"])
    state["final_answer"] = analysis
    return state
```

### 3. Edges
Connections between nodes (define flow).

```python
# Conditional edge
def should_continue(state: AgentState) -> str:
    if "done" in state["messages"][-1]:
        return "end"
    return "continue"

# Add edges
graph.add_edge("research", "analyze")  # Always go to analyze
graph.add_conditional_edges(
    "analyze",
    should_continue,
    {"continue": "research", "end": END}
)
```

## Basic Example: Simple Agent

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_community.llms import Ollama

# Define state
class SimpleState(TypedDict):
    input: str
    output: str
    steps: int

# Initialize LLM
llm = Ollama(model="llama3.2")

# Define nodes
def process_input(state: SimpleState) -> SimpleState:
    """Process user input."""
    response = llm.invoke(state["input"])
    state["output"] = response
    state["steps"] = state.get("steps", 0) + 1
    return state

def check_quality(state: SimpleState) -> SimpleState:
    """Check if response is good enough."""
    if len(state["output"]) > 50:
        state["output"] += " [Quality check passed]"
    return state

# Build graph
workflow = StateGraph(SimpleState)

# Add nodes
workflow.add_node("process", process_input)
workflow.add_node("quality_check", check_quality)

# Add edges
workflow.set_entry_point("process")
workflow.add_edge("process", "quality_check")
workflow.add_edge("quality_check", END)

# Compile
app = workflow.compile()

# Run
result = app.invoke({"input": "Explain Python in simple terms", "steps": 0})
print(result["output"])
```

## ReAct Agent with LangGraph

More control than standard ReAct:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    input: str
    agent_outcome: str
    intermediate_steps: Annotated[list, operator.add]

def run_agent(state: AgentState):
    """Let agent decide what to do."""
    agent_outcome = agent.invoke(state)
    return {"agent_outcome": agent_outcome}

def execute_tools(state: AgentState):
    """Execute the tool the agent selected."""
    agent_action = state["agent_outcome"]
    tool_output = tools[agent_action.tool].invoke(agent_action.tool_input)
    return {
        "intermediate_steps": [(agent_action, tool_output)]
    }

def should_continue(state: AgentState) -> str:
    """Decide if agent should continue or finish."""
    if isinstance(state["agent_outcome"], AgentFinish):
        return "end"
    return "continue"

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", run_agent)
workflow.add_node("tools", execute_tools)

workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {"continue": "tools", "end": END}
)
workflow.add_edge("tools", "agent")

app = workflow.compile()
```

## Human-in-the-Loop

Add approval steps:

```python
from langgraph.checkpoint import MemorySaver

class ApprovalState(TypedDict):
    content: str
    approved: bool

def generate_content(state: ApprovalState):
    content = llm.invoke("Write a tweet about AI")
    return {"content": content}

def human_approval(state: ApprovalState):
    """This will pause and wait for human input."""
    # In practice, this connects to your UI
    print(f"Content: {state['content']}")
    approved = input("Approve? (y/n): ") == "y"
    return {"approved": approved}

def publish(state: ApprovalState):
    if state["approved"]:
        print(f"Publishing: {state['content']}")
    else:
        print("Content rejected")
    return state

workflow = StateGraph(ApprovalState)
workflow.add_node("generate", generate_content)
workflow.add_node("approve", human_approval)
workflow.add_node("publish", publish)

workflow.set_entry_point("generate")
workflow.add_edge("generate", "approve")
workflow.add_edge("approve", "publish")
workflow.add_edge("publish", END)

# Use memory saver for persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)
```

## Multi-Agent Collaboration

Different agents for different tasks:

```python
class ResearchState(TypedDict):
    topic: str
    research: str
    outline: str
    draft: str
    final: str

def researcher(state: ResearchState):
    """Research the topic."""
    search_results = search_tool.run(state["topic"])
    return {"research": search_results}

def planner(state: ResearchState):
    """Create outline."""
    prompt = f"Create outline for: {state['topic']}\nResearch: {state['research']}"
    outline = llm.invoke(prompt)
    return {"outline": outline}

def writer(state: ResearchState):
    """Write draft."""
    prompt = f"Write article:\nOutline: {state['outline']}\nResearch: {state['research']}"
    draft = llm.invoke(prompt)
    return {"draft": draft}

def editor(state: ResearchState):
    """Edit and finalize."""
    prompt = f"Edit this article: {state['draft']}"
    final = llm.invoke(prompt)
    return {"final": final}

# Build pipeline
workflow = StateGraph(ResearchState)
workflow.add_node("research", researcher)
workflow.add_node("plan", planner)
workflow.add_node("write", writer)
workflow.add_node("edit", editor)

workflow.set_entry_point("research")
workflow.add_edge("research", "plan")
workflow.add_edge("plan", "write")
workflow.add_edge("write", "edit")
workflow.add_edge("edit", END)

app = workflow.compile()

result = app.invoke({"topic": "Benefits of Python for beginners"})
print(result["final"])
```

## Error Handling & Retries

```python
class RobustState(TypedDict):
    input: str
    output: str
    errors: list
    retry_count: int

def process_with_retry(state: RobustState):
    try:
        result = risky_llm_call(state["input"])
        return {"output": result, "retry_count": 0}
    except Exception as e:
        errors = state.get("errors", [])
        errors.append(str(e))
        retry_count = state.get("retry_count", 0) + 1
        return {"errors": errors, "retry_count": retry_count}

def should_retry(state: RobustState) -> str:
    if state.get("output"):
        return "success"
    if state.get("retry_count", 0) < 3:
        return "retry"
    return "failed"

workflow = StateGraph(RobustState)
workflow.add_node("process", process_with_retry)
workflow.add_node("success", lambda s: s)
workflow.add_node("failed", lambda s: {"output": "Failed after retries"})

workflow.set_entry_point("process")
workflow.add_conditional_edges(
    "process",
    should_retry,
    {"success": "success", "retry": "process", "failed": "failed"}
)
workflow.add_edge("success", END)
workflow.add_edge("failed", END)

app = workflow.compile()
```

## Persistence & Checkpoints

Save and resume workflows:

```python
from langgraph.checkpoint.sqlite import SqliteSaver

# Create checkpointer
checkpointer = SqliteSaver.from_conn_string("agent_checkpoints.db")

# Compile with checkpointer
app = workflow.compile(checkpointer=checkpointer)

# Run with thread_id for persistence
config = {"configurable": {"thread_id": "conversation-1"}}
result = app.invoke({"input": "Hello"}, config=config)

# Continue same conversation later
result = app.invoke({"input": "What did I just say?"}, config=config)
```

## Streaming

Get real-time updates:

```python
# Stream nodes as they execute
for event in app.stream({"input": "Explain AI"}):
    for node_name, node_output in event.items():
        print(f"Node: {node_name}")
        print(f"Output: {node_output}")
        print("---")
```

## Subgraphs

Compose graphs together:

```python
# Create subgraph for validation
validation_graph = StateGraph(ValidationState)
validation_graph.add_node("check", validate)
validation_graph.add_node("fix", fix_errors)
# ... build validation logic

validation_app = validation_graph.compile()

# Use in main graph
def validate_step(state: MainState):
    result = validation_app.invoke({"content": state["content"]})
    return {"content": result["content"]}

main_workflow.add_node("validate", validate_step)
```

## Practical Example: Code Review Agent

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class CodeReviewState(TypedDict):
    code: str
    language: str
    issues: list
    suggestions: list
    score: int

def analyze_code(state: CodeReviewState):
    """Analyze code for issues."""
    prompt = f"""Analyze this {state['language']} code and list issues:
    
    {state['code']}
    
    Return issues as JSON list."""
    
    response = llm.invoke(prompt)
    issues = parse_json(response)
    return {"issues": issues}

def generate_suggestions(state: CodeReviewState):
    """Generate improvement suggestions."""
    prompt = f"""Given these issues: {state['issues']}
    
    Suggest improvements for:
    {state['code']}"""
    
    suggestions = llm.invoke(prompt)
    return {"suggestions": suggestions}

def calculate_score(state: CodeReviewState):
    """Score the code quality."""
    issue_count = len(state["issues"])
    score = max(0, 100 - (issue_count * 10))
    return {"score": score}

# Build workflow
workflow = StateGraph(CodeReviewState)
workflow.add_node("analyze", analyze_code)
workflow.add_node("suggest", generate_suggestions)
workflow.add_node("score", calculate_score)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "suggest")
workflow.add_edge("suggest", "score")
workflow.add_edge("score", END)

app = workflow.compile()

# Use it
result = app.invoke({
    "code": "def hello():\n  print('hello')",
    "language": "python"
})
print(f"Score: {result['score']}")
print(f"Issues: {result['issues']}")
print(f"Suggestions: {result['suggestions']}")
```

## Best Practices

### 1. Keep State Simple
```python
# ✅ Good - simple, focused state
class State(TypedDict):
    input: str
    output: str
    step: int

# ❌ Bad - too much state
class State(TypedDict):
    input: str
    output: str
    intermediate_1: str
    intermediate_2: str
    temp_data: dict
    flags: list
    # ... too many fields
```

### 2. Use Type Hints
```python
from typing import TypedDict

class State(TypedDict):
    count: int  # Type hints help catch errors
    items: list[str]
```

### 3. Test Nodes Independently
```python
# Test nodes before adding to graph
state = {"input": "test"}
result = my_node(state)
assert "output" in result
```

### 4. Visualize Your Graph
```python
from IPython.display import Image, display

# Visualize the workflow
display(Image(app.get_graph().draw_mermaid_png()))
```

## Debugging

### 1. Print State at Each Node
```python
def debug_node(state):
    print(f"Current state: {state}")
    return state

workflow.add_node("debug", debug_node)
```

### 2. Use Verbose Mode
```python
for event in app.stream(input_data, {"verbose": True}):
    print(event)
```

### 3. Check Graph Structure
```python
print(app.get_graph().draw_ascii())
```

## When to Use LangGraph

**Use LangGraph when you need:**
- Complex, multi-step workflows
- Conditional logic and branching
- Human-in-the-loop approvals
- Multi-agent coordination
- Error handling and retries
- Persistent conversation state

**Use Standard Agents when:**
- Simple tool-use cases
- Quick prototypes
- Straightforward ReAct pattern

## Next Steps

- [Build RAG Systems](04_rag.md)
- [Try LangGraph examples](../examples/06_langgraph/)
- [Read LangGraph docs](https://langchain-ai.github.io/langgraph/)

## Key Takeaways

✅ **LangGraph treats workflows as state machines**  
✅ **Nodes are functions, edges define flow**  
✅ **Perfect for complex, multi-step agent workflows**  
✅ **Supports persistence, streaming, and human-in-the-loop**  
✅ **More control than standard LangChain agents**
