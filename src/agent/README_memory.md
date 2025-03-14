# Memory System

The memory system is responsible for storing and retrieving the agent's experiences in the game world. It provides a foundation for the agent's decision-making process by maintaining a record of observations, actions, locations, and inventory.

### Key Features

- **Raw Memory Storage**: Chronological record of all observations and actions
- **State Tracking**: Current location, score, moves, and inventory
- **History Retrieval**: Access to recent interactions and visited locations
- **Inventory Management**: Tracking of collected items

### Usage Example

```python
from src.mock_environment import MockZorkEnvironment
from src.agent.memory import AgentMemory

# Initialize environment and memory
env = MockZorkEnvironment()
memory = AgentMemory()

# Get initial state and add to memory
state = env.reset()
memory.add_observation(state["observation"], state)

# Perform an action
action = "look"
result = env.step(action)

# Record the action and its result
memory.add_action(action, result)
memory.add_observation(result["observation"], result)

# Check inventory
if action.lower() in ["inventory", "i"]:
    memory.update_inventory(result["inventory"])

# Retrieve recent history
recent_history = memory.get_recent_history(5)
for item in recent_history:
    print(f"[{item['type']}] {item['content']}")

# Get location history
locations = memory.get_location_history()
print(f"Visited locations: {locations}")

# Get inventory
inventory = memory.get_inventory()
print(f"Inventory: {inventory}")
```

### Design Approach

The memory system is implemented using a bottom-up approach:

1. **Basic Storage Layer**: Raw storage of observations and actions
2. **State Tracking Layer**: Tracking of game state (location, score, inventory)
3. **Retrieval Layer**: Methods to access and query stored information

This layered approach allows for incremental development and testing, with each layer building on the functionality of the previous ones.

### Future Enhancements

In future iterations, the memory system will be extended with:

- **Semantic Memory**: Understanding of game objects and their properties
- **Spatial Memory**: Improved mapping of the game world
- **Embeddings**: Vector representations for semantic search
- **Knowledge Graph**: Structured representation of game entities and relationships

## Testing

You can test the memory system using the provided test script:

```
python tests/test_memory.py
```

This script demonstrates how the memory system interacts with the mock environment and shows the information it tracks.
