/**
 * Navigation tool for the Zork MCP server.
 * Handles movement commands in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const NavigateArgsSchema = z.object({
  direction: z.enum(['north', 'south', 'east', 'west', 'up', 'down'])
});

export class NavigateTool extends Tool<z.infer<typeof NavigateArgsSchema>> {
  protected schema = NavigateArgsSchema;

  protected name = 'navigate';
  protected description = 'Move in a direction';
  protected inputProperties = {
    direction: {
      type: 'string',
      description: 'Direction to move (north, south, east, west, up, down)',
      enum: ['north', 'south', 'east', 'west', 'up', 'down']
    }
  };
  protected examples = [
    {
      name: 'Go north',
      args: { direction: 'north' as const }
    },
    {
      name: 'Go south',
      args: { direction: 'south' as const }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof NavigateArgsSchema>): string {
    return args.direction;
  }

  protected getErrorMessage(): string {
    return 'Invalid direction. Please specify one of: north, south, east, west, up, down';
  }
}
