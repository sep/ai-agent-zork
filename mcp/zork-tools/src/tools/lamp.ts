/**
 * Lamp tool for the Zork MCP server.
 * Handles turning the lamp on and off in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';

interface LampArgs {
  action: 'on' | 'off';
}

/**
 * Handle lamp commands in the Zork environment.
 * 
 * @param environment The Zork environment
 * @param args The lamp arguments
 * @returns The result of the lamp action
 */
export function handleLamp(environment: MockZorkEnvironment, args: any) {
  // Validate arguments
  if (!args || (args.action !== 'on' && args.action !== 'off')) {
    return {
      content: [
        {
          type: 'text',
          text: 'Invalid action. Please specify either "on" or "off" for the lamp.'
        }
      ],
      isError: true
    };
  }

  // Execute the lamp command
  const result = environment.step(`turn ${args.action} lamp`);
  
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
