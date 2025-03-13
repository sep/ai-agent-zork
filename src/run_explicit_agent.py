"""
Run the Zork AI agent with the explicit LangGraph workflow.

This script runs the agent with the mock environment and explicit LangGraph workflow,
demonstrating a more sophisticated agent architecture with tool-based interaction.
The workflow is designed to work with MCP tools for Zork, though it currently
uses the mock environment directly for simplicity.
"""
import argparse
import os
from dotenv import load_dotenv
from src.mock_environment import MockZorkEnvironment
from src.mcp_environment import MCPEnvironmentWrapper
from src.agent.explicit.workflow import run_agent_workflow

# Load environment variables from .env file
load_dotenv()

# MCP server name for Zork tools
MCP_SERVER_NAME = "zork-tools"


def main():
    """
    Run the Zork AI agent with the explicit LangGraph workflow.
    
    This function:
    1. Initializes the environment
    2. Creates and runs the explicit LangGraph workflow
    3. Shows the agent's thoughts, tool selections, and the environment's responses
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run the Zork AI agent with explicit tool-based workflow"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-3.5-turbo",
        help="LLM model to use"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for the LLM provider (defaults to OPENAI_API_KEY env var)"
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=20,
        help="Maximum number of steps to run (default: 20)"
    )
    parser.add_argument(
        "--mcp-server",
        type=str,
        default="zork-tools",
        help="Name of the MCP server to use (default: zork-tools)"
    )
    parser.add_argument(
        "--fallback-to-mock",
        action="store_true",
        help="Fall back to mock environment if MCP server is not available"
    )
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("ZORK AI AGENT WITH EXPLICIT TOOL-BASED WORKFLOW")
    print("="*60)
    print(f"This agent uses a LangGraph workflow with {args.model} to play Zork.")
    print("It explicitly selects tools and provides parameters through the MCP server.")
    print("Press Ctrl+C to stop the agent.")
    
    # Initialize the environment
    try:
        print(f"Using MCP environment with server: {args.mcp_server}")
        env = MCPEnvironmentWrapper(args.mcp_server)
    except Exception as e:
        if args.fallback_to_mock:
            print(f"Error initializing MCP environment: {e}")
            print("Falling back to mock environment.")
            env = MockZorkEnvironment()
        else:
            print(f"Error initializing MCP environment: {e}")
            print("To fall back to the mock environment, use --fallback-to-mock")
            return
    
    try:
        # Run the agent workflow
        run_agent_workflow(
            environment=env,
            model_name=args.model,
            api_key=args.api_key,
            max_steps=args.max_steps
        )
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")


if __name__ == "__main__":
    main()
