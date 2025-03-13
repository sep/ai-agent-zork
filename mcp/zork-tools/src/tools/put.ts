/**
 * Put tool for the Zork MCP server.
 * Handles putting objects into containers in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface PutArgs {
  object: string;
  container: string;
}

/**
 * Handle put commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The put arguments
 * @returns The result of the put action
 */
export function handlePut(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string' || typeof args.container !== 'string') {
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

  // Normalize the object and container names
  const object = args.object.toLowerCase().trim();
  const container = args.container.toLowerCase().trim();
  
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
}
