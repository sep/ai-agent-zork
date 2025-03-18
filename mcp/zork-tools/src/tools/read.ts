/**
 * Read tool for the Zork MCP server.
 * Handles reading objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface ReadArgs {
  object: string;
}

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
 * @returns The result of the read command
 */
export function handleRead(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
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

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
  // We'll let the environment handle the visibility check
  // This is more robust than trying to check visibility ourselves
  
  // Execute the read command
  const result = environment.step(`read ${object}`);
  
  // Check if the read was successful
  const wasSuccessful = !result.observation.toLowerCase().includes("nothing written") && 
                        !result.observation.toLowerCase().includes("can't read");
  
  // Return the result
  return {
    content: [
      {
        type: 'text',
        text: result.observation
      },
      {
        type: 'json',
        json: {
          success: wasSuccessful,
          object: object
        }
      }
    ]
  };
}
