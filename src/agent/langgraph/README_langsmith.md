# LangSmith Integration for Zork AI Agent (LangGraph)

This document explains how to use the LangSmith integration for visualizing and debugging the Zork AI agent's LangGraph workflow.

## Overview

The Zork AI agent now supports tracing and visualization through LangSmith, a platform developed by LangChain for debugging, testing, evaluating, and monitoring LLM applications. This integration allows you to:

1. Visualize the agent's decision-making process in a web interface
2. Inspect the state at each step of the workflow
3. Debug issues with the agent's behavior
4. Understand how the agent selects actions
5. Compare different runs and configurations

## Prerequisites

To use LangSmith, you need:

1. A LangSmith account (sign up at [smith.langchain.com](https://smith.langchain.com))
2. A LangSmith API key
3. The `langsmith` Python package installed

```bash
pip install langsmith
```

## Configuration

The LangSmith configuration can be set in the `.env` file:

```
# LangSmith configuration for tracing and visualization
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=your-langsmith-api-key-here
LANGSMITH_PROJECT=zork-agent
```

You can copy the `.env.example` file to `.env` and update it with your actual API key:

```bash
cp .env.example .env
# Then edit the .env file with your text editor
```

Alternatively, you can set these values as environment variables:

```bash
# On Windows
set LANGSMITH_TRACING=true
set LANGSMITH_ENDPOINT=https://api.smith.langchain.com
set LANGSMITH_API_KEY=your_api_key
set LANGSMITH_PROJECT=zork-agent

# On Linux/macOS
export LANGSMITH_TRACING=true
export LANGSMITH_ENDPOINT=https://api.smith.langchain.com
export LANGSMITH_API_KEY=your_api_key
export LANGSMITH_PROJECT=zork-agent
```

## How to Enable LangSmith Tracing

To enable LangSmith tracing, use the `--enable-langsmith` flag when running the LangGraph agent:

```bash
python src/run_langgraph_agent.py --enable-langsmith
```

You can also specify a project name:

```bash
python src/run_langgraph_agent.py --enable-langsmith --langsmith-project my-zork-project
```

## Viewing Traces

After running the agent with LangSmith tracing enabled:

1. Go to [smith.langchain.com](https://smith.langchain.com)
2. Log in to your account
3. Navigate to the "Traces" section
4. Find your run in the list (it will be in the project you specified)
5. Click on the run to view the detailed trace

## Trace Structure

Each trace in LangSmith shows:

- The complete workflow graph
- Each node's execution details
- Input and output states for each node
- Timing information
- LLM calls with prompts and responses

## Benefits Over Basic Tracing

LangSmith provides several advantages over basic file-based tracing:

1. **Interactive Visualization**: See the workflow graph and execution path visually
2. **Prompt Analysis**: Examine the exact prompts sent to the LLM and the responses received
3. **Performance Metrics**: Get timing information for each step
4. **Run Comparison**: Compare different runs to identify improvements or regressions
5. **Sharing**: Easily share traces with team members
6. **Feedback Collection**: Collect feedback on runs to improve your agent

## Troubleshooting

If you encounter issues with LangSmith tracing:

1. Verify your API key is correct and properly set
2. Ensure you have internet connectivity
3. Check that you have the latest version of the `langsmith` package
4. Look for error messages in the console output
