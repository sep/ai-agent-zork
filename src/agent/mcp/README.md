# MCP Zork Agent

This package implements a direct MCP agent that uses the MCP environment to play Zork.

## Overview

The MCP agent follows a two-step process:

1. **Deliberation**: The agent first thinks about what to do next, considering the current game state, goals, and possible actions.
2. **Action Selection**: Based on this deliberation, the agent selects a specific action to take.

This approach mimics human problem-solving: we typically think before we act, weighing options and considering consequences.

## Usage

To run the MCP agent, use the `run_mcp_agent.py` script:

```bash
python src/run_mcp_agent.py
```

You can also use the unified runner:

```bash
python src/run_zork_agent.py --agent-type mcp
```

You can customize the agent's behavior with the following options:

- `--model`: The LLM model to use (default: "gpt-3.5-turbo")
- `--api-key`: The API key for the LLM provider (defaults to OPENAI_API_KEY env var)
- `--max-steps`: Maximum number of steps to run (default: 20)
- `--debug`: Print debug information

## Implementation

The agent is implemented in `agent.py` and consists of three main functions:

- `run_agent`: The main function that runs the agent loop
- `generate_thought`: Generates a deliberative thought about what to do next
- `select_action`: Selects an action to take based on the thought

The agent uses the MCP environment to interact with the Zork game.

## Comparison with Other Agents

- **LangGraph Agent**: Uses LangGraph but not MCP, generates text commands directly
- **MCP LangGraph Agent**: Uses both LangGraph and MCP, selects MCP tools and provides parameters
- **MCP Agent**: Uses MCP directly without LangGraph, follows a deliberative process
