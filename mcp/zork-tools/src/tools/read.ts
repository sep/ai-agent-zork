/**
 * Read tool for the Zork MCP server.
 * Handles reading objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const ReadArgsSchema = z.object({
  object: z.string()
});

export const readToolDefinition = {
  name: 'read',
  description: 'Read an object with text',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object to read'
      }
    },
    required: ['object']
  },
  examples: [
    {
      name: 'Read leaflet',
      args: { object: 'leaflet' }
    },
    {
      name: 'Read sign',
      args: { object: 'sign' }
    }
  ]
};

/**
 * Handle read commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The read arguments
 * @returns The result of the read action
 */
export function handleRead(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = ReadArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    
    // Execute the read command
    const result = environment.step(`read ${object}`);
    
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
          text: 'Invalid object. Please specify a valid object to read.'
        }
      ],
      isError: true
    };
  }
}
