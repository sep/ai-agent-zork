/**
 * Look tool for the Zork MCP server.
 * Handles looking at the current location in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const LookArgsSchema = z.object({});

export class LookTool extends Tool<z.infer<typeof LookArgsSchema>> {
  protected schema = LookArgsSchema;

  protected name = 'look';
  protected description = 'Look at your current location';
  protected inputProperties = {};
  protected examples = [
    {
      name: 'Look around',
      args: {}
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment): string {
    return 'look';
  }

  protected getErrorMessage(): string {
    return 'Failed to look around.';
  }
} 