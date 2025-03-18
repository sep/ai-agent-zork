/**
 * Put tool for the Zork MCP server.
 * Handles putting objects into containers in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const PutArgsSchema = z.object({
  object: z.string(),
  container: z.string()
});

export const putToolDefinition = {
  name: 'put',
  description: 'Put an object into a container',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object to put'
      },
      container: {
        type: 'string',
        description: 'Container to put the object in'
      }
    },
    required: ['object', 'container']
  },
  examples: [
    {
      name: 'Put leaflet in mailbox',
      args: { object: 'leaflet', container: 'mailbox' }
    },
    {
      name: 'Put sword in case',
      args: { object: 'sword', container: 'case' }
    }
  ]
};

/**
 * Handle put commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The put arguments
 * @returns The result of the put action
 */
export function handlePut(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = PutArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    const container = validatedArgs.container.toLowerCase().trim();
    
    // Execute the put command
    const result = environment.step(`put ${object} in ${container}`);
    
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
          text: 'Invalid arguments. Please specify a valid object and container.'
        }
      ],
      isError: true
    };
  }
}
