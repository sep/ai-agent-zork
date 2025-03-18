/**
 * Drop tool for the Zork MCP server.
 * Handles dropping objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const DropArgsSchema = z.object({
  object: z.string()
});

export class DropTool extends Tool<z.infer<typeof DropArgsSchema>> {
  protected schema = DropArgsSchema;

  protected name = 'drop';
  protected description = 'Drop an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to drop'
    }
  };
  protected examples = [
    {
      name: 'Drop leaflet',
      args: { object: 'leaflet' }
    },
    {
      name: 'Drop sword',
      args: { object: 'sword' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof DropArgsSchema>): string {
    return `drop ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to drop.';
  }
}
