"""
Rule-based planner module for the Zork AI agent.

This module provides rule-based action generation and planning capabilities
for the agent. It is responsible for:
1. Generating actions based on observations and memory using predefined rules
2. Validating actions against the environment's valid actions
3. Implementing strategies for exploration and puzzle-solving

The rule-based planner uses a set of handcrafted rules to determine actions,
in contrast to the LLM-based planner which uses a language model.
"""
from typing import List, Any, Tuple


class RuleBasedPlanner:
    """
    Rule-based action planner for the Zork AI agent.
    
    This class is responsible for generating actions based on
    observations and memory using predefined rules, and validating
    them against the environment's valid actions.
    
    It uses a set of handcrafted rules to determine actions, in contrast
    to the LLM-based planner which uses a language model.
    """

    def __init__(self):
        """
        Initialize the action planner.
        
        Sets up the basic data structures and configuration for action planning.
        """
        # Common verbs used in text adventures
        self.common_verbs = [
            # Movement
            "go", "move", "walk", "run",
            # Object interaction
            "take", "get", "pick", "grab",
            # Object placement
            "drop", "put", "place",
            # Observation
            "examine", "look", "inspect", "read",
            # Container interaction
            "open", "close", "unlock", "lock",
            # Manipulation
            "push", "pull", "move", "turn",
            # Consumption
            "eat", "drink",
            # Clothing
            "wear", "remove",
            # Combat
            "attack", "kill", "hit",
            # Inventory
            "inventory", "i",
            # Wait
            "wait", "z",
        ]
        
        # Common directions
        self.directions = [
            # Cardinal directions
            "north", "south", "east", "west",
            # Diagonal directions
            "northeast", "northwest", "southeast", "southwest",
            # Vertical and special directions
            "up", "down", "in", "out",
        ]
        
        # Exploration state
        self.explored_locations = set()
        self.current_goal = None
        self.action_history = []

    def generate_action(
        self, 
        observation: str, 
        valid_actions: List[str], 
        memory: Any
    ) -> str:
        """
        Generate the next action based on observation, valid actions, and memory.
        
        This is a simple rule-based implementation that will be replaced
        with an LLM-based implementation in future iterations.
        
        Args:
            observation: The current observation from the environment
            valid_actions: List of valid actions in the current state
            memory: The agent's memory
            
        Returns:
            The next action to take
        """
        # If we haven't looked around yet, do that first
        recent_look = self.action_history[-3:] if self.action_history else []
        if "look" in valid_actions and "look" not in recent_look:
            self.action_history.append("look")
            return "look"
        
        # If we haven't checked inventory recently, do that
        recent_actions = self.action_history[-5:] if self.action_history else []
        if "inventory" in valid_actions and "inventory" not in recent_actions:
            self.action_history.append("inventory")
            return "inventory"
        
        # If there's a closed mailbox, open it
        obs_lower = observation.lower()
        if ("open mailbox" in valid_actions and "mailbox" in obs_lower and 
                "closed mailbox" in obs_lower):
            self.action_history.append("open mailbox")
            return "open mailbox"
        
        print(f"can take leaflet? {'take leaflet' in valid_actions}")
        print(f"leaflet object? {'leaflet' in obs_lower}")

        print(f"can examine window? {'examine window' in valid_actions}")
        print(f"window object? {'window' in obs_lower}")

        # If there's a leaflet mentioned and we don't have it, take it
        if "take leaflet" in valid_actions and "leaflet" in obs_lower:
            self.action_history.append("take leaflet")
            return "take leaflet"
            
        # If there's a leaflet in the mailbox, take it
        if ("leaflet" in obs_lower and "mailbox" in obs_lower and 
                "take leaflet" in valid_actions):
            self.action_history.append("take leaflet")
            return "take leaflet"
            
        # If there's a leaflet mentioned, try to take it (more general rule)
        if "leaflet" in obs_lower and "take leaflet" in valid_actions:
            self.action_history.append("take leaflet")
            return "take leaflet"
            
        # If there's a window mentioned, try to examine it
        if "window" in obs_lower and "examine window" in valid_actions:
            self.action_history.append("examine window")
            return "examine window"
            
        # If there's a window that's ajar, try to open it
        if "window" in obs_lower and "ajar" in obs_lower and "open window" in valid_actions:
            self.action_history.append("open window")
            return "open window"
            
        # If there's an open window, try to go through it
        if "window" in obs_lower and "open" in obs_lower and "enter window" in valid_actions:
            self.action_history.append("enter window")
            return "enter window"
         
        # If we have a leaflet, try to read it (try different variations)
        inventory_str = str(memory.get_inventory()).lower() if memory else ""
        
        # Check if we've read or examined the leaflet recently
        recent_actions = self.action_history[-25:] if self.action_history else []
        read_recently = "read leaflet" in recent_actions
        examined_recently = "examine leaflet" in recent_actions
        
        # Try "read leaflet" if available and we haven't read it recently
        if "read leaflet" in valid_actions and "leaflet" in inventory_str and not read_recently:
            self.action_history.append("read leaflet")
            return "read leaflet"
            
        # Try just "read" if available and we have a leaflet and haven't read it recently
        if "read" in valid_actions and "leaflet" in inventory_str and not read_recently:
            self.action_history.append("read")
            return "read"
            
        # Try "examine leaflet" if available and we haven't examined it recently
        if "examine leaflet" in valid_actions and "leaflet" in inventory_str and not examined_recently:
            self.action_history.append("examine leaflet")
            return "examine leaflet"
        
        # Try to move in a direction we haven't explored
        recent_moves = self.action_history[-8:] if self.action_history else []
        for direction in self.directions:
            action = f"go {direction}"
            if action in valid_actions and action not in recent_moves:
                self.action_history.append(action)
                return action
        
        # If all else fails, try a random valid action
        import random
        action = random.choice(valid_actions)
        self.action_history.append(action)
        return action

    def validate_action(self, action: str, valid_actions: List[str]) -> Tuple[bool, str]:
        """
        Validate an action against the list of valid actions.
        
        Args:
            action: The action to validate
            valid_actions: List of valid actions in the current state
            
        Returns:
            A tuple of (is_valid, corrected_action)
        """
        # Check if the action is already valid
        if action in valid_actions:
            return True, action
        
        # Check if a similar action is valid
        action_lower = action.lower()
        for valid_action in valid_actions:
            if action_lower in valid_action.lower():
                return True, valid_action
            
            # Check if the action is a direction without "go"
            if action_lower in self.directions:
                go_action = f"go {action_lower}"
                if go_action in valid_actions:
                    return True, go_action
        
        # Action is not valid
        return False, action

    def update_exploration_state(self, observation: str, memory: Any) -> None:
        """
        Update the exploration state based on the observation and memory.
        
        Args:
            observation: The current observation from the environment
            memory: The agent's memory
        """
        # Track explored locations
        if memory and memory.current_location:
            self.explored_locations.add(memory.current_location)
