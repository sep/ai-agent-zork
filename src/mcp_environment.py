"""
MCP Environment Wrapper for Zork.

This module provides a wrapper for MCP tools to provide an environment-like interface
that matches the MockZorkEnvironment interface.
"""
from typing import Any, Dict, List, Optional


class MCPEnvironmentWrapper:
    """
    Wrapper for MCP tools to provide an environment-like interface.
    
    This class wraps MCP tools to provide an interface that matches the
    MockZorkEnvironment interface, allowing the agent to use MCP tools
    without changing the agent code.
    """
    
    def __init__(self, server_name: str):
        """
        Initialize the MCP environment wrapper.
        
        Args:
            server_name: The name of the MCP server to use
        """
        self.server_name = server_name
        self.score = 0
        self.moves = 0
        self.current_location = ""
        self.inventory = []
        self.valid_actions = []
        self.done = False
    
    def reset(self) -> Dict[str, Any]:
        """
        Reset the environment.
        
        Returns:
            A dictionary with the initial state
        """
        # Call the look tool to get the initial state
        from langchain_core.utils.function_calling import convert_to_openai_function
        
        # Use the MCP tool to look around
        try:
            from langchain.tools import Tool
            from langchain.agents import AgentExecutor
            
            # Call the look tool
            result = self._use_mcp_tool("look", {})
            
            # Extract the observation
            observation = ""
            for content_item in result.get("content", []):
                if content_item.get("type") == "text":
                    observation += content_item.get("text", "")
            
            # Get the inventory
            inv_result = self._use_mcp_tool("inventory", {})
            inventory = []
            for content_item in inv_result.get("content", []):
                if content_item.get("type") == "json" and "items" in content_item.get("json", {}):
                    inventory = content_item["json"]["items"]
            
            # Reset state variables
            self.score = 0
            self.moves = 0
            self.current_location = "west_of_house"  # Default starting location
            self.inventory = inventory
            self.valid_actions = self._get_valid_actions()
            self.done = False
            
            return {
                "observation": observation,
                "score": self.score,
                "done": self.done,
                "moves": self.moves,
                "valid_actions": self.valid_actions,
                "inventory": self.inventory,
                "location": self.current_location
            }
        except Exception as e:
            print(f"Error resetting MCP environment: {e}")
            # Return a default state
            return {
                "observation": "Error connecting to MCP server.",
                "score": 0,
                "done": True,
                "moves": 0,
                "valid_actions": [],
                "inventory": [],
                "location": ""
            }
    
    def step(self, action: str) -> Dict[str, Any]:
        """
        Take a step in the environment using the appropriate MCP tool.
        
        Args:
            action: The action to take
            
        Returns:
            A dictionary with the new state
        """
        # Increment moves
        self.moves += 1
        
        # Parse the action to determine which tool to use
        tool_name, tool_args = self._parse_action(action)
        
        try:
            # Call the MCP tool
            result = self._use_mcp_tool(tool_name, tool_args)
            
            # Extract the observation
            observation = ""
            for content_item in result.get("content", []):
                if content_item.get("type") == "text":
                    observation += content_item.get("text", "")
            
            # Update state based on the result
            self._update_state(tool_name, result)
            
            # Check for game completion
            if "you have died" in observation.lower() or "game over" in observation.lower():
                self.done = True
            
            return {
                "observation": observation,
                "score": self.score,
                "done": self.done,
                "moves": self.moves,
                "valid_actions": self.valid_actions,
                "inventory": self.inventory,
                "location": self.current_location
            }
        except Exception as e:
            print(f"Error executing MCP tool {tool_name}: {e}")
            return {
                "observation": f"Error executing tool {tool_name}: {e}",
                "score": self.score,
                "done": self.done,
                "moves": self.moves,
                "valid_actions": self.valid_actions,
                "inventory": self.inventory,
                "location": self.current_location
            }
    
    def _parse_action(self, action: str) -> tuple[str, Dict[str, Any]]:
        """
        Parse an action string into tool name and arguments.
        
        Args:
            action: The action string
            
        Returns:
            A tuple of (tool_name, tool_args)
        """
        action = action.lower().strip()
        
        # Handle navigation
        if action.startswith("go "):
            direction = action[3:].strip()
            return "navigate", {"direction": direction}
        elif action in ["north", "south", "east", "west", "up", "down"]:
            return "navigate", {"direction": action}
        
        # Handle examination
        if action.startswith("examine ") or action.startswith("look at "):
            obj = action.split(" ", 2)[-1].strip()
            return "examine", {"object": obj}
        
        # Handle taking objects
        if action.startswith("take ") or action.startswith("get "):
            obj = action.split(" ", 1)[-1].strip()
            return "take", {"object": obj}
        
        # Handle dropping objects
        if action.startswith("drop "):
            obj = action.split(" ", 1)[-1].strip()
            return "drop", {"object": obj}
        
        # Handle inventory
        if action in ["inventory", "i"]:
            return "inventory", {}
        
        # Handle reading
        if action.startswith("read "):
            obj = action.split(" ", 1)[-1].strip()
            return "read", {"object": obj}
        
        # Handle looking
        if action == "look":
            return "look", {}
        
        # Handle opening
        if action.startswith("open "):
            obj = action.split(" ", 1)[-1].strip()
            return "open", {"object": obj}
        
        # Handle closing
        if action.startswith("close "):
            obj = action.split(" ", 1)[-1].strip()
            return "close", {"object": obj}
        
        # Default to look if we can't parse the action
        print(f"Could not parse action: {action}, defaulting to look")
        return "look", {}
    
    def _update_state(self, tool_name: str, result: Dict[str, Any]) -> None:
        """
        Update the environment state based on the tool result.
        
        Args:
            tool_name: The name of the tool that was used
            result: The result of the tool execution
        """
        # Extract structured data if available
        structured_data = {}
        for content_item in result.get("content", []):
            if content_item.get("type") == "json":
                structured_data = content_item.get("json", {})
        
        # Update inventory if available
        if tool_name == "inventory" and "items" in structured_data:
            self.inventory = structured_data["items"]
        
        # For take/drop tools, update inventory if success info is available
        if (tool_name == "take" or tool_name == "drop") and "success" in structured_data:
            if "inventory" in structured_data:
                self.inventory = structured_data["inventory"]
        
        # Update score if available (would need to be added to MCP tools)
        if "score" in structured_data:
            self.score = structured_data["score"]
        
        # Update location if available (would need to be added to MCP tools)
        if "location" in structured_data:
            self.current_location = structured_data["location"]
        
        # Update valid actions
        self.valid_actions = self._get_valid_actions()
    
    def _get_valid_actions(self) -> List[str]:
        """
        Get the list of valid actions in the current state.
        
        Returns:
            A list of valid actions
        """
        # This would ideally come from the MCP server
        # For now, we'll return a default list of actions
        valid_actions = [
            "look",
            "inventory",
            "i",
            "help",
            "score"
        ]
        
        # Add directions
        for direction in ["north", "south", "east", "west", "up", "down"]:
            valid_actions.append(f"go {direction}")
            valid_actions.append(direction)
        
        # Add object interactions based on inventory
        for item in self.inventory:
            valid_actions.append(f"examine {item}")
            valid_actions.append(f"look at {item}")
            valid_actions.append(f"drop {item}")
            valid_actions.append(f"read {item}")
        
        return valid_actions
    
    def _use_mcp_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use an MCP tool.
        
        Args:
            tool_name: The name of the tool to use
            args: The arguments to pass to the tool
            
        Returns:
            The result of the tool execution
        """
        import json
        
        # Format the arguments as a JSON string
        args_json = json.dumps(args)
        
        # Use the use_mcp_tool function to call the MCP tool
        from langchain.tools import Tool
        
        # This is the actual MCP tool call
        result = use_mcp_tool(
            server_name=self.server_name,
            tool_name=tool_name,
            arguments=args_json
        )
        
        return result


def use_mcp_tool(server_name: str, tool_name: str, arguments: str) -> Dict[str, Any]:
    """
    Use an MCP tool.
    
    Args:
        server_name: The name of the MCP server
        tool_name: The name of the tool to use
        arguments: The arguments to pass to the tool, as a JSON string
        
    Returns:
        The result of the tool execution
    """
    # Import here to avoid circular imports
    import json
    
    # Parse the arguments
    args = json.loads(arguments) if arguments else {}
    
    try:
        # Try to use the actual MCP SDK
        try:
            # Import the MCP SDK
            from langchain.tools import use_mcp_tool as langchain_use_mcp_tool
            
            # Call the MCP tool
            result = langchain_use_mcp_tool(
                server_name=server_name,
                tool_name=tool_name,
                arguments=args
            )
            
            return result
        except ImportError:
            # If the MCP SDK is not available, fall back to our mock implementation
            print("MCP SDK not available, falling back to mock implementation")
            
            # Create a mock result based on the tool name and args
            if tool_name == "look":
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": "You are in a mock environment. This is a simulated MCP tool call."
                        }
                    ]
                }
            elif tool_name == "inventory":
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": "You are carrying nothing."
                        },
                        {
                            "type": "json",
                            "json": {
                                "items": []
                            }
                        }
                    ]
                }
            elif tool_name == "navigate":
                direction = args.get("direction", "nowhere")
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"You move {direction}."
                        }
                    ]
                }
            elif tool_name == "examine":
                obj = args.get("object", "nothing")
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"You examine the {obj}. It looks like a mock object."
                        }
                    ]
                }
            else:
                # Default response for other tools
                result = {
                    "content": [
                        {
                            "type": "text",
                            "text": f"You use the {tool_name} tool with args: {args}"
                        }
                    ]
                }
            
            return result
    except Exception as e:
        # If there's an error, return an error message
        print(f"Error using MCP tool: {e}")
        return {
            "content": [
                {
                    "type": "text",
                    "text": f"Error using MCP tool: {e}"
                }
            ]
        }
    
    return result
