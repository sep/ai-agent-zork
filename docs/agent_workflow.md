# Zork AI Agent Workflow

This document provides a visual representation and explanation of the Zork AI agent workflow.

## Workflow Diagram

```mermaid
graph TD
    %% Main function loop
    Start([Start]) --> InitEnv[Initialize Environment]
    InitEnv --> InitState[Initialize Agent State]
    InitState --> Loop[Loop for max_steps]
    
    %% LangGraph workflow (inner loop)
    subgraph "LangGraph Workflow"
        Observe[Observe Node<br/>Process observation<br/>Update history] --> ShouldContinue{Should Continue?}
        ShouldContinue -->|"continue"| Think[Think Node<br/>Generate thought<br/>using LLM]
        ShouldContinue -->|"end"| End([End Workflow])
        Think --> Act[Act Node<br/>Generate action<br/>using LLM]
    end
    
    %% Function control flow (outer loop)
    Loop --> InvokeGraph[Invoke LangGraph Workflow]
    InvokeGraph --> CheckEnd{Workflow Ended?}
    CheckEnd -->|Yes| FinalStats[Print Final Stats]
    CheckEnd -->|No| UpdateState[Update Agent State]
    UpdateState --> ExecuteAction[Execute Action in Environment]
    ExecuteAction --> UpdateObservation[Update Agent State with New Observation]
    UpdateObservation --> Loop
    FinalStats --> End2([End])
    
    %% Environment interaction
    subgraph "Environment Interaction"
        ExecuteAction --> EnvStep[Environment.step]
        EnvStep --> GetObs[Get Observation]
        GetObs --> GetValid[Get Valid Actions]
        GetValid --> GetLoc[Get Location]
        GetLoc --> GetScore[Get Score]
        GetScore --> GetMoves[Get Moves]
        GetMoves --> GetInv[Get Inventory]
        GetInv --> UpdateObservation
    end
    
    %% Styling
    classDef process fill:#f9f,stroke:#333,stroke-width:2px
    classDef decision fill:#bbf,stroke:#333,stroke-width:2px
    classDef terminal fill:#dfd,stroke:#333,stroke-width:2px
    
    class Start,End,End2 terminal
    class ShouldContinue,CheckEnd decision
    class Observe,Think,Act,InitEnv,InitState,UpdateState,ExecuteAction,UpdateObservation,Loop,InvokeGraph,FinalStats process
```

## Explanation of the Workflow

The diagram illustrates the two-level control flow of our Zork AI agent:

### Outer Loop (Function Level)

1. **Initialization**: The process starts by initializing the environment and the agent state.
2. **Main Loop**: For each step (up to max_steps):
   - Invoke the LangGraph workflow
   - Check if the workflow has ended
   - Update the agent state with the result
   - Execute the action in the environment
   - Update the agent state with the new observation
3. **Termination**: Print final stats and end the process

### Inner Loop (LangGraph Workflow)

1. **Observe Node**: Process the current observation and update history
2. **Should Continue?**: Determine if the workflow should continue or end
3. **Think Node**: Generate a thought about the current state using the LLM
4. **Act Node**: Generate an action based on the thought using the LLM

### Environment Interaction

The diagram also shows how the agent interacts with the environment:
- Execute the action in the environment
- Get the observation, valid actions, location, score, moves, and inventory
- Update the agent state with the new information

## Implementation Details

### LangGraph Workflow Design

We implemented the LangGraph workflow with a linear flow (without loops) for technical reasons:

1. **Recursion Limit Issues**: When we initially implemented the workflow with a loop from "act" back to "observe", we encountered a `GraphRecursionError` with the message "Recursion limit of 25 reached without hitting a stop condition." This error occurs because LangGraph has built-in safeguards to prevent infinite loops.

2. **State Management Approach**: LangGraph uses a different approach to state management than what we initially expected. When a graph is compiled and invoked, LangGraph attempts to run the entire graph to completion, following all edges until it reaches an end state or hits the recursion limit.

3. **Manual Loop Control**: By removing the loop in the graph definition and instead manually managing the loop in our `run_agent_workflow` function, we gain more control over the execution flow and can avoid the recursion limit.

### Code Implementation

In our implementation:

```python
# The graph definition is linear (no loops)
workflow.add_edge("observe", "think")
workflow.add_edge("think", "act")

# The function implements the loop
for step in range(max_steps):
    # Run one step of the workflow
    result = app.invoke(agent_state)
    
    # Update the agent state
    agent_state = result
    
    # Execute the action in the environment
    state = environment.step(agent_state["action"])
    
    # Update the agent state with the new observation
    agent_state["observation"] = state["observation"]
    # ... other state updates ...
```

This pattern is common in LangGraph applications where you need more control over the execution flow than what's provided by the built-in graph execution model.

## Benefits of This Approach

1. **Simplicity**: The graph structure is simpler and easier to reason about
2. **Reliability**: We avoid hitting recursion limits and potential stack overflows
3. **Flexibility**: We can add custom logic between steps
4. **Observability**: It's easier to log and debug the execution flow
5. **Control**: We have explicit control over when to continue or stop the loop

This design pattern allows us to leverage the strengths of LangGraph for defining the agent's reasoning process while maintaining control over the overall execution flow.
