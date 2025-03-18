/**
 * Examine tool for the Zork MCP server.
 * Handles examining objects in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const ExamineArgsSchema = z.object({
  object: z.string()
});

export class ExamineTool extends Tool<z.infer<typeof ExamineArgsSchema>> {
  protected schema = ExamineArgsSchema;

  protected name = 'examine';
  protected description = 'Examine an object';
  protected inputProperties = {
    object: {
      type: 'string',
      description: 'Object to examine'
    }
  };
  protected examples = [
    {
      name: 'Examine mailbox',
      args: { object: 'mailbox' }
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment, args: z.infer<typeof ExamineArgsSchema>): string {
    return `examine ${args.object}`;
  }

  protected getErrorMessage(): string {
    return 'Invalid object. Please specify an object to examine.';
  }
}
