/**
 * Lamp tool for the Zork MCP server.
 * Handles controlling the lamp in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const LampArgsSchema = z.object({
  action: z.enum(['on', 'off'])
});

export const lampToolDefinition = {
  name: 'lamp',
  description: 'Turn the lamp on or off',
  inputSchema: {
    type: 'object',
    properties: {
      action: {
        type: 'string',
        description: 'Action to perform with the lamp (on or off)',
        enum: ['on', 'off']
      }
    },
    required: ['action']
  },
  examples: [
    {
      name: 'Turn lamp on',
      args: { action: 'on' }
    },
    {
      name: 'Turn lamp off',
      args: { action: 'off' }
    }
  ]
};

/**
 * Handle lamp commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The lamp arguments
 * @returns The result of the lamp action
 */
export function handleLamp(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = LampArgsSchema.parse(args);
    const action = validatedArgs.action;
    
    // Execute the lamp command
    const result = environment.step(`turn ${action} lamp`);
    
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
          text: 'Invalid action. Please specify either "on" or "off".'
        }
      ],
      isError: true
    };
  }
}
