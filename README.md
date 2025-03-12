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
├── src/                # Source code
│   ├── agent/          # Agent implementation
│   ├── mock_environment.py  # Mock game environment
│   └── jericho_environment.py  # Optional Jericho wrapper (reference)
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

You can run the AI agent that automatically plays Zork using:

```
python src/run_agent.py
```

This will start the agent with the rule-based planner by default, which will:
- Explore the environment systematically
- Interact with objects it encounters
- Track its progress through the game
- Continue until stopped (Ctrl+C)

You can also run the agent with the LLM-based planner by using the `--use-llm` flag:

```
python src/run_agent.py --use-llm
```

You can specify which LLM model to use with the `--model` flag:

```
python src/run_agent.py --use-llm --model gpt-4
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
   python src/run_agent.py --use-llm --api-key your-api-key-here
   ```

If no API key is provided, the LLM-based planner will fall back to the rule-based planner.

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

#### LLM-Based Planner

The LLM-based planner extends the rule-based planner with more sophisticated reasoning:

- Uses an LLM to generate contextually appropriate actions
- Maintains a context window of recent game state
- Falls back to rule-based planning when needed
- Provides more advanced puzzle-solving capabilities

You can use it by running:
```
python src/run_agent.py --use-llm
```

### LangGraph Workflow

The LangGraph workflow implements a more sophisticated agent architecture:

- Observe-Think-Act loop for better reasoning
- Explicit thought generation before taking actions
- Stateful workflow management
- Better handling of complex game situations

You can run the agent with the LangGraph workflow using:
```
python src/run_langgraph_agent.py
```

You can specify which LLM model to use with the `--model` flag:
```
python src/run_langgraph_agent.py --model gpt-4
```

The LangGraph workflow provides several advantages:
- More transparent reasoning (thoughts are displayed)
- Better decision-making through explicit reasoning
- More flexible architecture for future enhancements

A detailed diagram and explanation of the agent workflow can be found in [docs/agent_workflow.md](docs/agent_workflow.md).

## License

This project is for educational purposes.

- Zork game file from: https://github.com/the-infocom-files/zork1
- Original Zork game copyright by Infocom
