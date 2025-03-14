"""
LangGraph workflow for the Zork AI agent.

This module provides a LangGraph-based workflow for the agent, implementing
an observe-think-act loop with more sophisticated reasoning capabilities.
"""
from typing import Dict, List, Any, Optional, TypedDict
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# Load environment variables from .env file
load_dotenv()

# Define the state schema
class AgentState(TypedDict):
    """State for the agent workflow."""
    observation: str
    valid_actions: List[str]
    inventory: List[str]
    location: str
    thought: Optional[str]
    action: Optional[str]
    history: List[Dict[str, Any]]
    score: int
    moves: int
    done: bool


def create_agent_workflow(
    model_name: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None
) -> StateGraph:
    """
    Create a LangGraph workflow for the Zork AI agent.
    
    Args:
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider (defaults to environment variable)
        
    Returns:
        A LangGraph StateGraph
    """
    # Initialize the LLM
    llm = ChatOpenAI(
        model=model_name,
        api_key=api_key or os.environ.get("OPENAI_API_KEY"),
        temperature=0.7
    )
    
    # Define the nodes
    def observe(state: AgentState) -> AgentState:
        """
        Process the current observation and update the state.
        
        Args:
            state: The current state
            
        Returns:
            The updated state
        """
        # Add the current observation to history
        if state["observation"]:
            history_item = {
                "observation": state["observation"],
                "location": state["location"],
                "inventory": state["inventory"],
                "score": state["score"],
                "moves": state["moves"]
            }
            
            # Add the previous action if it exists
            if state["action"]:
                history_item["action"] = state["action"]
                
            # Add to history
            state["history"] = state["history"] + [history_item]
        
        # Clear the previous thought and action
        state["thought"] = None
        state["action"] = None
        
        return state
    
    def think(state: AgentState) -> AgentState:
        """
        Generate a thought about the current state.
        
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
        
        Valid Actions:
        {', '.join(state["valid_actions"][:20])}
        
        Score: {state["score"]}
        Moves: {state["moves"]}
        
        Recent History:
        {state["history"][-3:]}
        
        Think about the current situation. What should you do next and why?
        Consider your goals, the environment, and the available actions.
        """
        
        # Generate a thought using the LLM
        response = llm.invoke(prompt)
        thought = response.content
        
        # Update the state with the thought
        state["thought"] = thought
        
        return state
    
    def act(state: AgentState) -> AgentState:
        """
        Generate an action based on the thought.
        
        Args:
            state: The current state
            
        Returns:
            The updated state with an action
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
        
        Valid Actions:
        {', '.join(state["valid_actions"][:20])}
        
        Your Thought:
        {state["thought"]}
        
        Based on your thought, what is the single next action you will take?
        Return ONLY the action, with no additional explanation or commentary.
        The action must be one of the valid actions provided.
        """
        
        # Generate an action using the LLM
        response = llm.invoke(prompt)
        action = response.content.strip()
        
        # Validate the action against valid actions
        if action not in state["valid_actions"]:
            # Try to find a similar action
            for valid_action in state["valid_actions"]:
                if action.lower() in valid_action.lower():
                    action = valid_action
                    break
            
            # If still not valid, use a default action
            if action not in state["valid_actions"]:
                action = "look"  # Default to looking around
        
        # Update the state with the action
        state["action"] = action
        
        return state
    
    def should_continue(state: AgentState) -> str:
        """
        Determine if the workflow should continue or end.
        
        Args:
            state: The current state
            
        Returns:
            "continue" to continue the workflow, "end" to end it
        """
        # End the workflow if the game is over
        if state["done"]:
            return "end"
        
        # Continue the workflow
        return "continue"
    
    # Create the graph
    workflow = StateGraph(AgentState)
    
    # Add the nodes
    workflow.add_node("observe", observe)
    workflow.add_node("think", think)
    workflow.add_node("act", act)
    
    # Add the edges (linear flow without loops)
    workflow.add_edge("observe", "think")
    workflow.add_edge("think", "act")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "observe",
        should_continue,
        {
            "continue": "think",
            "end": END
        }
    )
    
    # Set the entry point
    workflow.set_entry_point("observe")
    
    return workflow


def run_agent_workflow(
    environment: Any,
    model_name: str = "gpt-3.5-turbo",
    api_key: Optional[str] = None,
    max_steps: int = 100
) -> Dict[str, Any]:
    """
    Run the agent workflow with the given environment.
    
    Args:
        environment: The environment to run the agent in
        model_name: The name of the LLM model to use
        api_key: The API key for the LLM provider
        max_steps: The maximum number of steps to run
        
    Returns:
        The final state
    """
    # Create the workflow
    workflow = create_agent_workflow(model_name, api_key)
    app = workflow.compile()
    
    # Initialize the environment
    state = environment.reset()
    
    # Convert to AgentState
    agent_state = AgentState(
        observation=state["observation"],
        valid_actions=state["valid_actions"],
        inventory=state["inventory"],
        location=state["location"],
        thought=None,
        action=None,
        history=[],
        score=state["score"],
        moves=state["moves"],
        done=state["done"]
    )
    
    # Run the workflow
    for step in range(max_steps):
        # Print the step
        print(f"\n{'='*60}")
        print(f"STEP {step + 1}")
        print(f"{'='*60}")
        
        # Run one step of the workflow
        result = app.invoke(agent_state)
        
        # Check if the workflow has ended
        if "end" in result:
            break
        
        # Update the agent state
        agent_state = result
        
        # Print the thought and action
        if agent_state["thought"]:
            print(f"Thought: {agent_state['thought']}")
        
        if agent_state["action"]:
            print(f"Action: {agent_state['action']}")
            
            # Execute the action in the environment
            state = environment.step(agent_state["action"])
            
            # Update the agent state with the new observation
            agent_state["observation"] = state["observation"]
            agent_state["valid_actions"] = state["valid_actions"]
            agent_state["inventory"] = state["inventory"]
            agent_state["location"] = state["location"]
            agent_state["score"] = state["score"]
            agent_state["moves"] = state["moves"]
            agent_state["done"] = state["done"]
            
            # Print the result
            print(f"Observation: {state['observation']}")
            print(f"Location: {state['location']}")
            print(f"Score: {state['score']}")
            print(f"Moves: {state['moves']}")
            print(f"Inventory: {state['inventory']}")
    
    # Print final stats
    print(f"\n{'='*60}")
    print("FINAL STATS")
    print(f"{'='*60}")
    print(f"Steps: {agent_state['moves']}")
    print(f"Score: {agent_state['score']}")
    print(f"Inventory: {agent_state['inventory']}")
    
    return agent_state
