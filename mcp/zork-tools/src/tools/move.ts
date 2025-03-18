/**
 * Move tool for the Zork MCP server.
 * Handles moving objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface MoveArgs {
  object: string;
}

export const moveToolDefinition = {
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
  },
  examples: [
    {
      name: 'Move rug',
      args: { object: 'rug' }
    },
    {
      name: 'Move rock',
      args: { object: 'rock' }
    }
  ]
};

/**
 * Handle move commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The move arguments
 * @returns The result of the move action
 */
export function handleMove(environment: MockZorkEnvironment, args: MoveArgs) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid object. Please specify a valid object to move.'
        }
      ],
      isError: true
    };
  }

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
  // Execute the move command
  const result = environment.step(`move ${object}`);
  
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
