/**
 * Open tool for the Zork MCP server.
 * Handles opening objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const OpenArgsSchema = z.object({
  object: z.string()
});

export class OpenTool extends Tool<z.infer<typeof OpenArgsSchema>> {
  protected schema = OpenArgsSchema;

  protected name = 'open';
  protected description = 'Open an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to open'
    }
  };
  protected examples = [
    {
      name: 'Open mailbox',
      args: { object: 'mailbox' }
    },
    {
      name: 'Open door',
      args: { object: 'door' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof OpenArgsSchema>): string {
    return `open ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to open.';
  }
}
