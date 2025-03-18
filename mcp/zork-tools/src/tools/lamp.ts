/**
 * Lamp tool for the Zork MCP server.
 * Handles controlling the lamp in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const LampArgsSchema = z.object({
  action: z.enum(['on', 'off'])
});

export class LampTool extends Tool<z.infer<typeof LampArgsSchema>> {
  protected schema = LampArgsSchema;

  protected name = 'lamp';
  protected description = 'Turn the lamp on or off';
  protected inputProperties = {
    action: {
      type: 'string',
      description: 'Action to perform with the lamp (on or off)',
      enum: ['on', 'off']
    }
  };
  protected examples = [
    {
      name: 'Turn lamp on',
      args: { action: 'on' as const }
    },
    {
      name: 'Turn lamp off',
      args: { action: 'off' as const }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof LampArgsSchema>): string {
    return `turn ${args.action} lamp`;
  }

  protected getErrorMessage(): string {
    return 'Invalid action. Please specify either "on" or "off".';
  }
}
