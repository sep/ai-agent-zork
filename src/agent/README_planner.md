# Planner Component

The planner component is responsible for generating actions based on observations and memory, and validating them against the environment's valid actions.

## Key Features

- **Rule-based Action Generation**: Generates actions based on observations, valid actions, and memory
- **Action Validation**: Validates actions against the environment's valid actions
- **Exploration State Tracking**: Tracks explored locations and action history

## Usage Example

```python
from src.mock_environment import MockZorkEnvironment
from src.agent.memory import AgentMemory
from src.agent.planner import ActionPlanner

# Initialize components
env = MockZorkEnvironment()
memory = AgentMemory()
planner = ActionPlanner()

# Get initial state
state = env.reset()
memory.add_observation(state["observation"], state)

# Main agent loop
for _ in range(10):  # Run for 10 steps
    # Generate action
    action = planner.generate_action(
        state["observation"],
        state["valid_actions"],
        memory
    )
    
    # Execute action
    result = env.step(action)
    
    # Update memory
    memory.add_action(action, result)
    memory.add_observation(result["observation"], result)
    
    # Update inventory if needed
    if action.lower() in ["inventory", "i"]:
        memory.update_inventory(result["inventory"])
    
    # Update exploration state
    planner.update_exploration_state(result["observation"], memory)
    
    # Update state for next iteration
    state = result
```

## Design Approach

The planner is implemented using a bottom-up approach:

1. **Basic Action Generation**: Simple rule-based action generation
   - Look around if we haven't recently
   - Check inventory if we haven't recently
   - Interact with objects mentioned in observations
   - Explore new directions
   - Fall back to random valid actions

2. **Action Validation**: Validate and correct actions
   - Check if action is already valid
   - Look for similar valid actions
   - Handle special cases like directions without "go"

3. **Exploration State**: Track exploration progress
   - Record visited locations
   - Track action history to avoid repetition

## Future Enhancements

In future iterations, the planner will be extended with:

1. **LLM-based Action Generation**: Replace rule-based generation with LLM
   - Use prompts to generate contextually appropriate actions
   - Incorporate memory for informed decision-making

2. **Goal-oriented Planning**: Add support for goals and subgoals
   - Define high-level goals (e.g., "explore the house")
   - Break down into subgoals (e.g., "find a way in")
   - Generate actions to achieve goals

3. **Advanced Exploration Strategies**:
   - Systematic exploration of the game world
   - Backtracking when stuck
   - Puzzle-solving strategies

## Testing

You can test the planner using the provided test script:

```
python tests/test_planner.py
```

This script demonstrates how the planner works with the mock environment and memory system, showing:
- Action generation based on observations and memory
- Action validation and correction
- Exploration state tracking
