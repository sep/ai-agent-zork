"""
LangGraph workflow for the explicit Zork AI agent.

This module implements a LangGraph workflow for an explicit agent that uses MCP tools
to interact with the Zork environment. The agent explicitly selects tools and
provides parameters, rather than generating text commands directly.
"""
from typing import Any, Dict, List, TypedDict, Optional, Tuple, cast
import os
import json
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END


class AgentState(TypedDict):
    """
    State for the agent workflow.
    
    This TypedDict defines the structure of the state that is passed between
    nodes in the workflow graph.
    """
    observation: str  # Current observation from the environment
    thought: str  # Agent's reasoning about what to do next
    action: str  # Action to take in the environment
    score: int  # Current score in the game
    moves: int  # Number of moves taken
    done: bool  # Whether the game is over
    inventory: List[str]  # Items in the inventory
    location: str  # Current location in the game
    valid_actions: List[str]  # Valid actions in the current state
    tool_name: Optional[str]  # Name of the selected tool
    tool_args: Optional[Dict[str, Any]]  # Arguments for the selected tool
    tool_result: Optional[str]  # Result of the tool execution


def create_agent_workflow(
    environment: Any,
    model_name: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    max_steps: int = 100
) -> Tuple[StateGraph, Dict[str, Any]]:
    """
    Create a LangGraph workflow for the explicit Zork AI agent.
    
    Args:
        environment: The environment to interact with
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider
        max_steps: Maximum number of steps to run
        
    Returns:
        A tuple of (workflow, initial_state)
    """
    # Initialize the LLM
    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    
    llm = ChatOpenAI(model=model_name, api_key=api_key)
    
    # Define the workflow nodes
    def observe(state: AgentState) -> AgentState:
        """
        Get the current observation from the environment.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with the current observation
        """
        # If this is the first step, reset the environment
        if state.get("observation") is None:
            env_state = environment.reset()
            return {
                "observation": env_state["observation"],
                "score": env_state["score"],
                "done": env_state["done"],
                "moves": env_state["moves"],
                "valid_actions": env_state["valid_actions"],
                "inventory": env_state["inventory"],
                "location": env_state["location"],
                "thought": "",
                "action": "",
                "tool_name": None,
                "tool_args": None,
                "tool_result": None
            }
        
        # Otherwise, return the current state
        return state
    
    def think(state: AgentState) -> AgentState:
        """
        Generate a thought about what to do next.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with a thought
        """
        # Create a prompt for the LLM
        prompt = f"""
        You are an expert text adventure game player. You are playing Zork.
        
        Current Observation:
        {state["observation"]}
        
        Current Location:
        {state["location"]}
        
        Inventory:
        {state["inventory"]}
        
        Score: {state["score"]}
        Moves: {state["moves"]}
        
        Think step by step about what to do next. Consider:
        1. What is happening in the game?
        2. What are your goals?
        3. What actions can you take?
        4. What would be the best action to take?
        
        Your thought process:
        """
        
        # Generate a thought using the LLM
        messages = [
            SystemMessage(content="You are an expert text adventure game player."),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(messages)
        
        # Update the state with the thought
        state["thought"] = response.content
        
        return state
    
    def select_tool(state: AgentState) -> AgentState:
        """
        Select a tool to use based on the thought.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with a selected tool
        """
        # Create a prompt for the LLM
        prompt = f"""
        You are an expert text adventure game player. You are playing Zork.
        
        Current Observation:
        {state["observation"]}
        
        Current Location:
        {state["location"]}
        
        Inventory:
        {state["inventory"]}
        
        Your Thought:
        {state["thought"]}
        
        Available Tools:
        - navigate: Move in a specified direction (north, south, east, west, up, down)
        - examine: Examine an object in the environment
        - take: Take an object
        - drop: Drop an object from your inventory
        - inventory: Check your inventory
        - read: Read an object with text
        - look: Look around to get a description of your surroundings
        
        Select the most appropriate tool and provide its parameters in JSON format.
        
        Example for navigate: {{"tool": "navigate", "args": {{"direction": "north"}}}}
        Example for examine: {{"tool": "examine", "args": {{"object": "mailbox"}}}}
        Example for take: {{"tool": "take", "args": {{"object": "leaflet"}}}}
        Example for drop: {{"tool": "drop", "args": {{"object": "sword"}}}}
        Example for inventory: {{"tool": "inventory", "args": {{}}}}
        Example for read: {{"tool": "read", "args": {{"object": "leaflet"}}}}
        Example for look: {{"tool": "look", "args": {{}}}}
        
        Your tool selection (JSON format):
        """
        
        # Generate a tool selection using the LLM
        messages = [
            SystemMessage(content="You are an expert text adventure game player."),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(messages)
        
        # Parse the tool selection
        try:
            # Extract JSON from the response
            content = response.content
            
            # If the response contains a code block, extract it
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            tool_selection = json.loads(content)
            
            # Update the state with the selected tool
            state["tool_name"] = tool_selection["tool"]
            state["tool_args"] = tool_selection["args"]
        except Exception as e:
            # If there's an error, default to the look tool
            print(f"Error parsing tool selection: {e}")
            print(f"Response: {response.content}")
            state["tool_name"] = "look"
            state["tool_args"] = {}
        
        return state
    
    def act(state: AgentState) -> AgentState:
        """
        Execute the selected tool.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with the action result
        """
        # Get the selected tool and arguments
        tool_name = state["tool_name"]
        tool_args = state["tool_args"] or {}
        
        # Execute the tool
        # Note: In a real implementation, this would use MCP to call the tools
        # For now, we'll simulate it by mapping to environment commands
        if tool_name == "navigate":
            direction = tool_args.get("direction", "")
            result = environment.step(f"go {direction}")
            action = f"go {direction}"
        elif tool_name == "examine":
            obj = tool_args.get("object", "")
            result = environment.step(f"examine {obj}")
            action = f"examine {obj}"
        elif tool_name == "take":
            obj = tool_args.get("object", "")
            result = environment.step(f"take {obj}")
            action = f"take {obj}"
        elif tool_name == "drop":
            obj = tool_args.get("object", "")
            result = environment.step(f"drop {obj}")
            action = f"drop {obj}"
        elif tool_name == "inventory":
            result = environment.step("inventory")
            action = "inventory"
        elif tool_name == "read":
            obj = tool_args.get("object", "")
            result = environment.step(f"read {obj}")
            action = f"read {obj}"
        elif tool_name == "look":
            result = environment.step("look")
            action = "look"
        else:
            # Default to look if the tool is not recognized
            result = environment.step("look")
            action = "look"
        
        # Update the state with the action result
        state["action"] = action
        state["observation"] = result["observation"]
        state["score"] = result["score"]
        state["done"] = result["done"]
        state["moves"] = result["moves"]
        state["valid_actions"] = result["valid_actions"]
        state["inventory"] = result["inventory"]
        state["location"] = result["location"]
        state["tool_result"] = result["observation"]
        
        return state
    
    def should_continue(state: AgentState) -> str:
        """
        Determine whether to continue or end the workflow.
        
        Args:
            state: The current state
            
        Returns:
            "continue" or "end"
        """
        # End if the game is over or we've reached the maximum number of steps
        if state["done"] or state["moves"] >= max_steps:
            return "end"
        
        return "continue"
    
    # Create the workflow graph
    workflow = StateGraph(AgentState)
    
    # Add the nodes
    workflow.add_node("observe", observe)
    workflow.add_node("think", think)
    workflow.add_node("select_tool", select_tool)
    workflow.add_node("act", act)
    
    # Add the edges
    workflow.add_edge("observe", "think")
    workflow.add_edge("think", "select_tool")
    workflow.add_edge("select_tool", "act")
    workflow.add_conditional_edges(
        "act",
        should_continue,
        {
            "continue": "observe",
            "end": END
        }
    )
    
    # Set the entry point
    workflow.set_entry_point("observe")
    
    # Compile the workflow
    workflow = workflow.compile()
    
    # Create the initial state
    initial_state = cast(AgentState, {
        "observation": None,
        "thought": "",
        "action": "",
        "score": 0,
        "moves": 0,
        "done": False,
        "inventory": [],
        "location": "",
        "valid_actions": [],
        "tool_name": None,
        "tool_args": None,
        "tool_result": None
    })
    
    return workflow, initial_state


def run_agent_workflow(
    environment: Any,
    model_name: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    max_steps: int = 100
) -> None:
    """
    Run the agent workflow.
    
    Args:
        environment: The environment to interact with
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider
        max_steps: Maximum number of steps to run
    """
    # Create the workflow
    workflow, initial_state = create_agent_workflow(
        environment=environment,
        model_name=model_name,
        api_key=api_key,
        max_steps=max_steps
    )
    
    # Run the workflow
    for i, state in enumerate(workflow.stream(initial_state)):
        node = state.get("__metadata__", {}).get("name", "")
        
        if node == "act":
            # Print the step information
            print("\n" + "="*60)
            print(f"STEP {state['moves']}")
            print("="*60)
            
            # Print the thought
            print("Thought:", state["thought"])
            
            # Print the tool selection
            print(f"Tool: {state['tool_name']}")
            print(f"Args: {state['tool_args']}")
            
            # Print the action
            print("Action:", state["action"])
            
            # Print the observation
            print("Observation:", state["observation"])
            
            # Print the game state
            print(f"Location: {state['location']}")
            print(f"Score: {state['score']}")
            print(f"Moves: {state['moves']}")
            print(f"Inventory: {state['inventory']}")
    
    # Print the final stats
    print("\n" + "="*60)
    print("FINAL STATS")
    print("="*60)
    print(f"Steps: {state['moves']}")
    print(f"Score: {state['score']}")
    print(f"Inventory: {state['inventory']}")
