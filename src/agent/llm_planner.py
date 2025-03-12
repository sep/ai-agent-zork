"""
LLM-based planner module for the Zork AI agent.

This module provides an LLM-powered action generation and planning capabilities
for the agent. It is responsible for:
1. Generating actions based on observations, memory, and context
2. Validating actions against the environment's valid actions
3. Implementing advanced strategies for exploration and puzzle-solving

The LLM planner extends the RuleBasedPlanner with more sophisticated
reasoning and contextual understanding.
"""
from typing import List, Any, Dict, Optional
import os
import json
import time
import requests
from dotenv import load_dotenv
from .rule_based_planner import RuleBasedPlanner

# Load environment variables from .env file
load_dotenv()


class LLMBasedPlanner(RuleBasedPlanner):
    """
    LLM-powered action planner for the Zork AI agent.
    
    This class extends the RuleBasedPlanner with LLM capabilities
    for more sophisticated action generation and planning.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: str = None):
        """
        Initialize the LLM action planner.
        
        Args:
            model_name: The name of the LLM model to use
            api_key: The API key for the LLM provider (defaults to environment variable)
        """
        super().__init__()
        self.model_name = model_name
        # Try to get API key from provided argument, then environment variable
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.context_window = []
        self.max_context_items = 10
        self.system_prompt = self._create_system_prompt()
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
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
        # Check if API key is available
        if not self.api_key:
            print("No API key found. Set OPENAI_API_KEY environment variable.")
            print("Falling back to rule-based planner.")
            return super().generate_action(observation, valid_actions, memory)
        
        # Create the prompt for the LLM
        prompt = self._create_llm_prompt(observation, valid_actions, memory)
        
        # Prepare the API request
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 50,
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0
        }
        
        # Make the API request with retries
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                # Check if the request was successful
                if response.status_code == 200:
                    result = response.json()
                    action = result["choices"][0]["message"]["content"].strip()
                    print(f"LLM generated action: {action}")
                    return action
                
                # Handle rate limiting
                if response.status_code == 429:
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                
                # Handle other errors
                print(f"API error: {response.status_code} - {response.text}")
                break
                
            except Exception as e:
                print(f"Error calling LLM API: {str(e)}")
                if attempt < self.max_retries - 1:
                    wait_time = self.retry_delay * (2 ** attempt)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    break
        
        # Fall back to rule-based planner if API call fails
        print("LLM API call failed. Falling back to rule-based planner.")
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
