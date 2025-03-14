"""
Run the Zork AI agent with the LangGraph workflow.

This script runs the agent with the mock environment and LangGraph workflow,
demonstrating a more sophisticated agent architecture with observe-think-act loops.
"""
import argparse
import os
from dotenv import load_dotenv
from src.mock_environment import MockZorkEnvironment
from src.agent.langgraph.workflow import run_agent_workflow

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Run the Zork AI agent with the LangGraph workflow.
    
    This function:
    1. Initializes the environment
    2. Creates and runs the LangGraph workflow
    3. Shows the agent's thoughts, actions, and the environment's responses
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Zork AI agent with LangGraph")
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
    
    print("\n" + "="*60)
    print("ZORK AI AGENT WITH LANGGRAPH WORKFLOW")
    print("="*60)
    print(f"This agent uses a LangGraph workflow with {args.model} to play Zork.")
    print("Press Ctrl+C to stop the agent.")
    
    # Initialize the environment
    env = MockZorkEnvironment()
    
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
