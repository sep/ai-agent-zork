"""
LLM-based planner module for the Zork AI agent.

This module provides an LLM-powered action generation and planning capabilities
for the agent. It is responsible for:
1. Generating actions based on observations, memory, and context
2. Validating actions against the environment's valid actions
3. Implementing advanced strategies for exploration and puzzle-solving

The LLM planner extends the rule-based planner with more sophisticated
reasoning and contextual understanding.
"""
from typing import List, Any, Dict, Optional
import os
import json
from .planner import ActionPlanner


class LLMActionPlanner(ActionPlanner):
    """
    LLM-powered action planner for the Zork AI agent.
    
    This class extends the rule-based ActionPlanner with LLM capabilities
    for more sophisticated action generation and planning.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the LLM action planner.
        
        Args:
            model_name: The name of the LLM model to use
        """
        super().__init__()
        self.model_name = model_name
        self.context_window = []
        self.max_context_items = 10
        self.system_prompt = self._create_system_prompt()
        
    def _create_system_prompt(self) -> str:
        """
        Create the system prompt for the LLM.
        
        Returns:
            The system prompt string
        """
        return """
        You are an expert text adventure game player. Your task is to generate the next action
        for an AI agent playing Zork. You will be given:
        
        1. The current observation from the game
        2. A list of valid actions in the current state
        3. The agent's inventory
        4. Recent actions taken by the agent
        5. The agent's current location
        
        Your goal is to generate a single action that will help the agent make progress in the game.
        The action must be one of the valid actions provided. Focus on:
        
        - Exploration: Systematically exploring the game world
        - Object interaction: Taking, examining, and using objects appropriately
        - Puzzle solving: Identifying and solving puzzles
        - Goal tracking: Working toward game objectives
        
        Return ONLY the next action to take, with no additional explanation or commentary.
        """
    
    def generate_action(
        self, 
        observation: str, 
        valid_actions: List[str], 
        memory: Any
    ) -> str:
        """
        Generate the next action using the LLM.
        
        Args:
            observation: The current observation from the environment
            valid_actions: List of valid actions in the current state
            memory: The agent's memory
            
        Returns:
            The next action to take
        """
        # Fall back to rule-based planner if no valid actions
        if not valid_actions:
            return super().generate_action(observation, valid_actions, memory)
        
        # Update context with current state
        self._update_context(observation, valid_actions, memory)
        
        # Generate action using LLM
        action = self._generate_llm_action(observation, valid_actions, memory)
        
        # Validate the action
        is_valid, corrected_action = self.validate_action(action, valid_actions)
        
        # Use the corrected action if the original was invalid
        if not is_valid:
            print(f"Invalid action '{action}' corrected to '{corrected_action}'")
            action = corrected_action
        
        # Add the action to history
        self.action_history.append(action)
        
        return action
    
    def _update_context(
        self, 
        observation: str, 
        valid_actions: List[str], 
        memory: Any
    ) -> None:
        """
        Update the context window with the current state.
        
        Args:
            observation: The current observation from the environment
            valid_actions: List of valid actions in the current state
            memory: The agent's memory
        """
        # Create a context item with the current state
        context_item = {
            "observation": observation,
            "valid_actions": valid_actions[:20],  # Limit to 20 actions to save context space
            "inventory": memory.get_inventory() if memory else [],
            "location": memory.current_location if memory else "unknown",
            "recent_actions": self.action_history[-5:] if self.action_history else []
        }
        
        # Add to context window
        self.context_window.append(context_item)
        
        # Maintain maximum context window size
        if len(self.context_window) > self.max_context_items:
            self.context_window.pop(0)
    
    def _generate_llm_action(
        self, 
        observation: str, 
        valid_actions: List[str], 
        memory: Any
    ) -> str:
        """
        Generate an action using the LLM.
        
        Args:
            observation: The current observation from the environment
            valid_actions: List of valid actions in the current state
            memory: The agent's memory
            
        Returns:
            The generated action
        """
        # Create the prompt for the LLM
        prompt = self._create_llm_prompt(observation, valid_actions, memory)
        
        # TODO: Implement actual LLM call here
        # For now, fall back to rule-based planner
        print("LLM integration not implemented yet. Falling back to rule-based planner.")
        return super().generate_action(observation, valid_actions, memory)
    
    def _create_llm_prompt(
        self, 
        observation: str, 
        valid_actions: List[str], 
        memory: Any
    ) -> str:
        """
        Create the prompt for the LLM.
        
        Args:
            observation: The current observation from the environment
            valid_actions: List of valid actions in the current state
            memory: The agent's memory
            
        Returns:
            The prompt string
        """
        inventory_str = str(memory.get_inventory()) if memory else "[]"
        location_str = memory.current_location if memory else "unknown"
        recent_actions_str = str(self.action_history[-5:]) if self.action_history else "[]"
        
        prompt = f"""
        Current Observation:
        {observation}
        
        Valid Actions:
        {', '.join(valid_actions[:20])}
        
        Inventory:
        {inventory_str}
        
        Current Location:
        {location_str}
        
        Recent Actions:
        {recent_actions_str}
        
        Generate the next action:
        """
        
        return prompt
