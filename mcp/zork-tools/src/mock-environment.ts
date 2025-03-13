/**
 * TypeScript version of the MockZorkEnvironment from the Python implementation.
 * This is a simplified adapter that forwards commands to the Python environment.
 */

// In a real implementation, this would directly implement the environment logic
// For now, we'll create a simplified version that mimics the Python implementation

export interface Location {
  description: string;
  exits: Record<string, string | null>;
  objects: string[];
}

export interface ObjectState {
  location: string;
  open?: boolean;
  read?: boolean;
  on?: boolean;
  moved?: boolean;
}

export interface GameState {
  observation: string;
  score: number;
  done: boolean;
  moves: number;
  valid_actions: string[];
  inventory: string[];
  location: string;
}

export class MockZorkEnvironment {
  private current_location: string;
  private inventory: string[];
  private score: number;
  private moves: number;
  private max_moves: number;
  private done: boolean;
  private object_states: Record<string, ObjectState>;
  private locations: Record<string, Location>;
  private dark_locations: Set<string>;
  private grue_warning_given: boolean;

  constructor() {
    this.current_location = "west_of_house";
    this.inventory = [];
    this.score = 0;
    this.moves = 0;
    this.max_moves = 1000;
    this.done = false;
    this.grue_warning_given = false;
    this.dark_locations = new Set(["cellar"]);

    // Initialize object states
    this.object_states = {
      "mailbox": { open: false, location: "west_of_house" },
      "leaflet": { read: false, location: "in_mailbox" },
      "lamp": { on: false, location: "living_room" },
      "sword": { location: "living_room" },
      "trophy_case": { open: true, location: "living_room" },
      "rug": { moved: false, location: "living_room" },
      "egg": { location: "forest" },
      "water": { location: "stream" }
    };

    // Initialize locations
    this.locations = {
      "west_of_house": {
        description: "You are standing in an open field west of a white house, with a boarded front door.",
        exits: { "north": "north_of_house", "south": "south_of_house", "west": "forest", "east": "behind_house" },
        objects: ["mailbox"]
      },
      "north_of_house": {
        description: "You are facing the north side of a white house. There is no door here, and all the windows are boarded up.",
        exits: { "west": "west_of_house", "east": "behind_house" },
        objects: []
      },
      "south_of_house": {
        description: "You are facing the south side of a white house. There is no door here, and all the windows are boarded.",
        exits: { "west": "west_of_house", "east": "behind_house" },
        objects: []
      },
      "behind_house": {
        description: "You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which is slightly ajar.",
        exits: { "west": "west_of_house", "north": "north_of_house", "south": "south_of_house", "east": "forest", "window": "kitchen" },
        objects: []
      },
      "kitchen": {
        description: "You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. A passage leads to the west and a dark staircase can be seen leading upward. To the east is a small window which is open.",
        exits: { "west": "living_room", "up": "upstairs", "window": "behind_house" },
        objects: ["table", "sack"]
      },
      "upstairs": {
        description: "You are in the attic. The only exit is a stairway leading down.",
        exits: { "down": "kitchen" },
        objects: ["rope", "knife"]
      },
      "living_room": {
        description: "You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, and a large oriental rug in the center of the room.",
        exits: { 
          "east": "kitchen", 
          "west": null, 
          "down": this.object_states["rug"]?.moved ? "cellar" : null 
        },
        objects: ["lamp", "sword", "trophy_case", "rug"]
      },
      "cellar": {
        description: "You are in a dark and damp cellar with a narrow passageway leading north, and a crawlway to the south. On the west is the bottom of a steep metal ramp which is unclimbable.",
        exits: { "north": "troll_room", "south": "east_of_chasm", "up": "living_room" },
        objects: []
      },
      "forest": {
        description: "This is a forest, with trees in all directions. To the east, there appears to be sunlight.",
        exits: { "west": "west_of_house", "east": "clearing", "north": "clearing", "south": "forest" },
        objects: ["egg"]
      },
      "clearing": {
        description: "You are in a small clearing in a well marked forest path that extends to the east and west.",
        exits: { "west": "forest", "east": "canyon_view" },
        objects: []
      },
      "canyon_view": {
        description: "You are at the top of the Great Canyon on its west wall. From here there is a marvelous view of the canyon and parts of the Frigid River upstream. Across the canyon, the walls of the White Cliffs join the mighty ramparts of the Flathead Mountains to the east.",
        exits: { "west": "clearing", "down": "rocky_ledge" },
        objects: []
      },
      "rocky_ledge": {
        description: "You are on a ledge in the middle of the Great Canyon. From here there is a spectacular view of the canyon and the Frigid River below. The canyon wall is too steep to climb, but a chimney leads upward.",
        exits: { "up": "canyon_view" },
        objects: ["nest"]
      },
      "stream": {
        description: "You are in a small chamber filled with water. The only exit is to the west.",
        exits: { "west": "reservoir" },
        objects: ["water"]
      }
    };
  }

  reset(): GameState {
    // Reset the environment to its initial state
    this.current_location = "west_of_house";
    this.inventory = [];
    this.score = 0;
    this.moves = 0;
    this.done = false;
    this.grue_warning_given = false;

    // Reset object states
    this.object_states = {
      "mailbox": { open: false, location: "west_of_house" },
      "leaflet": { read: false, location: "in_mailbox" },
      "lamp": { on: false, location: "living_room" },
      "sword": { location: "living_room" },
      "trophy_case": { open: true, location: "living_room" },
      "rug": { moved: false, location: "living_room" },
      "egg": { location: "forest" },
      "water": { location: "stream" }
    };

    // Update living room exits
    this.locations["living_room"].exits.down = null;

    return {
      observation: this._getLocationDescription(),
      score: this.score,
      done: this.done,
      moves: this.moves,
      valid_actions: this.getValidActions(),
      inventory: this.getInventory(),
      location: this.current_location
    };
  }

  step(action: string): GameState {
    // Take a step in the game by executing the given action
    this.moves++;

    // Check for maximum moves
    if (this.moves >= this.max_moves) {
      this.done = true;
      return {
        observation: "You have exceeded the maximum number of moves.",
        score: this.score,
        done: this.done,
        moves: this.moves,
        valid_actions: [],
        inventory: this.getInventory(),
        location: this.current_location
      };
    }

    // Process the action
    const result = this._processAction(action.toLowerCase());

    // Check for death by grue in dark locations
    if (this.dark_locations.has(this.current_location) && !this._hasLight()) {
      if (!this.grue_warning_given && !result.includes("grue")) {
        this.grue_warning_given = true;
        return {
          observation: "It is pitch black. You are likely to be eaten by a grue.\n\n" + result,
          score: this.score,
          done: this.done,
          moves: this.moves,
          valid_actions: this.getValidActions(),
          inventory: this.getInventory(),
          location: this.current_location
        };
      } else if (this.grue_warning_given && this.moves % 3 === 0) {
        this.done = true;
        return {
          observation: "Oh, no! You have walked into the slavering fangs of a lurking grue!\n\n***** You have died *****",
          score: this.score,
          done: this.done,
          moves: this.moves,
          valid_actions: [],
          inventory: this.getInventory(),
          location: this.current_location
        };
      }
    }

    return {
      observation: result,
      score: this.score,
      done: this.done,
      moves: this.moves,
      valid_actions: this.getValidActions(),
      inventory: this.getInventory(),
      location: this.current_location
    };
  }

  getValidActions(): string[] {
    // Get a list of valid actions in the current game state
    const validActions: string[] = [];

    // Add movement actions
    const location = this.locations[this.current_location];
    for (const [direction, destination] of Object.entries(location.exits)) {
      if (destination) {
        if (direction === "window") {
          validActions.push("enter window");
          validActions.push("go through window");
        } else {
          validActions.push(`go ${direction}`);
          validActions.push(direction);
        }
      }
    }

    // Add object interactions for visible objects
    const visibleObjects = this._getVisibleObjects();
    for (const obj of visibleObjects) {
      validActions.push(`examine ${obj}`);
      validActions.push(`look at ${obj}`);

      if (!this.inventory.includes(obj)) {
        validActions.push(`take ${obj}`);
        validActions.push(`get ${obj}`);
      }

      if (this.inventory.includes(obj)) {
        validActions.push(`drop ${obj}`);
      }

      // Object-specific actions
      if (obj === "mailbox") {
        validActions.push(`open ${obj}`);
        validActions.push(`close ${obj}`);
      }

      if (obj === "lamp" && this.inventory.includes(obj)) {
        validActions.push(`turn on ${obj}`);
        validActions.push(`turn off ${obj}`);
      }

      // Add read action for leaflet if it's in inventory
      if (obj === "leaflet" && (this.object_states["leaflet"].location === "inventory" || this.inventory.includes("leaflet"))) {
        validActions.push(`read ${obj}`);
      }

      if (obj === "rug") {
        validActions.push(`move ${obj}`);
        validActions.push(`lift ${obj}`);
      }
    }

    // Add general actions
    validActions.push("look", "inventory", "i", "help", "score");

    return validActions;
  }

  getInventory(): string[] {
    // Return the current inventory
    return [...this.inventory];
  }

  private _getLocationDescription(): string {
    // Get the description of the current location
    if (this.dark_locations.has(this.current_location) && !this._hasLight()) {
      return "It is pitch black.";
    }

    const location = this.locations[this.current_location];
    let description = location.description;

    // Add visible objects
    const visibleObjects: string[] = [];
    for (const obj of location.objects) {
      if (this.object_states[obj]?.location === this.current_location) {
        if (obj === "mailbox") {
          const status = this.object_states["mailbox"].open ? "open" : "closed";
          visibleObjects.push(`There is a ${status} mailbox here.`);

          // If mailbox is open and contains leaflet
          if (this.object_states["mailbox"].open && this.object_states["leaflet"].location === "in_mailbox") {
            visibleObjects.push("There is a small leaflet in the mailbox.");
          }
        } else if (obj === "lamp") {
          const status = this.object_states["lamp"].on ? "lit" : "turned off";
          visibleObjects.push(`There is a brass lamp here (${status}).`);
        } else if (obj === "sword") {
          visibleObjects.push("There is a sword of Elvish workmanship here.");
        } else if (obj === "trophy_case") {
          visibleObjects.push("There is a trophy case here.");
        } else if (obj === "rug") {
          const status = this.object_states["rug"].moved ? "moved aside" : "lying in the center of the room";
          visibleObjects.push(`There is a large oriental rug ${status}.`);
        } else {
          visibleObjects.push(`There is a ${obj} here.`);
        }
      }
    }

    if (visibleObjects.length > 0) {
      description += "\n\n" + visibleObjects.join("\n");
    }

    return description;
  }

  private _getVisibleObjects(): string[] {
    // Get a list of visible objects in the current location
    if (this.dark_locations.has(this.current_location) && !this._hasLight()) {
      return [];
    }

    const visibleObjects: string[] = [];

    // Add objects in the current location
    for (const obj of this.locations[this.current_location].objects) {
      if (this.object_states[obj]?.location === this.current_location) {
        visibleObjects.push(obj);
      }
    }

    // Add objects in open containers in the current location
    if (visibleObjects.includes("mailbox") && this.object_states["mailbox"].open && this.object_states["leaflet"].location === "in_mailbox") {
      visibleObjects.push("leaflet");
    }

    // Add objects in inventory
    visibleObjects.push(...this.inventory);

    return visibleObjects;
  }

  private _hasLight(): boolean {
    // Check if the player has a light source
    return this.inventory.includes("lamp") && this.object_states["lamp"]?.on === true;
  }

  private _processAction(action: string): string {
    // Process the given action and update the game state
    // Split the action into words
    const words = action.toLowerCase().split(/\s+/);
    if (words.length === 0) {
      return "I don't understand that.";
    }

    // Extract the verb and object
    const verb = words[0];
    const obj = words.length > 1 ? words[words.length - 1] : "";

    // Handle moving the rug (special case)
    if ((verb === "move" || verb === "lift") && obj === "rug") {
      return this._handleMoveRug();
    }

    // Handle movement
    if (["go", "walk", "north", "south", "east", "west", "up", "down", "enter"].includes(verb) || 
        Object.keys(this.locations[this.current_location].exits).includes(verb)) {
      return this._handleMovement(action);
    }

    // Handle looking
    if ((verb === "look" || verb === "l") && words.length === 1) {
      return this._getLocationDescription();
    }

    // Handle examining objects
    if ((verb === "examine" || verb === "look") && obj && obj !== "at") {
      return this._handleExamine(obj);
    }

    // Handle inventory
    if (verb === "inventory" || verb === "i") {
      return this.inventory.length === 0 ? 
        "You are not carrying anything." : 
        "You are carrying:\n" + this.inventory.map(item => `  ${item}`).join("\n");
    }

    // Handle taking objects
    if (["take", "get", "pick"].includes(verb)) {
      return this._handleTake(obj);
    }

    // Handle dropping objects
    if (["drop", "put"].includes(verb)) {
      return this._handleDrop(obj);
    }

    // Handle opening objects
    if (verb === "open") {
      return this._handleOpen(obj);
    }

    // Handle closing objects
    if (verb === "close") {
      return this._handleClose(obj);
    }

    // Handle turning on/off the lamp
    if (verb === "turn" && words.length > 1) {
      if (words[1] === "on" && obj === "lamp") {
        return this._handleTurnOnLamp();
      } else if (words[1] === "off" && obj === "lamp") {
        return this._handleTurnOffLamp();
      }
    }

    // Handle reading
    if (verb === "read") {
      return this._handleRead(obj);
    }

    // Handle score
    if (verb === "score") {
      return `Your score is ${this.score} (in ${this.moves} moves).`;
    }

    // Handle help
    if (verb === "help") {
      return (
        "Some useful commands:\n" +
        "- Movement: north, south, east, west, up, down\n" +
        "- Actions: look, examine [object], take [object], drop [object]\n" +
        "- Inventory: inventory or i\n" +
        "- Object interaction: open [object], close [object], read [object]\n" +
        "- Lamp: turn on lamp, turn off lamp\n" +
        "- Other: score, help"
      );
    }

    return "I don't understand that command.";
  }

  private _handleMovement(action: string): string {
    // Handle movement actions
    // Extract the direction
    const words = action.toLowerCase().split(/\s+/);
    let direction = words[0];

    // If the command is "go direction" or similar, use the last word
    if (["go", "move", "walk", "enter"].includes(direction)) {
      if (words.length > 1) {
        direction = words[words.length - 1];
      } else {
        return "Go where?";
      }
    }

    // Handle "enter window" or "go through window"
    if ((words.includes("enter") || words.includes("through")) && words.includes("window")) {
      direction = "window";
    }

    // Check if the direction is valid
    const exits = this.locations[this.current_location].exits;
    if (!(direction in exits)) {
      return "You can't go that way.";
    }

    // Check if the exit is blocked
    const destination = exits[direction];
    if (destination === null) {
      if (direction === "west" && this.current_location === "living_room") {
        return "The door is nailed shut.";
      } else if (direction === "down" && this.current_location === "living_room") {
        return "You can't go that way.";
      }
      return "You can't go that way.";
    }

    // Move to the new location
    this.current_location = destination;

    // Return the description of the new location
    return this._getLocationDescription();
  }

  private _handleExamine(obj: string): string {
    // Handle examining objects
    // Check if the object is visible
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes(obj) && !this.inventory.includes(obj)) {
      return "You don't see that here.";
    }

    // Return the description of the object
    if (obj === "mailbox") {
      const status = this.object_states["mailbox"].open ? "open" : "closed";
      let description = `It's a small ${status} mailbox.`;
      if (this.object_states["mailbox"].open && this.object_states["leaflet"].location === "in_mailbox") {
        description += " There is a small leaflet inside.";
      }
      return description;
    } else if (obj === "leaflet") {
      return "A small leaflet. It appears to contain instructions.";
    } else if (obj === "lamp") {
      const status = this.object_states["lamp"].on ? "on" : "off";
      return `It's a brass lamp. It is currently ${status}.`;
    } else if (obj === "sword") {
      return "The sword is made of Elvish workmanship with strange runes on the blade.";
    } else if (obj === "trophy_case") {
      return "The trophy case is empty and waiting for treasures.";
    } else if (obj === "rug") {
      const status = this.object_states["rug"].moved ? "moved aside, revealing a trapdoor" : "lying in the center of the room";
      return `It's a large oriental rug, ${status}.`;
    } else if (obj === "egg") {
      return "The egg is covered with fine gold inlay, and is extremely valuable.";
    } else if (obj === "water") {
      return "The water is clear and refreshing.";
    } else {
      return `You see nothing special about the ${obj}.`;
    }
  }

  private _handleTake(obj: string): string {
    // Handle taking objects
    // Check if the object is visible
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes(obj)) {
      return "You don't see that here.";
    }

    // Check if the object is already in inventory
    if (this.inventory.includes(obj)) {
      return "You're already carrying that.";
    }

    // Check if the object can be taken
    if (["mailbox", "trophy_case", "rug"].includes(obj)) {
      return "You can't take that.";
    }

    // Check if the object is in a container
    if (obj === "leaflet" && this.object_states["leaflet"].location === "in_mailbox") {
      if (!this.object_states["mailbox"].open) {
        return "The mailbox is closed.";
      }
    }

    // Take the object
    if (obj === "leaflet") {
      this.object_states["leaflet"].location = "inventory";
    } else if (obj === "lamp") {
      this.object_states["lamp"].location = "inventory";
    } else if (obj === "sword") {
      this.object_states["sword"].location = "inventory";
    } else if (obj === "egg") {
      this.object_states["egg"].location = "inventory";
      this.score += 5;  // Award points for finding a treasure
    } else if (obj === "water") {
      return "The water slips through your fingers.";
    } else {
      return "You can't take that.";
    }

    this.inventory.push(obj);
    return "Taken.";
  }

  private _handleDrop(obj: string): string {
    // Handle dropping objects
    // Check if the object is in inventory
    if (!this.inventory.includes(obj)) {
      return "You're not carrying that.";
    }

    // Drop the object
    this.inventory = this.inventory.filter(item => item !== obj);

    if (obj === "leaflet") {
      this.object_states["leaflet"].location = this.current_location;
    } else if (obj === "lamp") {
      this.object_states["lamp"].location = this.current_location;
    } else if (obj === "sword") {
      this.object_states["sword"].location = this.current_location;
    } else if (obj === "egg") {
      this.object_states["egg"].location = this.current_location;
    }

    return "Dropped.";
  }

  private _handleOpen(obj: string): string {
    // Handle opening objects
    // Check if the object is visible
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes(obj) && !this.inventory.includes(obj)) {
      return "You don't see that here.";
    }

    // Handle specific objects
    if (obj === "mailbox") {
      if (this.object_states["mailbox"].open) {
        return "It's already open.";
      }

      this.object_states["mailbox"].open = true;

      if (this.object_states["leaflet"].location === "in_mailbox") {
        return "Opening the mailbox reveals a small leaflet.";
      }
      return "Opened.";
    } else if (obj === "trophy_case") {
      return "The trophy case is already open.";
    } else {
      return "You can't open that.";
    }
  }

  private _handleClose(obj: string): string {
    // Handle closing objects
    // Check if the object is visible
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes(obj) && !this.inventory.includes(obj)) {
      return "You don't see that here.";
    }

    // Handle specific objects
    if (obj === "mailbox") {
      if (!this.object_states["mailbox"].open) {
        return "It's already closed.";
      }

      this.object_states["mailbox"].open = false;
      return "Closed.";
    } else {
      return "You can't close that.";
    }
  }

  private _handleTurnOnLamp(): string {
    // Handle turning on the lamp
    // Check if the lamp is in inventory
    if (!this.inventory.includes("lamp")) {
      return "You're not carrying that.";
    }

    // Check if the lamp is already on
    if (this.object_states["lamp"].on) {
      return "The lamp is already on.";
    }

    // Turn on the lamp
    this.object_states["lamp"].on = true;
    return "The lamp is now on and providing light.";
  }

  private _handleTurnOffLamp(): string {
    // Handle turning off the lamp
    // Check if the lamp is in inventory
    if (!this.inventory.includes("lamp")) {
      return "You're not carrying that.";
    }

    // Check if the lamp is already off
    if (!this.object_states["lamp"].on) {
      return "The lamp is already off.";
    }

    // Turn off the lamp
    this.object_states["lamp"].on = false;

    // Check if in a dark location
    if (this.dark_locations.has(this.current_location)) {
      return "The lamp is now off. It is pitch black.";
    }

    return "The lamp is now off.";
  }

  private _handleRead(obj: string): string {
    // Handle reading objects
    // Check if the object is visible or in inventory
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes(obj) && !this.inventory.includes(obj)) {
      return "You don't see that here.";
    }

    // Handle specific objects
    if (obj === "leaflet") {
      if (!this.object_states["leaflet"].read) {
        this.object_states["leaflet"].read = true;
        this.score += 1;  // Award a point for reading the leaflet
      }

      return (
        "WELCOME TO ZORK!\n\n" +
        "ZORK is a game of adventure, danger, and low cunning. " +
        "In it you will explore some of the most amazing territory ever seen by mortals. " +
        "No computer should be without one!"
      );
    } else {
      return `There's nothing written on the ${obj}.`;
    }
  }

  private _handleMoveRug(): string {
    // Handle moving the rug
    // Check if the rug is visible
    const visibleObjects = this._getVisibleObjects();
    if (!visibleObjects.includes("rug")) {
      return "You don't see that here.";
    }

    // Check if the rug is already moved
    if (this.object_states["rug"].moved) {
      return "The rug has already been moved aside.";
    }

    // Move the rug
    this.object_states["rug"].moved = true;
    this.score += 2;  // Award points for discovering the trapdoor

    // Update the exits
    this.locations["living_room"].exits.down = "cellar";

    return "You move the rug aside, revealing a closed trapdoor in the floor.";
  }
}
