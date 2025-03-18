/**
 * Navigation tool for the Zork MCP server.
 * Handles movement in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const NavigateArgsSchema = z.object({
  direction: z.string()
});

export const navigateToolDefinition = {
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
  },
  examples: [
    {
      name: 'Go north',
      args: { direction: 'north' }
    },
    {
      name: 'Go up',
      args: { direction: 'up' }
    }
  ]
};

/**
 * Handle navigation commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The navigation arguments
 * @returns The result of the navigation
 */
export function handleNavigate(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = NavigateArgsSchema.parse(args);
    const direction = validatedArgs.direction.toLowerCase().trim();
    
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
  } catch (error) {
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
}
