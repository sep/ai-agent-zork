/**
 * Examination tool for the Zork MCP server.
 * Handles examining objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface ExamineArgs {
  object: string;
}

/**
 * Handle examination commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The examination arguments
 * @returns The result of the examination
 */
export function handleExamine(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || typeof args.object !== 'string') {
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

  // Normalize the object name
  const object = args.object.toLowerCase().trim();
  
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
}
