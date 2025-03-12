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

*Note: The AI agent implementation is still in progress.*

## Development Status

- ✅ Project structure setup
- ✅ Mock environment implementation
- ✅ Agent memory system
- ✅ Action planner/generator
- ⏳ LangGraph workflow (planned)

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

### Action Planner

The action planner generates actions based on observations and memory:

- Rule-based action generation
- Action validation and correction
- Exploration state tracking

You can test it using:
```
python tests/test_planner.py
```

## License

This project is for educational purposes.

- Zork game file from: https://github.com/the-infocom-files/zork1
- Original Zork game copyright by Infocom
