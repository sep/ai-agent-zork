# AI Agent for Zork

An AI agent that plays the classic text adventure game Zork, demonstrating LLM-based agent capabilities.

## Project Overview

This project implements an AI agent that can play the text adventure game Zork. It uses:

- A custom mock environment that simulates Zork gameplay
- LangGraph for agent workflow management
- LangChain for LLM integration
- Python for all implementation

The agent demonstrates capabilities like:
- Understanding natural language game descriptions
- Planning and executing actions to solve puzzles
- Maintaining memory of game state and history
- Adapting to unexpected game situations

## Project Structure

```
ai-agent-zork/
├── games/              # Game files
│   └── zork1-r119-s880429.z3  # From https://github.com/the-infocom-files/zork1
├── mcp/                # MCP server implementation
│   └── zork-tools/     # MCP server for Zork tools
├── src/                # Source code
│   ├── agent/          # Agent implementation
│   │   ├── langgraph/  # LangGraph agent implementation
│   │   ├── mcp/        # MCP agent implementation
│   │   └── mcp_langgraph/ # MCP-LangGraph agent implementation
│   ├── mcp/            # MCP client implementation
│   └── mock_environment.py  # Mock game environment
├── tests/              # Test cases
└── requirements.txt    # Project dependencies
```

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the package in development mode:
   ```
   pip install -e .
   ```

   This will install all required dependencies and make the package importable
   from anywhere in your Python environment.

## Usage

### Playing the Mock Zork Environment Manually

You can interact with the mock Zork environment directly using the interactive script:

```
python src/play_zork.py
```

This will start an interactive session where you can type commands like:
- `north`, `south`, `east`, `west` - Move in different directions
- `look` - Look around
- `examine [object]` - Examine an object
- `take [object]` - Take an object
- `inventory` or `i` - Check your inventory
- `open [object]`, `close [object]` - Interact with objects
- `valid` - Show valid actions in the current state
- `help` - Show available commands
- `quit` or `exit` - End the session

### Running the AI Agent

The project provides several ways to run the AI agent, depending on which approach you want to use:

#### Rule-Based Agent

You can run the agent with the rule-based planner using:

```
python src/run_rule_based_agent.py
```

This will start the agent with a rule-based planner that:
- Explores the environment systematically
- Interacts with objects it encounters
- Tracks its progress through the game
- Continues until stopped (Ctrl+C)

The rule-based agent doesn't require an LLM or API key.

#### LLM-Based Agents

For more sophisticated agents that use LLMs, you can use the unified runner:

```
# Run the LangGraph agent (generates text commands directly)
python src/run_zork_agent.py --agent-type langgraph

# Run the MCP-LangGraph agent (uses tools with structured parameters)
python src/run_zork_agent.py --agent-type mcp_langgraph

# Run the MCP agent (uses MCP directly without LangGraph)
python src/run_zork_agent.py --agent-type mcp
```

You can specify which LLM model to use with the `--model` flag:

```
python src/run_zork_agent.py --agent-type mcp_langgraph --model gpt-4
```

### LLM Integration

The LLM-based planner requires an OpenAI API key to function. You can provide this in three ways:

1. Create a `.env` file in the project root with your API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
   (You can copy and rename the provided `.env.example` file)

2. Set the `OPENAI_API_KEY` environment variable:
   ```
   # On Linux/macOS
   export OPENAI_API_KEY=your-api-key-here
   
   # On Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   ```

3. Pass the API key directly as a command-line argument:
   ```
   python src/run_zork_agent.py --agent-type langgraph --api-key your-api-key-here
   ```

If no API key is provided, the LLM-based agents will attempt to use the environment variable.

The agent will display each action it takes, the resulting observation, and its current state (location, score, inventory).

## Development Status

- ✅ Project structure setup
- ✅ Mock environment implementation
- ✅ Agent memory system
- ✅ Rule-based action planner
- ✅ LLM-based action planner
- ✅ LangGraph workflow

## Components

### Mock Environment

The mock environment simulates the Zork game world without requiring external dependencies. It provides:

- Navigation between locations
- Object interactions (examining, taking, dropping)
- Inventory management
- Score and move tracking

You can interact with it directly using:
```
python src/play_zork.py
```

### Memory System

The memory system tracks the agent's experiences in the game world:

- Stores observations and actions
- Tracks location history and inventory
- Provides retrieval methods for recent history

You can test it using:
```
python tests/test_memory.py
```

### Action Planners

The project includes two types of action planners that generate actions based on observations and memory:

#### Rule-Based Planner

The rule-based planner uses predefined rules to generate actions:

- Prioritized action generation based on game state
- Action validation and correction
- Exploration state tracking
- Avoids repetitive actions

You can test it using:
```
python tests/test_planner.py
```

Note: The rule-based planner is implemented in `src/agent/rule_based_planner.py`.

#### LLM-Based Planner

The LLM-based planner extends the rule-based planner with more sophisticated reasoning:

- Uses an LLM to generate contextually appropriate actions
- Maintains a context window of recent game state
- Falls back to rule-based planning when needed
- Provides more advanced puzzle-solving capabilities

You can use it with any of the LLM-based agents:
```
python src/run_zork_agent.py --agent-type langgraph
```

### Agent Architectures

This project implements three different agent architectures to demonstrate the evolution of AI agent design:

#### LangGraph Agent

The LangGraph agent uses a LangGraph workflow with an observe-think-act loop:

- Generates text commands directly (e.g., "go north", "take lamp")
- Implicit reasoning about available actions
- Natural language command generation

You can run this agent using:

```
# Using the unified runner
python src/run_zork_agent.py --agent-type langgraph

# Using the dedicated runner
python src/run_langgraph_agent.py
```

The LangGraph agent provides:
- Transparent reasoning (thoughts are displayed)
- Direct command generation
- Stateful workflow management

A detailed diagram and explanation of the LangGraph agent workflow can be found in [src/agent/langgraph/README.md](src/agent/langgraph/README.md).

#### MCP-LangGraph Agent

The MCP-LangGraph agent combines LangGraph for workflow structure with MCP for tool-based interaction:

- Selects specific MCP tools and provides parameters
- Follows an observe-think-select_tool-act loop
- Provides more structured interaction with the environment
- Uses tool definitions and examples directly from the MCP server
- Features prominent warning messages for error conditions

You can run this agent using:

```
# Using the unified runner
python src/run_zork_agent.py --agent-type mcp_langgraph

# Using the dedicated runner
python src/run_mcp_langgraph_agent.py

# With fallback to mock environment if MCP is not available
python src/run_mcp_langgraph_agent.py --fallback-to-mock
```

The MCP-LangGraph agent provides several advantages:
- More structured interaction with the environment through MCP tools
- Clearer separation of reasoning and action
- Better alignment with modern AI agent frameworks
- Direct integration with the Model Context Protocol (MCP)
- Robust error handling with clear warning messages
- Dynamic tool discovery from the MCP server

A detailed diagram and explanation of the MCP-LangGraph agent workflow can be found in [src/agent/mcp_langgraph/README.md](src/agent/mcp_langgraph/README.md).

#### MCP Agent

The MCP agent uses MCP directly without LangGraph:

- Follows a deliberative process of thinking then acting
- Uses MCP tools to interact with the environment
- Dynamically retrieves tool definitions from the MCP server
- Features prominent warning messages for error conditions
- Simpler implementation but less structured workflow

You can run this agent using:

```
# Using the unified runner
python src/run_zork_agent.py --agent-type mcp

# Using the dedicated runner
python src/run_mcp_agent.py
```

The MCP agent provides:
- Direct use of MCP tools without the LangGraph workflow
- Two-step process: deliberation followed by action selection
- Simpler implementation compared to the LangGraph-based agents
- Robust error handling with clear warning messages
- Dynamic tool discovery from the MCP server

A detailed explanation of the MCP agent can be found in [src/agent/mcp/README.md](src/agent/mcp/README.md).

## License

This project is for educational purposes.

- Zork game file from: https://github.com/the-infocom-files/zork1
- Original Zork game copyright by Infocom
