import { z } from 'zod';
import { MockZorkEnvironment } from '../mock-environment.js';

export abstract class Tool<T> {
  protected abstract schema: z.ZodType<T>;
  protected abstract name: string;
  protected abstract description: string;
  protected abstract examples: Array<{name: string, args: T}>;
  protected abstract inputProperties: Record<string, { type: string, description: string }>;

  public get toolDefinition() {
    return {
      name: this.name,
      description: this.description,
      inputSchema: {
        type: 'object',
        properties: this.inputProperties,
        required: Object.keys(this.inputProperties)
      },
      examples: this.examples
    };
  }

  protected abstract executeCommand(environment: MockZorkEnvironment, args: T): string;

  public handle(environment: MockZorkEnvironment, args: unknown) {
    try {
      const validatedArgs = this.schema.parse(args);
      const result = environment.step(this.executeCommand(environment, validatedArgs));
      
      return {
        content: [
          {
            type: 'text',
            text: result.observation
          }
        ]
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: this.getErrorMessage(error)
          }
        ],
        isError: true
      };
    }
  }

  protected getErrorMessage(error: unknown): string {
    if (error instanceof z.ZodError) {
      return `Invalid arguments. ${error.errors[0].message}`;
    }
    return 'An error occurred while executing the command.';
  }
} 