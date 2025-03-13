"""
Test script for the Jericho-based Zork environment wrapper.

Note: This test requires Jericho, which has installation issues on Windows.
      It is kept for reference but not currently used.
"""
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Import after path setup
from src.jericho_environment import ZorkEnvironment  # noqa: E402


def main():
    """
    Test the ZorkEnvironment class with a simple interaction.
    """
    # Find the Zork game file
    game_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "games"
    )
    game_files = [
        f for f in os.listdir(game_dir) 
        if f.endswith((".z3", ".z5", ".dat"))
    ]
    
    if not game_files:
        print(f"No game files found in {game_dir}")
        print("Please place a Zork game file (.z3, .z5, or .dat) "
              "in the games directory")
        sys.exit(1)
    
    game_path = os.path.join(game_dir, game_files[0])
    print(f"Using game file: {game_path}")
    
    # Initialize the environment
    env = ZorkEnvironment(game_path)
    
    # Get the initial observation
    state = env.reset()
    print("\n" + "="*50)
    print("INITIAL STATE:")
    print("="*50)
    print(state["observation"])
    
    # Test a few commands
    test_commands = [
        "look",
        "inventory",
        "examine mailbox",
        "open mailbox",
        "take leaflet",
        "read leaflet",
        "go north"
    ]
    
    for command in test_commands:
        print("\n" + "="*50)
        print(f"COMMAND: {command}")
        print("="*50)
        state = env.step(command)
        print(state["observation"])
        print(f"Score: {state['score']}")
        
    # Print valid actions
    print("\n" + "="*50)
    print("VALID ACTIONS:")
    print("="*50)
    for action in state["valid_actions"][:10]:  # Show first 10 valid actions
        print(f"- {action}")
    if len(state["valid_actions"]) > 10:
        print(f"... and {len(state['valid_actions']) - 10} more")


if __name__ == "__main__":
    main()
