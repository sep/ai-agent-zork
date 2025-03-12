"""
Simple test script to verify the project structure.
"""
import os
import sys

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


def main():
    """
    Test the project structure and print information about the Zork game file.
    """
    # Find the Zork game file
    game_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "games"
    )
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(__file__)}")
    print(f"Game directory: {game_dir}")
    
    if os.path.exists(game_dir):
        print(f"Game directory exists: {game_dir}")
        game_files = [
            f for f in os.listdir(game_dir) 
            if f.endswith((".z3", ".z5", ".dat"))
        ]
        
        if game_files:
            print(f"Found game files: {game_files}")
            game_path = os.path.join(game_dir, game_files[0])
            print(f"Using game file: {game_path}")
            
            # Print file size
            file_size = os.path.getsize(game_path)
            print(f"File size: {file_size} bytes")
        else:
            print(f"No game files found in {game_dir}")
    else:
        print(f"Game directory does not exist: {game_dir}")


if __name__ == "__main__":
    main()
