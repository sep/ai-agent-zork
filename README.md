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

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

*Note: The agent implementation is still in progress. This section will be updated when the agent is ready to use.*

## Development Status

- ✅ Project structure setup
- ✅ Mock environment implementation
- ⏳ Agent memory system (in progress)
- ⏳ Action generator (planned)
- ⏳ LangGraph workflow (planned)

## License

This project is for educational purposes.

- Zork game file from: https://github.com/the-infocom-files/zork1
- Original Zork game copyright by Infocom
