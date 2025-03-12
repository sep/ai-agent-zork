"""
Memory module for the Zork AI agent.

This module provides the memory system for the agent, allowing it to:
1. Store observations and actions
2. Track game state changes
3. Retrieve historical information

The memory system is implemented using a bottom-up approach, starting with
basic storage and gradually adding more complex features.
"""
from typing import Dict, List, Any, Optional
from datetime import datetime


class AgentMemory:
    """
    Memory system for the Zork AI agent.
    
    This class provides storage and retrieval of game history and state
    information.
    It starts with basic functionality and will be extended with more advanced
    features in future iterations.
    """

    def __init__(self):
        """
        Initialize the agent memory with empty storage.
        
        Sets up the basic data structures for storing observations, actions,
        and game state information.
        """
        # Raw memory storage - chronological record of everything observed
        # and done
        self.observations: List[Dict[str, Any]] = []
        self.actions: List[Dict[str, Any]] = []
        
        # Current game state tracking
        self.current_location: Optional[str] = None
        self.previous_locations: List[str] = []
        self.inventory: List[str] = []
        self.score: int = 0
        self.moves: int = 0
        
        # Initialize timestamp for memory creation
        self.created_at = datetime.now()
        self.last_updated = self.created_at

    def add_observation(self, observation: str, state: Dict[str, Any]) -> None:
        """
        Add a new observation to memory.
        
        Args:
            observation: The text observation from the environment
            state: The full state object returned by the environment
        """
        # Record the timestamp
        timestamp = datetime.now()
        
        # Extract key information from the state
        location = state.get("location")
        score = state.get("score", 0)
        moves = state.get("moves", 0)
        
        # Create the observation record
        observation_record = {
            "timestamp": timestamp,
            "text": observation,
            "location": location,
            "score": score,
            "moves": moves,
        }
        
        # Add to observations list
        self.observations.append(observation_record)
        
        # Update current game state
        if location and location != self.current_location:
            if self.current_location:
                self.previous_locations.append(self.current_location)
            self.current_location = location
        
        self.score = score
        self.moves = moves
        self.last_updated = timestamp

    def add_action(self, action: str, result: Dict[str, Any]) -> None:
        """
        Add a performed action to memory.
        
        Args:
            action: The text action performed by the agent
            result: The result of the action (from environment.step())
        """
        # Record the timestamp
        timestamp = datetime.now()
        
        # Determine if the action was successful
        # For now, we'll consider any action that doesn't contain an error
        # message as successful
        # This is a simple heuristic and will be improved in future iterations
        observation = result.get("observation", "")
        success = not any(error in observation.lower() for error in [
            "you can't", "you don't", "i don't", "nothing happens"
        ])
        
        # Create the action record
        action_record = {
            "timestamp": timestamp,
            "text": action,
            "success": success,
            "location": result.get("location"),
            "score_change": result.get("score", 0) - self.score,
        }
        
        # Add to actions list
        self.actions.append(action_record)
        self.last_updated = timestamp

    def get_recent_history(self, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the most recent interactions (observations and actions).
        
        Args:
            n: Number of recent interactions to retrieve
            
        Returns:
            List of recent interactions in chronological order
        """
        # Combine observations and actions
        combined = []
        
        for obs in self.observations:
            combined.append({
                "type": "observation",
                "timestamp": obs["timestamp"],
                "content": obs["text"],
                "location": obs["location"],
            })
        
        for act in self.actions:
            combined.append({
                "type": "action",
                "timestamp": act["timestamp"],
                "content": act["text"],
                "success": act["success"],
            })
        
        # Sort by timestamp
        combined.sort(key=lambda x: x["timestamp"])
        
        # Return the most recent n items
        return combined[-n:] if n < len(combined) else combined

    def get_location_history(self) -> List[str]:
        """
        Get the history of visited locations.
        
        Returns:
            List of visited locations in order of first visit
        """
        # Start with previous locations
        locations = self.previous_locations.copy()
        
        # Add current location if it exists and isn't already in the list
        if self.current_location and self.current_location not in locations:
            locations.append(self.current_location)
        
        return locations

    def get_inventory(self) -> List[str]:
        """
        Get the current inventory.
        
        Returns:
            List of items in inventory
        """
        return self.inventory.copy()

    def update_inventory(self, inventory_text: str) -> None:
        """
        Update the inventory based on inventory text.
        
        Args:
            inventory_text: The text description of the inventory
        """
        # This is a simple implementation that will be improved in future
        # iterations
        # For now, we'll just store the raw inventory text
        self.inventory = []
        
        # Simple parsing of inventory text
        if "You are carrying:" in inventory_text:
            items_text = inventory_text.split("You are carrying:")[1].strip()
            items = [line.strip() for line in items_text.split("\n")]
            
            # Process each item
            for item in items:
                # Remove leading spaces, bullets, etc.
                clean_item = item.lstrip(" •-")
                
                # Extract the basic item name (ignoring status in parentheses)
                if "(" in clean_item:
                    clean_item = clean_item.split("(")[0].strip()
                
                # Add to inventory if not empty
                if clean_item:
                    self.inventory.append(clean_item)

    def __str__(self) -> str:
        """
        Get a string representation of the memory state.
        
        Returns:
            String summary of the memory
        """
        return (
            f"AgentMemory: {len(self.observations)} observations, "
            f"{len(self.actions)} actions, "
            f"Current location: {self.current_location}, "
            f"Score: {self.score}, "
            f"Moves: {self.moves}, "
            f"Inventory: {len(self.inventory)} items"
        )
