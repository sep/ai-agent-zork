/**
 * Take tool for the Zork MCP server.
 * Handles picking up objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const TakeArgsSchema = z.object({
  object: z.string()
});

export class TakeTool extends Tool<z.infer<typeof TakeArgsSchema>> {
  protected schema = TakeArgsSchema;

  protected name = 'take';
  protected description = 'Pick up an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to pick up'
    }
  };
  protected examples = [
    {
      name: 'Take a key',
      args: { object: 'key' }
    },
    {
      name: 'Take a leaflet',
      args: { object: 'leaflet' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof TakeArgsSchema>): string {
    return `take ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to take.';
  }
}
