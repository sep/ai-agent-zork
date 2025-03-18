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

// Import tool classes
import { NavigateTool } from './tools/navigation.js';
import { ExamineTool } from './tools/examine.js';
import { InventoryTool } from './tools/inventory.js';
import { TakeTool } from './tools/take.js';
import { DropTool } from './tools/drop.js';
import { ReadTool } from './tools/read.js';
import { OpenTool } from './tools/open.js';
import { CloseTool } from './tools/close.js';
import { PutTool } from './tools/put.js';
import { LampTool } from './tools/lamp.js';
import { MoveTool } from './tools/move.js';
import { LookTool } from './tools/look.js';

class ZorkToolsServer {
  private server: Server;
  private environment: MockZorkEnvironment;
  private tools = {
    navigate: new NavigateTool(),
    examine: new ExamineTool(),
    inventory: new InventoryTool(),
    take: new TakeTool(),
    drop: new DropTool(),
    read: new ReadTool(),
    open: new OpenTool(),
    close: new CloseTool(),
    put: new PutTool(),
    lamp: new LampTool(),
    move: new MoveTool(),
    look: new LookTool()
  };

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
      tools: Object.values(this.tools).map(tool => tool.toolDefinition)
    }));

    // Handle tool execution
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      try {
        const { name, arguments: args = {} } = request.params;
        const tool = this.tools[name as keyof typeof this.tools];
        
        if (!tool) {
          throw new McpError(
            ErrorCode.MethodNotFound,
            `Unknown tool: ${request.params.name}`
          );
        }

        return tool.handle(this.environment, args);
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
