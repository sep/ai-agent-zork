/**
 * Turn tool for the Zork MCP server.
 * Handles turning objects on/off in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const TurnArgsSchema = z.object({
  action: z.enum(['on', 'off']),
  object: z.string()
}).transform(args => ({
  ...args,
  object: args.object || 'lamp'
}));

export class TurnTool extends Tool<z.infer<typeof TurnArgsSchema>> {
  protected schema = TurnArgsSchema;

  protected name = 'turn';
  protected description = 'Turn an object on or off';
  protected inputProperties = {
    action: {
      type: 'string',
      description: 'Action to perform (on or off)',
      enum: ['on', 'off']
    },
    object: {
      type: 'string',
      description: 'Object to turn on/off (defaults to lamp)'
    }
  };
  protected examples = [
    {
      name: 'Turn lamp on',
      args: { action: 'on' as const, object: 'lamp' }
    },
    {
      name: 'Turn lamp off',
      args: { action: 'off' as const, object: 'lamp' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof TurnArgsSchema>): string {
    return `turn ${args.action} ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid arguments. Please specify "on" or "off" for the action.';
  }
}
