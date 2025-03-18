/**
 * Close tool for the Zork MCP server.
 * Handles closing objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const CloseArgsSchema = z.object({
  object: z.string()
});

export class CloseTool extends Tool<z.infer<typeof CloseArgsSchema>> {
  protected schema = CloseArgsSchema;

  protected name = 'close';
  protected description = 'Close an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to close'
    }
  };
  protected examples = [
    {
      name: 'Close mailbox',
      args: { object: 'mailbox' }
    },
    {
      name: 'Close door',
      args: { object: 'door' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof CloseArgsSchema>): string {
    return `close ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to close.';
  }
}
