# Agent Components

This directory contains the core components of the Zork AI agent system.

## Overview

The agent system is composed of several key components:

1. **Memory System** - Stores and retrieves the agent's experiences in the game world
2. **Planner** - Generates actions based on observations and memory
3. **Agent Implementations** - Different approaches to implementing the agent

## Agent Implementations

We have implemented three different agent architectures to demonstrate the evolution of AI agent design:

### LangGraph Agent

Located in `langgraph/` directory, this agent:
- Uses LangGraph to structure the agent's workflow
- Generates text commands directly (e.g., "go north", "take lamp")
- Does not use MCP, instead interacting with a mock environment
- Follows an observe-think-act loop

See [langgraph/README.md](langgraph/README.md) for more details.

### MCP LangGraph Agent

Located in `mcp_langgraph/` directory, this agent:
- Combines LangGraph for workflow structure with MCP for tool-based interaction
- Selects specific MCP tools and provides parameters
- Provides more structured interaction with the environment
- Follows an observe-think-select_tool-act loop

See [mcp_langgraph/README.md](mcp_langgraph/README.md) for more details.

### MCP Agent

Located in `mcp/` directory, this agent:
- Uses MCP directly without LangGraph
- Follows a deliberative process of thinking then acting
- Lacks the structured workflow that LangGraph provides
- Simpler implementation but less structured

See [mcp/README.md](mcp/README.md) for more details.

## Core Components

### Memory System

The memory system is responsible for storing and retrieving the agent's experiences in the game world. It provides a foundation for the agent's decision-making process by maintaining a record of observations, actions, locations, and inventory.

See [README_memory.md](README_memory.md) for more details.

### Planner

The planner component is responsible for generating actions based on observations and memory, and validating them against the environment's valid actions.

See [README_planner.md](README_planner.md) for more details.

## Usage

Each agent implementation has its own runner script:

```bash
# Run the LangGraph agent
python src/run_langgraph_agent.py

# Run the MCP LangGraph agent
python src/run_mcp_langgraph_agent.py

# Run the MCP agent
python src/run_mcp_agent.py
```

You can also use the unified runner:

```bash
# Run the LangGraph agent
python src/run_zork_agent.py --agent-type langgraph

# Run the MCP LangGraph agent
python src/run_zork_agent.py --agent-type mcp_langgraph

# Run the MCP agent
python src/run_zork_agent.py --agent-type mcp
```

## Testing

Each component and agent implementation has its own test file:

```bash
# Test the memory system
python tests/test_memory.py

# Test the planner
python tests/test_planner.py

# Test the LangGraph agent
python tests/test_langgraph_workflow.py

# Test the MCP LangGraph agent
python tests/test_mcp_langgraph_workflow.py

# Test the MCP agent
python tests/test_mcp_agent.py
```

You can run all tests with:

```bash
python -m unittest discover tests
