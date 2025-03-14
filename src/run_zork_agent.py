"""
Unified runner for the Zork AI agent.

This script provides a unified entry point for running either the LangGraph or MCP LangGraph
agent with the appropriate environment.
"""
import argparse
from dotenv import load_dotenv
from src.mock_environment import MockZorkEnvironment
from src.mcp.environment import create_environment
from src.agent.langgraph.workflow import run_agent_workflow as run_langgraph_workflow
from src.agent.mcp_langgraph.workflow import run_agent_workflow as run_mcp_langgraph_workflow

# Load environment variables from .env file
load_dotenv()

# MCP server name for Zork tools
MCP_SERVER_NAME = "zork-tools"


def main():
    """
    Run the Zork AI agent with either the LangGraph or MCP LangGraph workflow.
    
    This function:
    1. Parses command line arguments to determine which agent to run
    2. Initializes the environment
    3. Runs the selected agent workflow
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Zork AI agent")
    parser.add_argument(
        "--agent-type",
        type=str,
        choices=["langgraph", "mcp-langgraph"],
        default="langgraph",
        help="Type of agent to run (langgraph or mcp-langgraph)"
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
        default=100,
        help="Maximum number of steps to run"
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
    
    # Print header based on agent type
    print("\n" + "="*60)
    if args.agent_type == "langgraph":
        print("ZORK AI AGENT WITH LANGGRAPH WORKFLOW")
        print("="*60)
        print("This agent generates text commands directly.")
        
        # Initialize the environment for LangGraph agent
        env = MockZorkEnvironment()
    else:
        print("ZORK AI AGENT WITH MCP LANGGRAPH WORKFLOW")
        print("="*60)
        print("This agent selects MCP tools and provides parameters.")
        
        # Initialize the environment for MCP LangGraph agent
        try:
            print(f"Using MCP environment with server: {args.mcp_server}")
            env = create_environment(server_name=args.mcp_server, debug=True)
        except Exception as e:
            if args.fallback_to_mock:
                print(f"Error initializing MCP environment: {e}")
                print("Falling back to mock environment.")
                env = MockZorkEnvironment()
            else:
                print(f"Error initializing MCP environment: {e}")
                print("To fall back to the mock environment, use --fallback-to-mock")
                return
    
    print(f"Using model: {args.model}")
    print("Press Ctrl+C to stop the agent.")
    
    try:
        # Run the selected agent workflow
        if args.agent_type == "langgraph":
            run_langgraph_workflow(
                environment=env,
                model_name=args.model,
                api_key=args.api_key,
                max_steps=args.max_steps
            )
        else:
            run_mcp_langgraph_workflow(
                environment=env,
                model_name=args.model,
                api_key=args.api_key,
                max_steps=args.max_steps
            )
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")


if __name__ == "__main__":
    main()
