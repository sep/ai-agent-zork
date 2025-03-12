"""
Test script for the agent planner system.

This script demonstrates how the planner works with the mock environment
and memory system. It performs a sequence of actions and shows how the
planner generates actions based on observations and memory.
"""
from src.mock_environment import MockZorkEnvironment
from src.agent.memory import AgentMemory
from src.agent.planner import ActionPlanner


def print_section(title):
    """Print a section title with separators."""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    """
    Test the ActionPlanner class with the mock environment and memory.
    
    This function:
    1. Initializes the environment, memory, and planner
    2. Runs a simulation of the agent exploring the environment
    3. Shows how the planner generates actions based on observations and memory
    """
    print_section("PLANNER SYSTEM TEST")
    print("This test demonstrates how the planner works with the environment")
    print("and memory system.")
    
    # Initialize the components
    env = MockZorkEnvironment()
    memory = AgentMemory()
    planner = ActionPlanner()
    
    # Get the initial state
    state = env.reset()
    
    # Add the initial observation to memory
    memory.add_observation(state["observation"], state)
    
    print_section("INITIAL STATE")
    print(f"Location: {memory.current_location}")
    print(f"Observation: {state['observation']}")
    print(f"Valid actions: {', '.join(state['valid_actions'][:5])}...")
    
    # Run a simulation for a fixed number of steps
    max_steps = 10
    for step in range(max_steps):
        print_section(f"STEP {step + 1}")
        
        # Generate an action using the planner
        action = planner.generate_action(
            state["observation"],
            state["valid_actions"],
            memory
        )
        
        print(f"Generated action: {action}")
        
        # Execute the action in the environment
        result = env.step(action)
        
        # Add the action and result to memory
        memory.add_action(action, result)
        memory.add_observation(result["observation"], result)
        
        # Update inventory if this was an inventory command
        if action.lower() in ["inventory", "i"]:
            memory.update_inventory(result["inventory"])
        
        # Update exploration state in the planner
        planner.update_exploration_state(result["observation"], memory)
        
        # Print the result and memory state
        print(f"Observation: {result['observation']}")
        print(f"Location: {memory.current_location}")
        print(f"Score: {memory.score}")
        print(f"Moves: {memory.moves}")
        print(f"Inventory: {memory.get_inventory()}")
        print(f"Explored locations: {planner.explored_locations}")
        
        # Update the state for the next iteration
        state = result
    
    # Demonstrate action validation
    print_section("ACTION VALIDATION")
    
    test_actions = [
        "north",  # Direction without "go"
        "examine mailbox",  # Valid action
        "open door",  # Invalid action
        "take leaflet",  # Valid action
        "jump",  # Invalid action
    ]
    
    for test_action in test_actions:
        is_valid, corrected_action = planner.validate_action(
            test_action,
            state["valid_actions"]
        )
        
        if is_valid:
            print(f"'{test_action}' is valid as '{corrected_action}'")
        else:
            print(f"'{test_action}' is not valid")


if __name__ == "__main__":
    main()
