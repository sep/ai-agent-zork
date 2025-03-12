"""
Test script for the agent memory system.

This script demonstrates how the memory system works with the mock environment.
It performs a sequence of actions and shows how the memory system tracks
observations, actions, locations, and inventory.
"""
from src.mock_environment import MockZorkEnvironment
from src.agent.memory import AgentMemory


def print_section(title):
    """Print a section title with separators."""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    """
    Test the AgentMemory class with the mock environment.
    
    This function:
    1. Initializes the environment and memory
    2. Performs a sequence of actions
    3. Shows the memory state after each action
    4. Demonstrates memory retrieval methods
    """
    print_section("MEMORY SYSTEM TEST")
    print("This test demonstrates how the memory system works with the")
    print("environment.")
    
    # Initialize the environment and memory
    env = MockZorkEnvironment()
    memory = AgentMemory()
    
    # Get the initial state
    state = env.reset()
    
    # Add the initial observation to memory
    memory.add_observation(state["observation"], state)
    
    print_section("INITIAL STATE")
    print(f"Location: {memory.current_location}")
    print(f"Observation: {state['observation']}")
    print(f"Memory state: {memory}")
    
    # Define a sequence of actions to test different aspects of the memory
    # system
    test_actions = [
        "look",                  # Basic observation
        "examine mailbox",       # Examining an object
        "open mailbox",          # Interacting with an object
        "take leaflet",          # Taking an item
        "inventory",             # Checking inventory
        "read leaflet",          # Using an item
        "go north",              # Moving to a new location
        "go east",               # Moving again
        "invalid command",       # Testing an invalid action
    ]
    
    # Execute each action and update memory
    for action in test_actions:
        print_section(f"ACTION: {action}")
        
        # Execute the action in the environment
        result = env.step(action)
        
        # Add the action and result to memory
        memory.add_action(action, result)
        memory.add_observation(result["observation"], result)
        
        # Update inventory if this was an inventory command
        if action.lower() in ["inventory", "i"]:
            memory.update_inventory(result["inventory"])
        
        # Print the result and memory state
        print(f"Observation: {result['observation']}")
        print(f"Location: {memory.current_location}")
        print(f"Score: {memory.score}")
        print(f"Moves: {memory.moves}")
        print(f"Memory state: {memory}")
    
    # Demonstrate memory retrieval methods
    print_section("MEMORY RETRIEVAL")
    
    print("Recent History (last 5 interactions):")
    recent_history = memory.get_recent_history(5)
    for i, item in enumerate(recent_history, 1):
        print(f"{i}. [{item['type']}] {item['content'][:50]}...")
    
    print("\nLocation History:")
    locations = memory.get_location_history()
    for i, location in enumerate(locations, 1):
        print(f"{i}. {location}")
    
    print("\nInventory:")
    inventory = memory.get_inventory()
    if inventory:
        for i, item in enumerate(inventory, 1):
            print(f"{i}. {item}")
    else:
        print("Inventory is empty")


if __name__ == "__main__":
    main()
