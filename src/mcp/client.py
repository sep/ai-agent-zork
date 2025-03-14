"""
MCP Client for communicating with MCP servers.

This module implements a simple client that communicates with MCP servers
using the subprocess module and JSON-RPC protocol.
"""
import json
import subprocess
import threading
import time
from typing import Any, Dict, List, Optional, Union


class MCPClient:
    """
    A client for communicating with MCP servers.
    """
    
    def __init__(self, command: str, args: List[str], debug: bool = False):
        """
        Initialize the MCP client.
        
        Args:
            command: The command to run the MCP server
            args: The arguments to pass to the command
            debug: Whether to print debug information
        """
        self.process = None
        self.command = command
        self.args = args
        self.request_id = 0
        self.debug = debug
    
    def start(self) -> bool:
        """
        Start the MCP server process.
        
        Returns:
            True if the server was started successfully, False otherwise
        """
        print("Starting MCP server...")
        
        try:
            # Start the MCP server process
            self.process = subprocess.Popen(
                [self.command] + self.args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Start a thread to read stderr
            def read_stderr():
                for line in self.process.stderr:
                    print(f"[Server] {line.strip()}")
            
            stderr_thread = threading.Thread(target=read_stderr)
            stderr_thread.daemon = True
            stderr_thread.start()
            
            # Wait for the server to start
            time.sleep(1)
            
            return True
        except Exception as e:
            print(f"Error starting MCP server: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop the MCP server process.
        
        Returns:
            True if the server was stopped successfully, False otherwise
        """
        if self.process:
            print("Stopping MCP server...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
                self.process = None
                return True
            except Exception as e:
                print(f"Error stopping MCP server: {e}")
                return False
        return True
    
    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: The name of the tool to call
            arguments: The arguments to pass to the tool
            
        Returns:
            The result of the tool call, or None if an error occurred
        """
        if not self.process:
            print("MCP server not started")
            return None
        
        # Increment the request ID
        self.request_id += 1
        
        # Create the request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            }
        }
        
        # Debug
        if self.debug:
            print(f"Sending request: {json.dumps(request)}")
        
        try:
            # Send the request
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            
            # Read the response
            response = self.process.stdout.readline()
            
            # Debug
            if self.debug:
                print(f"Received response: {response}")
            
            # Parse the response
            try:
                response_json = json.loads(response)
                if "result" in response_json:
                    return response_json["result"]
                else:
                    error = response_json.get("error", {"code": -1, "message": "Unknown error"})
                    print(f"Error calling tool {tool_name}: {error}")
                    return None
            except json.JSONDecodeError:
                print(f"Error decoding response: {response}")
                return None
        except Exception as e:
            print(f"Error calling tool {tool_name}: {e}")
            return None
    
    def list_tools(self) -> Optional[List[Dict[str, Any]]]:
        """
        List the available tools on the MCP server.
        
        Returns:
            A list of available tools, or None if an error occurred
        """
        if not self.process:
            print("MCP server not started")
            return None
        
        # Increment the request ID
        self.request_id += 1
        
        # Create the request
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/list",
            "params": {}
        }
        
        # Debug
        if self.debug:
            print(f"Sending request: {json.dumps(request)}")
        
        try:
            # Send the request
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            
            # Read the response
            response = self.process.stdout.readline()
            
            # Debug
            if self.debug:
                print(f"Received response: {response}")
            
            # Parse the response
            try:
                response_json = json.loads(response)
                if "result" in response_json:
                    return response_json["result"]["tools"]
                else:
                    error = response_json.get("error", {"code": -1, "message": "Unknown error"})
                    print(f"Error listing tools: {error}")
                    return None
            except json.JSONDecodeError:
                print(f"Error decoding response: {response}")
                return None
        except Exception as e:
            print(f"Error listing tools: {e}")
            return None


def create_zork_client(debug: bool = False) -> MCPClient:
    """
    Create an MCP client for the Zork MCP server.
    
    Args:
        debug: Whether to print debug information
        
    Returns:
        An MCP client for the Zork MCP server
    """
    return MCPClient("node", ["mcp/zork-tools/build/index.js"], debug)


# Singleton MCP client for reuse across tool calls
_mcp_client = None

def get_mcp_client(server_name: str = "zork-tools", debug: bool = False) -> MCPClient:
    """
    Get or create the singleton MCP client.
    
    Args:
        server_name: The name of the MCP server to use
        debug: Whether to print debug information
        
    Returns:
        The singleton MCP client
    """
    global _mcp_client
    
    # Create and start the MCP client if it doesn't exist
    if _mcp_client is None:
        print("Creating and starting MCP client...")
        _mcp_client = create_zork_client(debug=debug)
        
        # Start the MCP server
        if not _mcp_client.start():
            raise Exception(f"Failed to start MCP server: {server_name}")
    
    return _mcp_client

def get_mcp_tools(server_name: str = "zork-tools", debug: bool = False) -> List[Dict[str, Any]]:
    """
    Get the available tools from the MCP server.
    
    Args:
        server_name: The name of the MCP server to use
        debug: Whether to print debug information
        
    Returns:
        A list of available tools with their descriptions and parameters
    """
    client = get_mcp_client(server_name, debug)
    
    # Get the list of tools
    tools = client.list_tools()
    if not tools:
        print("Warning: No tools found on MCP server")
        return []
    
    return tools

def use_mcp_tool(server_name: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use an MCP tool directly.
    
    This function uses a singleton MCP client to call the specified tool
    with the provided arguments and returns the result. The client is
    created and started on the first call, and reused for subsequent calls.
    
    Args:
        server_name: The name of the MCP server to use
        tool_name: The name of the tool to call
        args: The arguments to pass to the tool
        
    Returns:
        The result of the tool execution
    """
    global _mcp_client
    
    # Create and start the MCP client if it doesn't exist
    if _mcp_client is None:
        print("Creating and starting MCP client...")
        _mcp_client = create_zork_client(debug=False)
        
        # Start the MCP server
        if not _mcp_client.start():
            raise Exception(f"Failed to start MCP server: {server_name}")
    
    try:
        # Call the tool
        result = _mcp_client.call_tool(tool_name, args)
        
        if not result:
            raise Exception(f"Error calling tool {tool_name}: No result")
        
        # Convert the MCP result to the format expected by the agent
        # The agent expects a result with observation, score, done, moves, etc.
        observation = ""
        for content_item in result.get("content", []):
            if content_item.get("type") == "text":
                observation += content_item.get("text", "")
        
        # Extract structured data if available
        structured_data = {}
        for content_item in result.get("content", []):
            if content_item.get("type") == "json":
                structured_data = content_item.get("json", {})
        
        # Create a result object that matches the environment.step() return value
        return {
            "observation": observation,
            "score": structured_data.get("score", 0),
            "done": structured_data.get("done", False),
            "moves": structured_data.get("moves", 0),
            "valid_actions": structured_data.get("valid_actions", []),
            "inventory": structured_data.get("inventory", []),
            "location": structured_data.get("location", "")
        }
    except Exception as e:
        # If there's an error, clean up the client and re-raise the exception
        print(f"Error calling tool {tool_name}: {e}")
        if _mcp_client is not None:
            _mcp_client.stop()
            _mcp_client = None
        raise


def main():
    """
    Main function for testing the MCP client.
    """
    # Create the MCP client
    client = create_zork_client(debug=True)
    
    # Start the MCP server
    if not client.start():
        print("Failed to start MCP server")
        return
    
    try:
        # List available tools
        tools = client.list_tools()
        if tools:
            print("\nAvailable tools:")
            for tool in tools:
                print(f"- {tool['name']}: {tool['description']}")
        
        # Call the look tool
        print("\nCalling look tool...")
        result = client.call_tool("look")
        if result:
            print("\nLook result:")
            for content_item in result.get("content", []):
                if content_item.get("type") == "text":
                    print(content_item.get("text", ""))
        
        # Call the inventory tool
        print("\nCalling inventory tool...")
        result = client.call_tool("inventory")
        if result:
            print("\nInventory result:")
            for content_item in result.get("content", []):
                if content_item.get("type") == "text":
                    print(content_item.get("text", ""))
                elif content_item.get("type") == "json":
                    print(f"Items: {content_item.get('json', {}).get('items', [])}")
    
    finally:
        # Stop the MCP server
        client.stop()


if __name__ == "__main__":
    main()
