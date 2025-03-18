/**
 * Move tool for the Zork MCP server.
 * Handles moving objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const MoveArgsSchema = z.object({
  object: z.string()
});

export class MoveTool extends Tool<z.infer<typeof MoveArgsSchema>> {
  protected schema = MoveArgsSchema;

  protected name = 'move';
  protected description = 'Move an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to move'
    }
  };
  protected examples = [
    {
      name: 'Move rug',
      args: { object: 'rug' }
    },
    {
      name: 'Move rock',
      args: { object: 'rock' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof MoveArgsSchema>): string {
    return `move ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to move.';
  }
}
