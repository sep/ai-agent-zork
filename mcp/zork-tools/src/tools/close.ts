/**
 * Close tool for the Zork MCP server.
 * Handles closing objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface CloseArgs {
  object: string;
}

/**
 * Handle close commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The close arguments
 * @returns The result of the close action
 */
export function handleClose(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
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

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
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
}
