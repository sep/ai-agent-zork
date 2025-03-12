"""
Test script for the mock Zork environment.
"""
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import after path setup
from src.mock_environment import MockZorkEnvironment  # noqa: E402


def main():
    """
    Test the MockZorkEnvironment class with a simple interaction.
    """
    # Initialize the environment
    env = MockZorkEnvironment()
    
    # Get the initial state
    state = env.reset()
    print("\n" + "="*50)
    print("INITIAL STATE:")
    print("="*50)
    print(state["observation"])
    print(f"Score: {state['score']}")
    print(f"Location: {state['location']}")
    
    # Test a sequence of commands that demonstrates key features
    test_commands = [
        "look",
        "examine mailbox",
        "open mailbox",
        "examine leaflet",
        "take leaflet",
        "read leaflet",
        "go north",
        "go east",
        "go south",
        "go east",
        "enter window",
        "go west",
        "take lamp",
        "inventory",
        "take sword",
        "examine rug",
        "move rug",
        "go down",
        "turn on lamp",
        "look"
    ]
    
    for command in test_commands:
        print("\n" + "="*50)
        print(f"COMMAND: {command}")
        print("="*50)
        state = env.step(command)
        print(state["observation"])
        print(f"Score: {state['score']}")
        print(f"Location: {state['location']}")
        
    # Print valid actions at the end
    print("\n" + "="*50)
    print("VALID ACTIONS:")
    print("="*50)
    for action in state["valid_actions"][:10]:  # Show first 10 valid actions
        print(f"- {action}")
    if len(state["valid_actions"]) > 10:
        print(f"... and {len(state['valid_actions']) - 10} more")


if __name__ == "__main__":
    main()
