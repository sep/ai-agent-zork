"""
Interactive script to manually play the mock Zork environment.
This allows testing and exploring the environment without an AI agent.
"""
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Import after path setup
from src.mock_environment import MockZorkEnvironment  # noqa: E402


def main():
    """
    Run an interactive session with the mock Zork environment.
    """
    print("\n" + "="*60)
    print("MOCK ZORK INTERACTIVE MODE")
    print("="*60)
    print("Type commands to interact with the game.")
    print("Type 'quit' or 'exit' to end the session.")
    print("Type 'help' for available commands.")
    print("Type 'valid' to see valid actions in current state.")
    print("="*60 + "\n")
    
    # Initialize the environment
    env = MockZorkEnvironment()
    state = env.reset()
    
    # Display initial state
    print(state["observation"])
    print(f"Score: {state['score']} | "
          f"Moves: {state['moves']}")
    
    # Main interaction loop
    while True:
        # Get user input
        action = input("\n> ").strip()
        
        # Check for exit command
        if action.lower() in ["quit", "exit"]:
            print("\nThanks for playing!")
            break
        
        # Check for help command
        elif action.lower() == "help":
            print("\nAvailable commands:")
            print("- Movement: north, south, east, west, up, down")
            print("- Look: look, examine [object]")
            print("- Objects: take [object], drop [object]")
            print("- Interaction: open [object], close [object],")
            print("  read [object]")
            print("- Inventory: inventory, i")
            print("- Meta: valid (show valid actions), quit, exit, help")
            continue
        
        # Check for valid actions command
        elif action.lower() == "valid":
            print("\nValid actions in current state:")
            for valid_action in state["valid_actions"]:
                print(f"- {valid_action}")
            continue
        
        # Process the action in the environment
        state = env.step(action)
        
        # Display the result
        print("\n" + state["observation"])
        print(f"Score: {state['score']} | "
              f"Moves: {state['moves']}")
        
        # Display inventory if requested
        if action.lower() in ["inventory", "i"]:
            print("\n" + state["inventory"])


if __name__ == "__main__":
    main()
