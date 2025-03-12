# Implementation Plan: AI Agent for Zork

## 1. Project Setup

### 1.1 Environment Configuration
- Create a virtual environment
- Install core dependencies:
  - langgraph (for agent workflow)
  - langchain (for LLM integration)
  - pydantic (for data validation)
  - python-dotenv (for environment variables)
  - jericho (optional, for alternative game interaction)
- Obtain Zork game file:
  - zork1-r119-s880429.z3 from https://github.com/the-infocom-files/zork1

### 1.2 Project Structure
```
ai-agent-zork/
├── games/              # Game files (.z3, .z5, .dat)
│   └── zork1-r119-s880429.z3
├── src/                # Source code
│   ├── agent/          # Agent implementation
│   ├── mock_environment.py  # Mock game environment
│   ├── jericho_environment.py  # Optional Jericho wrapper (reference)
│   └── main.py         # Entry point (to be implemented)
├── tests/              # Test cases
│   ├── simple_test.py  # Project structure verification
│   ├── test_mock_environment.py  # Tests for mock environment
│   └── test_jericho_environment.py  # Tests for Jericho (reference)
├── .env                # Environment variables (API keys)
├── .gitignore          # Git ignore file
├── implementation_plan.md  # This document
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## 2. Core Components

### 2.1 Game Environment

#### 2.1.1 Mock Environment (src/mock_environment.py)
- Pure Python implementation simulating Zork
- No external dependencies required
- Methods:
  - `__init__()`: Initialize the environment
  - `reset()`: Reset the game to initial state
  - `step(action)`: Execute action and return observation
  - `get_valid_actions()`: Get list of valid actions
  - `get_inventory()`: Get current inventory
  - Internal methods for handling specific actions and game state

#### 2.1.2 Jericho Environment (src/jericho_environment.py) - Optional
- Wrapper around Jericho's FrotzEnv
- Requires Jericho installation (Linux-compatible)
- Methods:
  - `__init__(game_path)`: Initialize the environment
  - `reset()`: Reset the game to initial state
  - `step(action)`: Execute action and return observation
  - `get_valid_actions()`: Get list of valid actions
  - `get_inventory()`: Get current inventory
  - `get_location()`: Get current location description
  - `save_state()/load_state()`: Save/load game state

### 2.2 Agent Components (src/agent/)

#### 2.2.1 Memory (src/agent/memory.py)
- Store and retrieve game history
- Track:
  - Visited locations
  - Collected items
  - Attempted actions
  - Game state history
- Methods:
  - `add_observation(observation)`: Add new observation
  - `add_action(action)`: Add performed action
  - `get_recent_history(n)`: Get last n interactions
  - `get_location_history()`: Get visited locations
  - `get_inventory_history()`: Get inventory changes

#### 2.2.2 Planner (src/agent/planner.py)
- Generate actions based on observations and memory
- Components:
  - Action generator (using LLM)
  - Action validator (using environment's valid actions)
- Methods:
  - `generate_action(observation, memory)`: Generate next action
  - `validate_action(action, valid_actions)`: Check if action is valid

#### 2.2.3 Workflow (src/agent/workflow.py)
- Define LangGraph workflow
- Nodes:
  - `observe`: Process game text
  - `think`: Reason about game state
  - `act`: Generate and execute action
- Edges:
  - observe → think → act → observe (loop)

### 2.3 Main Application (src/main.py)
- Initialize components
- Run the agent
- Handle command-line arguments
- Configure logging

### 2.4 Agent Tools and Capabilities

#### 2.4.1 Text Understanding Tools
- Natural language processing to parse game descriptions
- Entity recognition to identify objects, locations, and characters
- Context tracking to understand the current game situation

#### 2.4.2 Decision-Making Tools
- Action prioritization based on game state
- Goal management to track objectives
- Obstacle identification and resolution strategies

#### 2.4.3 Exploration Tools
- World mapping to create a mental model of the game world
- Systematic exploration strategies
- Backtracking mechanisms when stuck

#### 2.4.4 Memory Management Tools
- Short-term memory for recent interactions
- Long-term memory for important discoveries
- Knowledge graph of game elements and their relationships

#### 2.4.5 Planning Tools
- Multi-step planning for complex puzzles
- Hypothesis testing for uncertain game mechanics
- Plan adaptation when unexpected outcomes occur

#### 2.4.6 Zork-Specific Tools
- **Parser Adaptation**: Formulate commands in Zork's expected syntax and vocabulary
- **Maze Solving**: Special algorithms for mapping identical-looking rooms
- **Resource Management**: Track limited resources like lamp battery
- **Death Avoidance**: Recognize and prevent deadly situations (grues, thieves)
- **Puzzle Dependency Tracking**: Understand which puzzles unlock others
- **Inventory Optimization**: Make decisions about what to carry vs. store given weight limits
- **Object Interaction Discovery**: Systematically try verb-object combinations to discover interactions

## 3. Implementation Phases

### Phase 1: Basic Infrastructure (In Progress)
- ✅ Set up project structure
- ✅ Implement mock environment
- ⏳ Create simple memory system
- ⏳ Build basic action generator

### Phase 2: LangGraph Integration (Upcoming)
- Implement workflow nodes
- Connect nodes with edges
- Add state management
- Create basic agent loop

### Phase 3: Advanced Features (Planned)
- Improve memory with embeddings
- Add planning capabilities
- Implement exploration strategies
- Add performance metrics

### Phase 4: Evaluation & Refinement (Planned)
- Test on different game scenarios
- Measure success metrics
- Optimize prompts
- Refine decision-making

## 4. LLM Integration

### 4.1 Prompt Engineering
- Design prompts for:
  - Game understanding
  - Action generation
  - Planning and reasoning

### 4.2 Model Selection
- Options:
  - OpenAI models (GPT-4, GPT-3.5-turbo)
  - Open-source models (Llama, Mistral)
  - Local models for testing

### 4.3 API Integration
- Set up API keys in .env
- Implement fallback mechanisms
- Handle rate limiting

## 5. Testing Strategy

### 5.1 Unit Tests
- Test environment wrapper
- Test memory system
- Test action generation

### 5.2 Integration Tests
- Test full agent workflow
- Test game completion scenarios

### 5.3 Evaluation Metrics
- Success rate on known puzzles
- Steps to complete objectives
- Score progression over time

## 6. Development Workflow

### Completed Steps
1. ✅ Set up project structure
2. ✅ Implement mock environment (src/mock_environment.py)
3. ✅ Create tests for the mock environment (tests/test_mock_environment.py)
4. ✅ Verify project structure (tests/simple_test.py)

### Next Steps
5. Implement memory system (src/agent/memory.py)
6. Create action generator (src/agent/planner.py)
7. Implement LangGraph workflow (src/agent/workflow.py)
8. Create main application (src/main.py)
9. Test on simple game scenarios
10. Iteratively improve components
11. Add advanced features
12. Evaluate and refine
