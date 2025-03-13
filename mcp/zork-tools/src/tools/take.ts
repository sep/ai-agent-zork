/**
 * Take tool for the Zork MCP server.
 * Handles taking objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface TakeArgs {
  object: string;
}

/**
 * Handle take commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The take arguments
 * @returns The result of the take command
 */
export function handleTake(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid object. Please specify a valid object to take.'
        }
      ],
      isError: true
    };
  }

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
  // Execute the take command
  const result = environment.step(`take ${object}`);
  
  // Check if the take was successful by comparing inventory before and after
  const inventoryBefore = environment.getInventory();
  const wasSuccessful = result.observation.toLowerCase().includes('taken') || 
                        (inventoryBefore.length < result.inventory.length);
  
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
