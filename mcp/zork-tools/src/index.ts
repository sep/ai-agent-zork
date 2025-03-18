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
import { handleExamine, examineToolDefinition } from './tools/examine.js';
import { handleInventory, inventoryToolDefinition } from './tools/inventory.js';
import { handleTake, takeToolDefinition } from './tools/take.js';
import { handleDrop, dropToolDefinition } from './tools/drop.js';
import { handleRead, readToolDefinition } from './tools/read.js';
import { handleOpen, openToolDefinition } from './tools/open.js';
import { handleClose, closeToolDefinition } from './tools/close.js';
import { handlePut, putToolDefinition } from './tools/put.js';
import { handleLamp, lampToolDefinition } from './tools/lamp.js';
import { handleMove, moveToolDefinition } from './tools/move.js';
import { handleLook, lookToolDefinition } from './tools/look.js';

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
                moveToolDefinition,
                lookToolDefinition
              ]
    }));

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const { name, arguments: args = {} } = request.params;
        switch (name) {
          case 'navigate':
            return handleNavigate(this.environment, args);
          case 'examine':
            return handleExamine(this.environment, args);
          case 'inventory':
            return handleInventory(this.environment);
          case 'take':
            return handleTake(this.environment, args);
          case 'drop':
            return handleDrop(this.environment, args);
          case 'read':
            return handleRead(this.environment, args);
          case 'look':
            return handleLook(this.environment);
          case 'open':
            return handleOpen(this.environment, args);
          case 'close':
            return handleClose(this.environment, args);
          case 'put':
            return handlePut(this.environment, args);
          case 'lamp':
            return handleLamp(this.environment, args);
          case 'move':
            return handleMove(this.environment, args);
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

const server = new ZorkToolsServer();
server.run().catch(console.error);
