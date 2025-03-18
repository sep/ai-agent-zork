/**
 * Take tool for the Zork MCP server.
 * Handles picking up objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const TakeArgsSchema = z.object({
  object: z.string()
});

export const takeToolDefinition = {
  name: 'take',
  description: 'Pick up an object',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object to pick up'
      }
    },
    required: ['object']
  },
  examples: [
    {
      name: 'Take a key',
      args: { object: 'key' }
    },
    {
      name: 'Take a leaflet',
      args: { object: 'leaflet' }
    }
  ]
};

/**
 * Handle take commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The take arguments
 * @returns The result of the take action
 */
export function handleTake(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = TakeArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    
    // Execute the take command
    const result = environment.step(`take ${object}`);
    
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
          text: 'Invalid object. Please specify a valid object to take.'
        }
      ],
      isError: true
    };
  }
}
