/**
 * Read tool for the Zork MCP server.
 * Handles reading objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const ReadArgsSchema = z.object({
  object: z.string()
});

export class ReadTool extends Tool<z.infer<typeof ReadArgsSchema>> {
  protected schema = ReadArgsSchema;

  protected name = 'read';
  protected description = 'Read an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to read'
    }
  };
  protected examples = [
    {
      name: 'Read leaflet',
      args: { object: 'leaflet' }
    },
    {
      name: 'Read sign',
      args: { object: 'sign' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof ReadArgsSchema>): string {
    return `read ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to read.';
  }
}
