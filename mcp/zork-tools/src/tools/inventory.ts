/**
 * Inventory tool for the Zork MCP server.
 * Handles checking inventory in the Zork environment.
 */
import { MockZorkEnvironment } from '../mock-environment.js';
import { z } from 'zod';
import { Tool } from './tool.js';

const InventoryArgsSchema = z.object({});

export class InventoryTool extends Tool<z.infer<typeof InventoryArgsSchema>> {
  protected schema = InventoryArgsSchema;

  protected name = 'inventory';
  protected description = 'Check your inventory';
  protected inputProperties = {};
  protected examples = [
    {
      name: 'Check inventory',
      args: {}
    }
  ];

  protected executeCommand(environment: MockZorkEnvironment): string {
    return 'inventory';
  }

  protected getErrorMessage(error?: unknown): string {
    return 'Failed to check inventory.';
  }

  // Override handle to include inventory items as JSON
  public override handle(environment: MockZorkEnvironment, args: unknown): any {
    try {
      this.schema.parse(args);
      const result = environment.step(this.executeCommand(environment));
      const inventoryItems = environment.getInventory();
      
      return {
        content: [
          {
            type: 'text',
            text: result.observation
          },
          {
            type: 'json',
            json: {
              items: inventoryItems
            }
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
}
