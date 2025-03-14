"""
MCP LangGraph workflow for the Zork AI agent.

This module implements a LangGraph workflow for an agent that uses MCP tools
to interact with the Zork environment. The agent explicitly selects tools and
provides parameters, rather than generating text commands directly.
"""
from typing import Any, Dict, List, TypedDict, Optional, Tuple, cast
import os
import json
import re
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
    max_steps: int = 20
) -> Tuple[StateGraph, Dict[str, Any]]:
    """
    Create a LangGraph workflow for the MCP Zork AI agent.
    
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
        print("In observe node")
        # If this is the first step, reset the environment
        if state.get("observation") is None:
            print("Resetting environment")
            env_state = environment.reset()
            print(f"Environment reset: {env_state}")
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
        print("Returning current state")
        return state
    
    def think(state: AgentState) -> AgentState:
        """
        Generate a thought about what to do next.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with a thought
        """
        print("In think node")
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
        try:
            print("Calling LLM for thought...")
            messages = [
                SystemMessage(content="You are an expert text adventure game player."),
                HumanMessage(content=prompt)
            ]
            response = llm.invoke(messages)
            print(f"LLM response for thought: {response.content[:100]}...")
            
            # Update the state with the thought
            state["thought"] = response.content
        except Exception as e:
            print(f"Error generating thought: {e}")
            state["thought"] = "I should look around to see what's here."
        
        return state
    
    def select_tool(state: AgentState) -> AgentState:
        """
        Select a tool to use based on the thought.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with a selected tool
        """
        print("In select_tool node")
        
        # Try to get the available tools from the MCP server
        try:
            from src.mcp.client import get_mcp_tools
            
            # Get the server name from the environment if available
            server_name = getattr(environment, 'server_name', "zork-tools")
            
            # Get the available tools from the MCP server
            tools = get_mcp_tools(server_name)
            
            # Build the tool descriptions and examples
            tool_descriptions = ""
            tool_examples = ""
            available_tools = {}
            
            for tool in tools:
                # Add the tool description
                tool_name = tool.get("name", "")
                if not tool_name:
                    continue
                    
                description = tool.get("description", "")
                tool_descriptions += f"- {tool_name}: {description}\n"
                
                # Add the tool to available_tools
                input_schema = tool.get("inputSchema", {})
                required = input_schema.get("required", [])
                available_tools[tool_name] = {"required": required}
                
                # Get examples from the tool definition if available
                examples = tool.get("examples", [])
                if examples:
                    for example in examples:
                        # Add the example to the prompt
                        example_json = {
                            "tool": tool_name,
                            "args": example.get("args", {})
                        }
                        example_name = example.get("name", f"Example for {tool_name}")
                        tool_examples += f"{example_name}: {json.dumps(example_json)}\n"
                else:
                    # If no examples are provided, generate one based on the schema
                    properties = input_schema.get("properties", {})
                    
                    # Build the example arguments
                    example_args = {}
                    for param_name, param_schema in properties.items():
                        if param_name in required:
                            # Use an example value based on the parameter name
                            if param_name == "direction":
                                example_args[param_name] = "north"
                            elif param_name == "object":
                                example_args[param_name] = "mailbox"
                            elif param_name == "container":
                                example_args[param_name] = "mailbox"
                            else:
                                example_args[param_name] = "example"
                    
                    # Add the example to the prompt
                    example = {
                        "tool": tool_name,
                        "args": example_args
                    }
                    tool_examples += f"Example for {tool_name}: {json.dumps(example)}\n"
        except (ImportError, Exception) as e:
            print(f"Error getting MCP tools: {e}")
            # Fall back to default tools
            tools = []
            tool_descriptions = ""
            tool_examples = ""
            available_tools = {
                "navigate": {"required": ["direction"]},
                "examine": {"required": ["object"]},
                "take": {"required": ["object"]},
                "drop": {"required": ["object"]},
                "inventory": {"required": []},
                "read": {"required": ["object"]},
                "look": {"required": []},
                "open": {"required": ["object"]},
                "close": {"required": ["object"]},
                "put": {"required": ["object", "container"]}
            }
        
        # If no tools were found, use default descriptions and examples
        if not tools:
            tool_descriptions = """
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
            """
            
            tool_examples = """
            Example for navigate: {"tool": "navigate", "args": {"direction": "north"}}
            Example for examine: {"tool": "examine", "args": {"object": "mailbox"}}
            Example for take: {"tool": "take", "args": {"object": "leaflet"}}
            Example for drop: {"tool": "drop", "args": {"object": "sword"}}
            Example for inventory: {"tool": "inventory", "args": {}}
            Example for read: {"tool": "read", "args": {"object": "leaflet"}}
            Example for look: {"tool": "look", "args": {}}
            Example for open: {"tool": "open", "args": {"object": "mailbox"}}
            Example for close: {"tool": "close", "args": {"object": "mailbox"}}
            Example for put: {"tool": "put", "args": {"object": "leaflet", "container": "mailbox"}}
            """
            
            valid_tool_names = ["navigate", "examine", "take", "drop", "inventory", "read", "look", "open", "close", "put"]
        
        # Create a prompt for the LLM with more detailed instructions
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
        {tool_descriptions}
        
        Select the most appropriate tool and provide its parameters in JSON format.
        
        {tool_examples}
        
        Your response must be valid JSON with a "tool" field and an "args" object containing the required parameters.
        
        Your tool selection (JSON format):
        """
        
        # Generate a tool selection using the LLM
        try:
            print("Calling LLM for tool selection...")
            messages = [
                SystemMessage(content="You are an expert text adventure game player."),
                HumanMessage(content=prompt)
            ]
            response = llm.invoke(messages)
            print(f"LLM response for tool selection: {response.content[:100]}...")
        except Exception as e:
            print(f"Error generating tool selection: {e}")
            state["tool_name"] = "look"
            state["tool_args"] = {}
            return state
        
        # Parse the tool selection with improved error handling
        try:
            # Extract JSON from the response
            content = response.content
            
            # If the response contains a code block, extract it
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            print(f"Original response: {content}")
            
            # Try to extract the tool name and args directly
            tool_name = "look"  # Default
            tool_args = {}
            
            # Try to parse as JSON first
            try:
                # Try to parse the content as JSON
                parsed = json.loads(content)
                if "tool" in parsed:
                    tool_name = parsed["tool"].lower()  # Normalize to lowercase
                if "args" in parsed and isinstance(parsed["args"], dict):
                    tool_args = parsed["args"]
            except json.JSONDecodeError:
                print("JSON parsing failed, falling back to regex extraction")
                # If that fails, use regex to extract the tool name and args with improved patterns
                
                # Extract tool name
                tool_match = re.search(r'"tool"\s*:\s*"([^"]+)"', content)
                if tool_match:
                    tool_name = tool_match.group(1).lower()  # Normalize to lowercase
                
                # Extract all possible arguments using a more general pattern
                arg_matches = re.findall(r'"([^"]+)"\s*:\s*"([^"]+)"', content)
                for key, value in arg_matches:
                    if key != "tool":  # Skip the tool name
                        tool_args[key] = value
            
            # Validate the tool name
            if tool_name not in available_tools:
                print(f"Invalid tool name: {tool_name}, defaulting to look")
                tool_name = "look"
                tool_args = {}
            
            # Validate required arguments
            required_args = available_tools[tool_name]["required"]
            missing_args = [arg for arg in required_args if arg not in tool_args]
            
            if missing_args:
                print(f"Missing required arguments for {tool_name}: {missing_args}")
                # If we're missing required arguments, try to infer them from the thought
                for arg in missing_args:
                    if arg == "object" and "object" in state["thought"].lower():
                        # Try to extract an object from the thought
                        objects = re.findall(r'\b(mailbox|leaflet|sword|lamp|house|door|window|rug)\b', state["thought"].lower())
                        if objects:
                            tool_args["object"] = objects[0]
                            print(f"Inferred object from thought: {objects[0]}")
                    elif arg == "direction" and any(dir in state["thought"].lower() for dir in ["north", "south", "east", "west", "up", "down"]):
                        # Try to extract a direction from the thought
                        directions = re.findall(r'\b(north|south|east|west|up|down)\b', state["thought"].lower())
                        if directions:
                            tool_args["direction"] = directions[0]
                            print(f"Inferred direction from thought: {directions[0]}")
            
            # If we still have missing required arguments, default to look
            missing_args = [arg for arg in required_args if arg not in tool_args]
            if missing_args:
                print(f"Still missing required arguments, defaulting to look")
                tool_name = "look"
                tool_args = {}
            
            print(f"Extracted tool: {tool_name}, args: {tool_args}")
            
            # Create the tool selection
            tool_selection = {"tool": tool_name, "args": tool_args}
            
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
        print("In act node")
        # Get the selected tool and arguments
        tool_name = state["tool_name"]
        tool_args = state["tool_args"] or {}
        
        # Create a descriptive action string for logging
        if tool_name == "navigate":
            action = f"go {tool_args.get('direction', '')}"
        elif tool_name == "examine":
            action = f"examine {tool_args.get('object', '')}"
        elif tool_name == "take":
            action = f"take {tool_args.get('object', '')}"
        elif tool_name == "drop":
            action = f"drop {tool_args.get('object', '')}"
        elif tool_name == "inventory":
            action = "inventory"
        elif tool_name == "read":
            action = f"read {tool_args.get('object', '')}"
        elif tool_name == "look":
            action = "look"
        elif tool_name == "open":
            action = f"open {tool_args.get('object', '')}"
        elif tool_name == "close":
            action = f"close {tool_args.get('object', '')}"
        elif tool_name == "put":
            action = f"put {tool_args.get('object', '')} in {tool_args.get('container', '')}"
        else:
            # Default to look if the tool is not recognized
            print(f"Unrecognized tool: {tool_name}, defaulting to look")
            tool_name = "look"
            tool_args = {}
            action = "look"
        
        try:
            # Check if we can use MCP tools directly
            HAS_MCP = True
            try:
                from src.mcp.client import use_mcp_tool
            except ImportError:
                HAS_MCP = False
                print("MCP client not available, falling back to direct environment calls")
            
            if hasattr(environment, 'server_name') and HAS_MCP:
                # Execute the tool via MCP
                print(f"Using MCP to execute tool: {tool_name}")
                result = use_mcp_tool(environment.server_name, tool_name, tool_args)
            else:
                # Fall back to the mock environment if MCP is not available
                print("Falling back to direct environment calls")
                
                # Map the tools to environment commands
                if tool_name == "navigate":
                    direction = tool_args.get("direction", "")
                    result = environment.step(f"go {direction}")
                elif tool_name == "examine":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"examine {obj}")
                elif tool_name == "take":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"take {obj}")
                elif tool_name == "drop":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"drop {obj}")
                elif tool_name == "inventory":
                    result = environment.step("inventory")
                elif tool_name == "read":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"read {obj}")
                elif tool_name == "look":
                    result = environment.step("look")
                elif tool_name == "open":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"open {obj}")
                elif tool_name == "close":
                    obj = tool_args.get("object", "")
                    result = environment.step(f"close {obj}")
                elif tool_name == "put":
                    obj = tool_args.get("object", "")
                    container = tool_args.get("container", "")
                    result = environment.step(f"put {obj} in {container}")
                else:
                    # Default to look if the tool is not recognized
                    print(f"Unrecognized tool: {tool_name}, defaulting to look")
                    result = environment.step("look")
        except Exception as e:
            # Handle any errors that occur during tool execution
            print(f"Error executing tool {tool_name}: {e}")
            result = {
                "observation": f"Error executing tool {tool_name}: {e}",
                "score": state["score"],
                "done": state["done"],
                "moves": state["moves"] + 1,
                "valid_actions": state["valid_actions"],
                "inventory": state["inventory"],
                "location": state["location"]
            }
        
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
    
    # Keep track of action history to detect loops
    action_history = []
    
    def should_continue(state: AgentState) -> str:
        """
        Determine whether to continue or end the workflow.
        
        Args:
            state: The current state
            
        Returns:
            "continue" or "end"
        """
        # End if the game is over or we've reached the maximum number of steps
        print(f"Checking if should continue: done={state['done']}, moves={state['moves']}, max_steps={max_steps}")
        if state["done"] or state["moves"] >= max_steps:
            print("Ending workflow")
            return "end"
        
        # Check for action loops (always enabled)
        nonlocal action_history
        current_action = (state["tool_name"], str(state["tool_args"]))
        action_history.append(current_action)
        
        # Check if the same action has been repeated 3 times in a row
        if len(action_history) >= 3:
            last_three = action_history[-3:]
            if last_three.count(current_action) == 3:
                print("Detected action loop, ending workflow")
                return "end"
        
        # Limit action history to last 10 actions to save memory
        action_history = action_history[-10:]
        
        print("Continuing workflow")
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
    max_steps: int = 20,
    recursion_limit: int = 100
) -> None:
    """
    Run the agent workflow.
    
    Args:
        environment: The environment to interact with
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider
        max_steps: Maximum number of steps to run
        recursion_limit: Maximum recursion depth for the LangGraph workflow
    """
    # Create the workflow
    workflow, initial_state = create_agent_workflow(
        environment=environment,
        model_name=model_name,
        api_key=api_key,
        max_steps=max_steps
    )
    
    # Run the workflow
    print("Starting workflow...")
    # Create a config dictionary with the recursion limit
    config = {"recursion_limit": recursion_limit}
    for i, state in enumerate(workflow.stream(initial_state, config=config)):
        node = state.get("__metadata__", {}).get("name", "")
        print(f"Processing node: {node}")
        
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
    
    # Get the final state directly from the environment
    env_state = environment.step("look")
    
    # Print the final stats
    print("\n" + "="*60)
    print("FINAL STATS")
    print("="*60)
    
    # Use the environment's state for the final stats, but subtract 1 from moves
    # because we added an extra "look" action to get the final state
    print(f"Steps: {env_state['moves'] - 1}")
    print(f"Score: {env_state['score']}")
    print(f"Inventory: {env_state['inventory']}")
