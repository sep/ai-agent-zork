/**
 * Open tool for the Zork MCP server.
 * Handles opening objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface OpenArgs {
  object: string;
}

/**
 * Handle open commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The open arguments
 * @returns The result of the open action
 */
export function handleOpen(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid object. Please specify a valid object to open.'
        }
      ],
      isError: true
    };
  }

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
  // Execute the open command
  const result = environment.step(`open ${object}`);
  
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
