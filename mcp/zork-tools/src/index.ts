#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';

// Import the mock environment
import { MockZorkEnvironment } from './mock-environment.js';

// Import tool handlers
import { handleNavigate } from './tools/navigation.js';
import { handleExamine } from './tools/examination.js';
import { handleInventory } from './tools/inventory.js';
import { handleTake } from './tools/take.js';
import { handleDrop } from './tools/drop.js';
import { handleRead } from './tools/read.js';
import { handleOpen } from './tools/open.js';
import { handleClose } from './tools/close.js';
import { handlePut } from './tools/put.js';
import { handleLamp } from './tools/lamp.js';
import { handleMove } from './tools/move.js';

class ZorkToolsServer {
  private server: Server;
  private environment: MockZorkEnvironment;

  constructor() {
    this.server = new Server(
      {
        name: 'zork-tools',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Initialize the environment
    this.environment = new MockZorkEnvironment();
    
    // Set up tool handlers
    this.setupToolHandlers();
    
    // Error handling
    this.server.onerror = (error) => console.error('[MCP Error]', error);
    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'navigate',
          description: 'Move in a specified direction',
          inputSchema: {
            type: 'object',
            properties: {
              direction: {
                type: 'string',
                description: 'Direction to move (north, south, east, west, up, down, etc.)'
              }
            },
            required: ['direction']
          }
        },
        {
          name: 'examine',
          description: 'Examine an object in the environment',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to examine'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'inventory',
          description: 'Check your inventory',
          inputSchema: {
            type: 'object',
            properties: {}
          }
        },
        {
          name: 'take',
          description: 'Take an object',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to take'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'drop',
          description: 'Drop an object from your inventory',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to drop'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'read',
          description: 'Read an object with text',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to read'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'look',
          description: 'Look around to get a description of your surroundings',
          inputSchema: {
            type: 'object',
            properties: {}
          }
        },
        {
          name: 'open',
          description: 'Open an object like a mailbox or door',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to open'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'close',
          description: 'Close an object like a mailbox or door',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to close'
              }
            },
            required: ['object']
          }
        },
        {
          name: 'put',
          description: 'Put an object into a container',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to put'
              },
              container: {
                type: 'string',
                description: 'Container to put the object in'
              }
            },
            required: ['object', 'container']
          }
        },
        {
          name: 'lamp',
          description: 'Turn the lamp on or off',
          inputSchema: {
            type: 'object',
            properties: {
              action: {
                type: 'string',
                description: 'Action to perform with the lamp (on or off)',
                enum: ['on', 'off']
              }
            },
            required: ['action']
          }
        },
        {
          name: 'move',
          description: 'Move an object like the rug',
          inputSchema: {
            type: 'object',
            properties: {
              object: {
                type: 'string',
                description: 'Object to move'
              }
            },
            required: ['object']
          }
        }
      ]
    }));

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        switch (request.params.name) {
          case 'navigate':
            return handleNavigate(this.environment, request.params.arguments);
          case 'examine':
            return handleExamine(this.environment, request.params.arguments);
          case 'inventory':
            return handleInventory(this.environment);
          case 'take':
            return handleTake(this.environment, request.params.arguments);
          case 'drop':
            return handleDrop(this.environment, request.params.arguments);
          case 'read':
            return handleRead(this.environment, request.params.arguments);
          case 'look':
            return handleLook(this.environment);
          case 'open':
            return handleOpen(this.environment, request.params.arguments);
          case 'close':
            return handleClose(this.environment, request.params.arguments);
          case 'put':
            return handlePut(this.environment, request.params.arguments);
          case 'lamp':
            return handleLamp(this.environment, request.params.arguments);
          case 'move':
            return handleMove(this.environment, request.params.arguments);
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Unknown tool: ${request.params.name}`
            );
        }
      } catch (error) {
        if (error instanceof McpError) {
          throw error;
        }
        throw new McpError(
          ErrorCode.InternalError,
          `Error executing tool: ${error instanceof Error ? error.message : String(error)}`
        );
      }
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Zork Tools MCP server running on stdio');
  }
}

// Helper function for the look tool
function handleLook(environment: MockZorkEnvironment) {
  const result = environment.step('look');
  return {
    content: [
      {
        type: 'text',
        text: result.observation
      }
    ]
  };
}

const server = new ZorkToolsServer();
server.run().catch(console.error);
