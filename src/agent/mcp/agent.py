"""
MCP Zork Agent.

This module implements a direct MCP agent that uses the MCP environment to play Zork.
The agent follows a deliberative process: first thinking about what to do,
then selecting an action based on that thought.
"""
import os
import time
from typing import Any, Dict
from dotenv import load_dotenv
from openai import OpenAI

from src.mcp.environment import create_environment

# Load environment variables from .env file
load_dotenv()


def run_agent(model_name: str = "gpt-3.5-turbo", api_key: str = None,
              max_steps: int = 20, debug: bool = False):
    """
    Run the agent.
    
    Args:
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider
        max_steps: Maximum number of steps to run
        debug: Whether to print debug information
    """
    # Initialize the LLM
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    client = OpenAI(api_key=api_key)
    
    print("\n" + "="*60)
    print("MCP ZORK AGENT")
    print("="*60)
    print(f"This agent uses {model_name} to play Zork.")
    print("It follows a deliberative process: first thinking, then acting.")
    print("Press Ctrl+C to stop the agent.")
    
    # Create the environment
    env = create_environment(debug=debug)
    
    try:
        # Initialize the environment
        game_state = env.reset()
        
        # Main loop
        for step in range(max_steps):
            # Print the current state
            print("\n" + "="*60)
            print(f"STEP {step+1}")
            print("="*60)
            print(f"Location: {game_state['location']}")
            print(f"Observation: {game_state['observation']}")
            print(f"Inventory: {game_state['inventory']}")
            print(f"Score: {game_state['score']}")
            print(f"Moves: {game_state['moves']}")
            
            # Generate a thought using the LLM
            thought = generate_thought(client, model_name, game_state)
            print(f"\nThought: {thought}")
            
            # Select an action using the LLM
            action = select_action(client, model_name, game_state, thought)
            print(f"\nAction: {action}")
            
            # Execute the action
            game_state = env.step(action)
            
            # Check if the game is done
            if game_state["done"]:
                break
            
            # Add a small delay to make the output more readable
            time.sleep(1)
        
        # Print final stats
        print("\n" + "="*60)
        print("FINAL STATS")
        print("="*60)
        print(f"Steps: {game_state['moves']}")
        print(f"Score: {game_state['score']}")
        print(f"Inventory: {game_state['inventory']}")
    
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
    
    except Exception as e:
        print(f"\nError running agent: {e}")


def generate_thought(client: OpenAI, model_name: str, game_state: Dict[str, Any]) -> str:
    """
    Generate a thought about what to do next.
    
    Args:
        client: The OpenAI client
        model_name: The name of the LLM model to use
        game_state: The current game state
        
    Returns:
        A thought about what to do next
    """
    prompt = f"""
    You are an expert text adventure game player. You are playing Zork.
    
    Current Observation:
    {game_state["observation"]}
    
    Current Location:
    {game_state["location"]}
    
    Inventory:
    {game_state["inventory"]}
    
    Score: {game_state["score"]}
    Moves: {game_state["moves"]}
    
    Think step by step about what to do next. Consider:
    1. What is happening in the game?
    2. What are your goals?
    3. What actions can you take?
    4. What would be the best action to take?
    
    Your thought process:
    """
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert text adventure game player."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content


def select_action(client: OpenAI, model_name: str, game_state: Dict[str, Any],
                 thought: str) -> str:
    """
    Select an action to take based on the thought.
    
    Args:
        client: The OpenAI client
        model_name: The name of the LLM model to use
        game_state: The current game state
        thought: The thought about what to do next
        
    Returns:
        An action to take
    """
    prompt = f"""
    You are an expert text adventure game player. You are playing Zork.
    
    Current Observation:
    {game_state["observation"]}
    
    Current Location:
    {game_state["location"]}
    
    Inventory:
    {game_state["inventory"]}
    
    Your Thought:
    {thought}
    
    Select a single action to take. Your response should be just the action, nothing else.
    For example: "look", "go north", "take leaflet", etc.
    
    Your action:
    """
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert text adventure game player."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content.strip()
