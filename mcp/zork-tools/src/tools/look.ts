/**
 * Look tool for the Zork MCP server.
 * Handles looking at the current location in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

export const lookToolDefinition = {
  name: 'look',
  description: 'Look at your current location'
};

/**
 * Handle look commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @returns The result of the look command
 */
export function handleLook(environment: MockZorkEnvironment) {
  // Execute the look command
  const result = environment.step('look');
  
  // Return the result
  return {
    content: [
      {
        type: 'text',
        text: result.observation
      }
    ]
  };
} 