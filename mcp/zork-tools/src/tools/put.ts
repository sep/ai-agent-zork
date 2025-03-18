/**
 * Put tool for the Zork MCP server.
 * Handles putting objects in containers in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const PutArgsSchema = z.object({
  object: z.string(),
  container: z.string()
});

export class PutTool extends Tool<z.infer<typeof PutArgsSchema>> {
  protected schema = PutArgsSchema;

  protected name = 'put';
  protected description = 'Put an object in a container';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to put'
    },
    container: {
      type: 'string',
      description: 'Container to put the object in'
    }
  };
  protected examples = [
    {
      name: 'Put leaflet in mailbox',
      args: { object: 'leaflet', container: 'mailbox' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof PutArgsSchema>): string {
    return `put ${args.object} in ${args.container}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid arguments. Please specify both an object to put and a container to put it in.';
  }
}
