"""
MCP Zork Agent.

This module implements a direct MCP agent that uses MCP tools directly to play Zork.
The agent follows a deliberative process: first thinking about what to do,
then selecting a tool and parameters based on that thought.
"""
import os
import time
import json
from typing import Any, Dict, List, Tuple
from dotenv import load_dotenv
from openai import OpenAI

from src.mcp.client import use_mcp_tool

# Load environment variables from .env file
load_dotenv()

# MCP server name for Zork tools
MCP_SERVER_NAME = "zork-tools"


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
    print("It follows a deliberative process: first thinking, then selecting a tool.")
    print("Press Ctrl+C to stop the agent.")
    
    try:
        # Initialize the game state
        game_state = {
            "observation": "",
            "location": "",
            "inventory": [],
            "score": 0,
            "moves": 0,
            "done": False
        }
        
        # Reset the game by calling the look tool
        result = use_mcp_tool(MCP_SERVER_NAME, "look", {})
        game_state["observation"] = result["observation"]
        game_state["location"] = result.get("location", "")
        
        # Get initial inventory
        inv_result = use_mcp_tool(MCP_SERVER_NAME, "inventory", {})
        game_state["inventory"] = inv_result.get("inventory", [])
        
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
            
            # Select a tool and parameters using the LLM
            tool_name, tool_args = select_tool(client, model_name, game_state, thought)
            print(f"\nTool: {tool_name}")
            print(f"Args: {tool_args}")
            
            # Execute the tool
            try:
                result = use_mcp_tool(MCP_SERVER_NAME, tool_name, tool_args)
                
                # Update the game state
                game_state["observation"] = result["observation"]
                game_state["score"] = result.get("score", game_state["score"])
                game_state["moves"] += 1
                game_state["inventory"] = result.get("inventory", game_state["inventory"])
                game_state["location"] = result.get("location", game_state["location"])
                
                # Check for game completion
                if "you have died" in game_state["observation"].lower() or "game over" in game_state["observation"].lower():
                    game_state["done"] = True
            except Exception as e:
                print(f"Error executing tool {tool_name}: {e}")
                game_state["observation"] = f"Error executing tool {tool_name}: {e}"
            
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


def select_tool(client: OpenAI, model_name: str, game_state: Dict[str, Any],
                thought: str) -> Tuple[str, Dict[str, Any]]:
    """
    Select a tool and parameters based on the thought.
    
    Args:
        client: The OpenAI client
        model_name: The name of the LLM model to use
        game_state: The current game state
        thought: The thought about what to do next
        
    Returns:
        A tuple of (tool_name, tool_args)
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
    
    Available Tools:
    - navigate: Move in a specified direction (north, south, east, west, up, down)
    - examine: Examine an object in the environment
    - take: Take an object
    - drop: Drop an object from your inventory
    - inventory: Check your inventory
    - read: Read an object with text
    - look: Look around to get a description of your surroundings
    - open: Open a container or door
    - close: Close a container or door
    - put: Put an object into a container
    
    Select the most appropriate tool and provide its parameters in JSON format.
    
    Example for navigate: {{"tool": "navigate", "args": {{"direction": "north"}}}}
    Example for examine: {{"tool": "examine", "args": {{"object": "mailbox"}}}}
    Example for take: {{"tool": "take", "args": {{"object": "leaflet"}}}}
    Example for drop: {{"tool": "drop", "args": {{"object": "sword"}}}}
    Example for inventory: {{"tool": "inventory", "args": {{}}}}
    Example for read: {{"tool": "read", "args": {{"object": "leaflet"}}}}
    Example for look: {{"tool": "look", "args": {{}}}}
    Example for open: {{"tool": "open", "args": {{"object": "mailbox"}}}}
    Example for close: {{"tool": "close", "args": {{"object": "mailbox"}}}}
    Example for put: {{"tool": "put", "args": {{"object": "leaflet", "container": "mailbox"}}}}
    
    Your response must be valid JSON with a "tool" field and an "args" object containing the required parameters.
    
    Your tool selection (JSON format):
    """
    
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an expert text adventure game player."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the tool selection
    content = response.choices[0].message.content.strip()
    
    # If the response contains a code block, extract it
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0].strip()
    elif "```" in content:
        content = content.split("```")[1].split("```")[0].strip()
    
    try:
        # Try to parse the content as JSON
        parsed = json.loads(content)
        tool_name = parsed.get("tool", "look").lower()  # Default to look
        tool_args = parsed.get("args", {})
        
        # Validate the tool name
        if tool_name not in ["navigate", "examine", "take", "drop", "inventory", "read", "look", "open", "close", "put"]:
            print(f"Invalid tool name: {tool_name}, defaulting to look")
            tool_name = "look"
            tool_args = {}
        
        # Validate required arguments
        if tool_name == "navigate" and "direction" not in tool_args:
            print("Missing required argument 'direction' for navigate, defaulting to look")
            tool_name = "look"
            tool_args = {}
        elif tool_name in ["examine", "take", "drop", "read", "open", "close"] and "object" not in tool_args:
            print(f"Missing required argument 'object' for {tool_name}, defaulting to look")
            tool_name = "look"
            tool_args = {}
        elif tool_name == "put" and ("object" not in tool_args or "container" not in tool_args):
            print("Missing required arguments for put, defaulting to look")
            tool_name = "look"
            tool_args = {}
    except json.JSONDecodeError:
        print("Error parsing JSON, defaulting to look")
        tool_name = "look"
        tool_args = {}
    
    return tool_name, tool_args
