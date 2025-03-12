"""
Unified runner for the Zork AI agent.

This script provides a unified entry point for running either the implicit or explicit
agent with the mock environment.
"""
import argparse
import os
from dotenv import load_dotenv
from src.mock_environment import MockZorkEnvironment
from src.agent.implicit.workflow import run_agent_workflow as run_implicit_workflow
from src.agent.explicit.workflow import run_agent_workflow as run_explicit_workflow

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Run the Zork AI agent with either the implicit or explicit workflow.
    
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
        choices=["implicit", "explicit"],
        default="implicit",
        help="Type of agent to run (implicit or explicit)"
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
    args = parser.parse_args()
    
    # Print header based on agent type
    print("\n" + "="*60)
    if args.agent_type == "implicit":
        print("ZORK AI AGENT WITH IMPLICIT WORKFLOW")
        print("="*60)
        print("This agent generates text commands directly.")
    else:
        print("ZORK AI AGENT WITH EXPLICIT TOOL-BASED WORKFLOW")
        print("="*60)
        print("This agent explicitly selects tools and provides parameters.")
    
    print(f"Using model: {args.model}")
    print("Press Ctrl+C to stop the agent.")
    
    # Initialize the environment
    env = MockZorkEnvironment()
    
    try:
        # Run the selected agent workflow
        if args.agent_type == "implicit":
            run_implicit_workflow(
                environment=env,
                model_name=args.model,
                api_key=args.api_key,
                max_steps=args.max_steps
            )
        else:
            run_explicit_workflow(
                environment=env,
                model_name=args.model,
                api_key=args.api_key,
                max_steps=args.max_steps
            )
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")


if __name__ == "__main__":
    main()
