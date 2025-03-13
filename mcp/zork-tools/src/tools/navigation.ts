/**
 * Navigation tool for the Zork MCP server.
 * Handles movement commands in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface NavigateArgs {
  direction: string;
}

/**
 * Handle navigation commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The navigation arguments
 * @returns The result of the navigation
 */
export function handleNavigate(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.direction !== 'string') {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid direction. Please specify a valid direction (north, south, east, west, up, down, etc.).'
        }
      ],
      isError: true
    };
  }

  // Normalize the direction
  const direction = args.direction.toLowerCase().trim();
  
  // Execute the movement command
  const result = environment.step(`go ${direction}`);
  
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
