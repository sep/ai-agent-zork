"""
Run the Zork AI agent with the current components.

This script runs the agent with the mock environment, memory system, and
either the rule-based planner or the LLM-based planner. It demonstrates 
how the agent can play Zork without the LangGraph workflow.
"""
import argparse
from src.mock_environment import MockZorkEnvironment
from src.agent.memory import AgentMemory
from src.agent.planner import ActionPlanner
from src.agent.llm_planner import LLMActionPlanner


def print_section(title):
    """Print a section title with separators."""
    print("\n" + "="*60)
    print(title)
    print("="*60)


def main():
    """
    Run the Zork AI agent.
    
    This function:
    1. Initializes the environment, memory, and planner
    2. Runs the agent in a loop
    3. Shows the agent's actions and the environment's responses
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Run the Zork AI agent")
    parser.add_argument(
        "--use-llm", 
        action="store_true", 
        help="Use the LLM-based planner instead of the rule-based planner"
    )
    parser.add_argument(
        "--model", 
        type=str, 
        default="gpt-3.5-turbo",
        help="LLM model to use (only applicable with --use-llm)"
    )
    args = parser.parse_args()
    
    print_section("ZORK AI AGENT")
    
    # Initialize the components
    env = MockZorkEnvironment()
    memory = AgentMemory()
    
    # Choose the planner based on command line arguments
    if args.use_llm:
        print(f"This agent uses an LLM-based planner ({args.model}) to play Zork.")
        planner = LLMActionPlanner(model_name=args.model)
    else:
        print("This agent uses a rule-based planner to play Zork.")
        planner = ActionPlanner()
    
    print("Press Ctrl+C to stop the agent.")
    
    # Get the initial state
    state = env.reset()
    
    # Add the initial observation to memory
    memory.add_observation(state["observation"], state)
    
    print_section("INITIAL STATE")
    print(f"Location: {memory.current_location}")
    print(f"Observation: {state['observation']}")
    
    # Run the agent loop
    step = 0
    try:
        while True:
            step += 1
            print_section(f"STEP {step}")
            
            # Generate an action using the planner
            action = planner.generate_action(
                state["observation"],
                state["valid_actions"],
                memory
            )
            
            print(f"Agent action: {action}")
            
            # Execute the action in the environment
            result = env.step(action)
            
            # Add the action and result to memory
            memory.add_action(action, result)
            memory.add_observation(result["observation"], result)
            
            # Update inventory if this was an inventory command
            if action.lower() in ["inventory", "i"]:
                memory.update_inventory(result["inventory"])
            
            # Update exploration state in the planner
            planner.update_exploration_state(result["observation"], memory)
            
            # Print the result and memory state
            print(f"Observation: {result['observation']}")
            print(f"Location: {memory.current_location}")
            print(f"Score: {memory.score}")
            print(f"Moves: {memory.moves}")
            print(f"Inventory: {memory.get_inventory()}")
            
            # Update the state for the next iteration
            state = result
            
            # Optional: Add a delay to make it easier to follow
            import time
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nAgent stopped by user.")
    
    # Print final stats
    print_section("FINAL STATS")
    print(f"Steps: {step}")
    print(f"Score: {memory.score}")
    print(f"Locations visited: {len(planner.explored_locations)}")
    print(f"Locations: {', '.join(planner.explored_locations)}")
    print(f"Inventory: {memory.get_inventory()}")


if __name__ == "__main__":
    main()
