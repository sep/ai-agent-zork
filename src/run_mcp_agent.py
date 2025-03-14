"""
Run the MCP Zork agent.

This script runs the MCP agent that uses the MCP environment to play Zork.
The agent follows a deliberative process: first thinking about what to do,
then selecting an action based on that thought.
"""
import argparse
from src.agent.mcp.agent import run_agent


def main():
    """
    Main function.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run the MCP Zork agent"
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
        "--debug",
        action="store_true",
        help="Print debug information"
    )
    args = parser.parse_args()
    
    # Run the agent
    run_agent(
        model_name=args.model,
        api_key=args.api_key,
        max_steps=args.max_steps,
        debug=args.debug
    )


if __name__ == "__main__":
    main()
