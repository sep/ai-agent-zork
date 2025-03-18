/**
 * Examine tool for the Zork MCP server.
 * Handles examining objects and locations in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';

const ExamineArgsSchema = z.object({
  object: z.string()
});

export const examineToolDefinition = {
  name: 'examine',
  description: 'Examine an object or location',
  inputSchema: {
    type: 'object',
    properties: {
      object: {
        type: 'string',
        description: 'Object or location to examine'
      }
    },
    required: ['object']
  },
  examples: [
    {
      name: 'Examine a key',
      args: { object: 'key' }
    },
    {
      name: 'Examine the room',
      args: { object: 'room' }
    }
  ]
};

/**
 * Handle examine commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The examine arguments
 * @returns The result of the examination
 */
export function handleExamine(environment: MockZorkEnvironment, args: unknown) {
  try {
    const validatedArgs = ExamineArgsSchema.parse(args);
    const object = validatedArgs.object.toLowerCase().trim();
    
    // Execute the examine command
    const result = environment.step(`examine ${object}`);
    
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
          text: 'Invalid object. Please specify a valid object to examine.'
        }
      ],
      isError: true
    };
  }
}
