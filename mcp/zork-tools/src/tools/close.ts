/**
 * Close tool for the Zork MCP server.
 * Handles closing objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const CloseArgsSchema = z.object({
  object: z.string()
});

export const closeToolDefinition = {
  name: 'close',
  description: 'Close an object like a mailbox or door',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object to close'
      }
    },
    required: ['object']
  },
  examples: [
    {
      name: 'Close mailbox',
      args: { object: 'mailbox' }
    },
    {
      name: 'Close door',
      args: { object: 'door' }
    }
  ]
};

/**
 * Handle close commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The close arguments
 * @returns The result of the close action
 */
export function handleClose(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = CloseArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    
    // Execute the close command
    const result = environment.step(`close ${object}`);
    
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
          text: 'Invalid object. Please specify a valid object to close.'
        }
      ],
      isError: true
    };
  }
}
