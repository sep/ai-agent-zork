# Zork Tools MCP Server

An MCP (Model Context Protocol) server that provides tools for AI agents to interact with the Zork text adventure game.

## Overview

This MCP server implements a set of tools that allow AI agents to interact with a Zork-like environment through a structured interface. It uses the Model Context Protocol to expose these tools to compatible AI systems, enabling more explicit and structured interactions compared to generating raw text commands.

The server includes a mock implementation of the Zork environment, which simulates the classic text adventure game with locations, objects, and interactions. This allows for testing and development without requiring the actual Zork game.

## Features

- **Structured Tool Interface**: Provides a set of well-defined tools with clear input schemas
- **Mock Environment**: Includes a simulated Zork environment for testing
- **Comprehensive Tool Set**: Covers all common Zork interactions:
  - Navigation
  - Object examination
  - Inventory management
  - Object manipulation (take, drop, open, close, etc.)
  - Reading text
  - Using the lamp

## Tools

The server provides the following tools:

| Tool Name | Description | Required Parameters |
|-----------|-------------|---------------------|
| `navigate` | Move in a specified direction | `direction`: Direction to move (north, south, east, west, up, down) |
| `examine` | Examine an object in the environment | `object`: Object to examine |
| `inventory` | Check your inventory | None |
| `take` | Take an object | `object`: Object to take |
| `drop` | Drop an object from your inventory | `object`: Object to drop |
| `read` | Read an object with text | `object`: Object to read |
| `look` | Look around to get a description of your surroundings | None |
| `open` | Open an object like a mailbox or door | `object`: Object to open |
| `close` | Close an object like a mailbox or door | `object`: Object to close |
| `put` | Put an object into a container | `object`: Object to put, `container`: Container to put the object in |
| `lamp` | Turn the lamp on or off | `action`: "on" or "off" |
| `move` | Move an object like the rug | `object`: Object to move |

## Installation

1. Ensure you have Node.js installed (v14 or later)
2. Clone this repository
3. Install dependencies:
   ```
   npm install
   ```
4. Build the project:
   ```
   npm run build
   ```

## Usage

### Running the Server

To run the MCP server:

```
npm start
```

This will start the server using stdio for communication.

### Configuring in MCP Settings

To use this server with an MCP-compatible system, add it to your MCP settings file:

```json
{
  "mcpServers": {
    "zork-tools": {
      "command": "node",
      "args": ["path/to/zork-tools/build/index.js"],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

### Using with Python

The server can be used with Python through the MCP environment wrapper:

```python
from src.mcp_environment import MCPEnvironmentWrapper

# Create the environment wrapper
env = MCPEnvironmentWrapper("zork-tools")

# Reset the environment to get the initial state
initial_state = env.reset()

# Take a step in the environment
result = env.step("look")
```

## Development

### Project Structure

```
zork-tools/
├── src/
│   ├── index.ts              # Main server implementation
│   ├── mock-environment.ts   # Mock Zork environment
│   └── tools/                # Tool implementations
│       ├── navigation.ts     # Navigation tool
│       ├── examination.ts    # Examination tool
│       ├── inventory.ts      # Inventory tool
│       ├── take.ts           # Take tool
│       ├── drop.ts           # Drop tool
│       ├── read.ts           # Read tool
│       ├── open.ts           # Open tool
│       ├── close.ts          # Close tool
│       ├── put.ts            # Put tool
│       ├── lamp.ts           # Lamp tool
│       └── move.ts           # Move tool
├── build/                    # Compiled JavaScript
├── package.json              # Project configuration
└── tsconfig.json             # TypeScript configuration
```

### Adding New Tools

To add a new tool:

1. Create a new file in the `src/tools` directory
2. Implement the tool handler function
3. Import the handler in `src/index.ts`
4. Add the tool to the list in the `setupToolHandlers` method
5. Add a case for the tool in the `CallToolRequestSchema` handler

## Integration with AI Agents

This MCP server is designed to work with AI agents that support the Model Context Protocol. It enables more structured interactions with the Zork environment, allowing agents to:

1. Select specific tools for different actions
2. Provide structured parameters for those tools
3. Receive structured responses

This approach has several advantages over generating raw text commands:

- **Clarity**: The agent explicitly selects which action to take
- **Validation**: Parameters can be validated before execution
- **Structure**: Responses can include structured data alongside text
- **Extensibility**: New tools can be added without changing the agent code
