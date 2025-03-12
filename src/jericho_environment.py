"""
Game environment wrapper for Zork using Jericho.

Note: This implementation requires Jericho, which has installation issues
      on Windows. It is kept for reference but not currently used.
      Use mock_environment.py instead.
"""
import os
from typing import Dict, List, Any

import jericho


class ZorkEnvironment:
    """
    Wrapper for the Zork game environment using Jericho.
    Provides methods to interact with the game and access game state.
    """

    def __init__(self, game_path: str):
        """
        Initialize the Zork environment.

        Args:
            game_path: Path to the Zork game file (.z3, .z5, or .dat)
        """
        if not os.path.exists(game_path):
            raise FileNotFoundError(f"Game file not found: {game_path}")

        self.env = jericho.FrotzEnv(game_path)
        self.game_name = os.path.basename(game_path).split('.')[0]
        self.current_step = 0
        self.max_steps = 1000  # Prevent infinite loops
        self.reset()

    def reset(self) -> Dict[str, Any]:
        """
        Reset the game environment to its initial state.

        Returns:
            Dict containing the initial observation and game info
        """
        initial_observation, info = self.env.reset()
        self.current_step = 0
        
        return {
            "observation": initial_observation,
            "score": 0,
            "done": False,
            "moves": 0,
            "valid_actions": self.get_valid_actions(),
            "inventory": self.get_inventory(),
            "location": self.get_location(),
            "info": info
        }

    def step(self, action: str) -> Dict[str, Any]:
        """
        Take a step in the game by executing the given action.

        Args:
            action: Text command to execute in the game

        Returns:
            Dict containing the observation, reward, done flag, 
            and additional info
        """
        self.current_step += 1
        
        # Execute the action in the game
        result = self.env.step(action)
        observation, score, done, info = result
        
        # Check if we've reached the maximum number of steps
        if self.current_step >= self.max_steps:
            done = True
        
        return {
            "observation": observation,
            "score": score,
            "done": done,
            "moves": self.current_step,
            "valid_actions": self.get_valid_actions(),
            "inventory": self.get_inventory(),
            "location": self.get_location(),
            "info": info
        }

    def get_valid_actions(self) -> List[str]:
        """
        Get a list of valid actions in the current game state.

        Returns:
            List of valid action strings
        """
        valid_actions = self.env.get_valid_actions()
        return valid_actions

    def get_inventory(self) -> str:
        """
        Get the current inventory.

        Returns:
            String describing the current inventory
        """
        # Execute 'inventory' command and return the result
        obs, _, _, _ = self.env.step('inventory')
        # Undo the 'inventory' command to not affect game state
        self.env.step('look')  # Reset observation without changing state
        return obs

    def get_location(self) -> str:
        """
        Get the current location description.

        Returns:
            String describing the current location
        """
        # Execute 'look' command and return the result
        obs, _, _, _ = self.env.step('look')
        return obs

    def save_state(self) -> Dict[str, Any]:
        """
        Save the current game state.

        Returns:
            Dict containing the saved game state
        """
        return self.env.get_state()

    def load_state(self, state: Dict[str, Any]) -> None:
        """
        Load a previously saved game state.

        Args:
            state: Game state dict from save_state
        """
        self.env.set_state(state)
