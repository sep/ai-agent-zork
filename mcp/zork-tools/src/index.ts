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

// Import tool handlers and definitions
import { handleNavigate, navigateToolDefinition } from './tools/navigation.js';
import { handleExamine, examineToolDefinition } from './tools/examination.js';
import { handleInventory, inventoryToolDefinition } from './tools/inventory.js';
import { handleTake, takeToolDefinition } from './tools/take.js';
import { handleDrop, dropToolDefinition } from './tools/drop.js';
import { handleRead, readToolDefinition } from './tools/read.js';
import { handleOpen, openToolDefinition } from './tools/open.js';
import { handleClose, closeToolDefinition } from './tools/close.js';
import { handlePut, putToolDefinition } from './tools/put.js';
import { handleLamp, lampToolDefinition } from './tools/lamp.js';
import { handleMove, moveToolDefinition } from './tools/move.js';

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
        navigateToolDefinition,
        examineToolDefinition,
        inventoryToolDefinition,
        takeToolDefinition,
        dropToolDefinition,
        readToolDefinition,
        openToolDefinition,
        closeToolDefinition,
        putToolDefinition,
        lampToolDefinition,
        moveToolDefinition
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
