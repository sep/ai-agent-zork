# Zork AI Agent Implementation Plan

## Completed Components

1. ✅ **Project Structure Setup**
   - Basic directory structure
   - Environment configuration
   - Documentation

2. ✅ **Mock Environment Implementation**
   - Location and object modeling
   - Action processing
   - Game state management
   - Added 'upstairs' location

3. ✅ **Agent Memory System**
   - Observation and action history
   - Location tracking
   - Inventory management

4. ✅ **Rule-Based Planner**
   - Basic action generation
   - Exploration logic
   - Action validation

5. ✅ **LLM-Based Planner**
   - OpenAI API integration
   - Context window management
   - Fallback to rule-based planning
   - API key management

6. ✅ **LangGraph Workflow**
   - Observe-Think-Act loop
   - Two-level control flow
   - Explicit reasoning
   - Workflow documentation

7. ✅ **Unit Tests**
   - Tests for rule-based planner
   - Tests for LLM-based planner
   - Tests for LangGraph workflow
   - Mock environment for testing

## Current Implementation: Tool Framework

1. **Implement Structured Tool Framework** (In Progress)
   - 🔄 Define tool definitions in YAML format (`tools.yaml`):
     - Create a unified definition for all tools
     - Include name, description, required/optional arguments, and examples
     - Use this as the single source of truth for both MCP server and Python tools
   - ✅ Create MCP server tools in TypeScript
   - 🔄 Implement `generate_tools.py` script to:
     - Read tool definitions from `tools.yaml`
     - Generate Python files for the tool registry and individual tool classes
     - Generate test files for the tool framework
   - 🔄 Update the agent to use the tool framework:
     - Modify the agent's action selection logic to use the tool registry
     - Update the execution logic to call the appropriate tools
     - Ensure proper error handling for tool execution
   - 🔄 Integrate with LangGraph workflow:
     - Update the workflow to use the tool framework
     - Add tool selection step to the workflow
     - Ensure proper handling of tool results
   - 🔄 Test the implementation:
     - Run the generated tests to verify the tool framework works correctly
     - Test the agent with the new tool framework
     - Verify that all tools work as expected

### Unified Tool Definition Approach

The tool framework uses a unified definition approach where tools are defined in one place (`tools.yaml`) and both the MCP server tools and Python tool registry are generated from the same definitions. This ensures consistency between the two implementations and makes it easier to add new tools in the future.

Example tool definition in YAML:
```yaml
- name: navigate
  description: Move in a specified direction
  required_args:
    - direction
  optional_args: []
  arg_descriptions:
    direction: Direction to move (north, south, east, west, up, down, etc.)
  examples:
    - args:
        direction: north
      description: Move north
```

The `generate_tools.py` script will:
1. Read these definitions from `tools.yaml`
2. Generate Python files:
   - `base.py` - Base Tool class and McpToolAdapter
   - `registry.py` - ToolRegistry class and tool registration
   - `__init__.py` - Exports and singleton registry
   - `README.md` - Documentation for the tool framework
3. Generate test files:
   - `test_tools.py` - Unit tests for the tool framework

## Future Implementation Steps

1. **Integrate LangView**
   - Set up LangView for workflow visualization
   - Configure tracing for the LangGraph workflow
   - Add instrumentation to capture agent reasoning
   - Create visualization dashboard
   - Document LangView integration

2. **Replace Mock Environment with Real Implementation**
   - Integrate with Z-machine interpreter (e.g., Frotz or Jericho)
   - Implement adapter for the real Zork game
   - Handle text parsing and response extraction
   - Add support for saving and loading game states
   - Update tests to work with the real environment

## Technical Considerations

1. **Tool Framework Design**
   - Using a unified YAML definition format for all tools
   - McpToolAdapter pattern to bridge between Python and MCP server
   - Singleton ToolRegistry for easy access throughout the codebase
   - Design for extensibility to add new tools easily

2. **LangView Integration**
   - Determine the appropriate level of instrumentation
   - Balance performance with observability
   - Consider privacy and security implications

3. **Real Environment Integration**
   - Handle differences between mock and real environments
   - Manage dependencies on external libraries
   - Consider performance implications
   - Ensure robust error handling

## Implementation Approach

For each remaining step:

1. **Design Phase**
   - Create detailed design document
   - Define interfaces and data structures
   - Identify potential challenges and solutions

2. **Implementation Phase**
   - Implement core functionality
   - Add tests for new components
   - Ensure backward compatibility

3. **Integration Phase**
   - Integrate with existing components
   - Update documentation
   - Verify end-to-end functionality

4. **Evaluation Phase**
   - Measure performance and effectiveness
   - Identify areas for improvement
   - Document lessons learned
