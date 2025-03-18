/**
 * Inventory tool for the Zork MCP server.
 * Handles checking inventory in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

export const inventoryToolDefinition = {
  name: 'inventory',
  description: 'Check your inventory',
  inputSchema: {
    type: 'object',
    properties: {}
  },
  examples: [
    {
      name: 'Check inventory',
      args: {}
    }
  ]
};

/**
 * Handle inventory commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @returns The result of the inventory command
 */
export function handleInventory(environment: MockZorkEnvironment) {
  // Execute the inventory command
  const result = environment.step('inventory');
  
  // Get the inventory items as an array
  const inventoryItems = environment.getInventory();
  
  // Return the result with both text and structured data
  return {
    content: [
      {
        type: 'text',
        text: result.observation
      },
      {
        type: 'json',
        json: {
          items: inventoryItems
        }
      }
    ]
  };
}
