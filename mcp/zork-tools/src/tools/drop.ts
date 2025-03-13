/**
 * Drop tool for the Zork MCP server.
 * Handles dropping objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface DropArgs {
  object: string;
}

/**
 * Handle drop commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The drop arguments
 * @returns The result of the drop command
 */
export function handleDrop(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid object. Please specify a valid object to drop.'
        }
      ],
      isError: true
    };
  }

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
  // Check if the object is in the inventory
  const inventory = environment.getInventory();
  if (!inventory.includes(object)) {
    return {
      content: [
        {
          type: 'text',
          text: `You're not carrying ${object}.`
        }
      ],
      isError: true
    };
  }
  
  // Execute the drop command
  const result = environment.step(`drop ${object}`);
  
  // Check if the drop was successful by comparing inventory before and after
  const wasSuccessful = result.observation.toLowerCase().includes('dropped') || 
                        (inventory.length > result.inventory.length);
  
  // Return the result
  return {
    content: [
      {
        type: 'text',
        text: result.observation
      },
      {
        type: 'json',
        json: {
          success: wasSuccessful,
          inventory: result.inventory
        }
      }
    ]
  };
}
