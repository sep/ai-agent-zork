/**
 * Drop tool for the Zork MCP server.
 * Handles dropping objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const DropArgsSchema = z.object({
  object: z.string()
});

export const dropToolDefinition = {
  name: 'drop',
  description: 'Drop an object from your inventory',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object to drop'
      }
    },
    required: ['object']
  },
  examples: [
    {
      name: 'Drop leaflet',
      args: { object: 'leaflet' }
    },
    {
      name: 'Drop sword',
      args: { object: 'sword' }
    }
  ]
};

/**
 * Handle drop commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The drop arguments
 * @returns The result of the drop action
 */
export function handleDrop(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = DropArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    
    // Execute the drop command
    const result = environment.step(`drop ${object}`);
    
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
          text: 'Invalid object. Please specify a valid object to drop.'
        }
      ],
      isError: true
    };
  }
}
