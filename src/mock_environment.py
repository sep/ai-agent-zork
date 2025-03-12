"""
Mock environment for Zork that simulates key aspects of the game.
This allows development of the AI agent without dependencies on external interpreters.
"""
from typing import Dict, List, Any, Optional, Set


class MockZorkEnvironment:
    """
    A simplified mock environment that simulates key aspects of Zork.
    """

    def __init__(self):
        """Initialize the mock Zork environment with game state."""
        # Current location
        self.current_location = "west_of_house"
        
        # Player inventory
        self.inventory: List[str] = []
        
        # Game state
        self.score = 0
        self.moves = 0
        self.max_moves = 1000
        self.game_over = False
        
        # Object states
        self.object_states = {
            "mailbox": {"open": False, "location": "west_of_house"},
            "leaflet": {"read": False, "location": "in_mailbox"},
            "lamp": {"on": False, "location": "living_room"},
            "sword": {"location": "living_room"},
            "trophy_case": {"open": True, "location": "living_room"},
            "rug": {"moved": False, "location": "living_room"},
            "egg": {"location": "forest"},
            "water": {"location": "stream"}
        }
        
        # Location data
        self.locations = {
            "west_of_house": {
                "description": "You are standing in an open field west of a white house, with a boarded front door.",
                "exits": {"north": "north_of_house", "south": "south_of_house", "west": "forest", "east": "behind_house"},
                "objects": ["mailbox"]
            },
            "north_of_house": {
                "description": "You are facing the north side of a white house. There is no door here, and all the windows are boarded up.",
                "exits": {"west": "west_of_house", "east": "behind_house"},
                "objects": []
            },
            "south_of_house": {
                "description": "You are facing the south side of a white house. There is no door here, and all the windows are boarded.",
                "exits": {"west": "west_of_house", "east": "behind_house"},
                "objects": []
            },
            "behind_house": {
                "description": "You are behind the white house. A path leads into the forest to the east. In one corner of the house there is a small window which is slightly ajar.",
                "exits": {"west": "west_of_house", "north": "north_of_house", "south": "south_of_house", "east": "forest", "window": "kitchen"},
                "objects": []
            },
            "kitchen": {
                "description": "You are in the kitchen of the white house. A table seems to have been used recently for the preparation of food. A passage leads to the west and a dark staircase can be seen leading upward. To the east is a small window which is open.",
                "exits": {"west": "living_room", "up": "upstairs", "window": "behind_house"},
                "objects": ["table", "sack"]
            },
            "living_room": {
                "description": "You are in the living room. There is a doorway to the east, a wooden door with strange gothic lettering to the west, which appears to be nailed shut, and a large oriental rug in the center of the room.",
                "exits": {"east": "kitchen", "west": None, "down": "cellar" if self.object_states.get("rug", {}).get("moved", False) else None},
                "objects": ["lamp", "sword", "trophy_case", "rug"]
            },
            "cellar": {
                "description": "You are in a dark and damp cellar with a narrow passageway leading north, and a crawlway to the south. On the west is the bottom of a steep metal ramp which is unclimbable.",
                "exits": {"north": "troll_room", "south": "east_of_chasm", "up": "living_room"},
                "objects": []
            },
            "forest": {
                "description": "This is a forest, with trees in all directions. To the east, there appears to be sunlight.",
                "exits": {"west": "west_of_house", "east": "clearing", "north": "clearing", "south": "forest"},
                "objects": ["egg"]
            },
            "clearing": {
                "description": "You are in a small clearing in a well marked forest path that extends to the east and west.",
                "exits": {"west": "forest", "east": "canyon_view"},
                "objects": []
            },
            "canyon_view": {
                "description": "You are at the top of the Great Canyon on its west wall. From here there is a marvelous view of the canyon and parts of the Frigid River upstream. Across the canyon, the walls of the White Cliffs join the mighty ramparts of the Flathead Mountains to the east.",
                "exits": {"west": "clearing", "down": "rocky_ledge"},
                "objects": []
            },
            "rocky_ledge": {
                "description": "You are on a ledge in the middle of the Great Canyon. From here there is a spectacular view of the canyon and the Frigid River below. The canyon wall is too steep to climb, but a chimney leads upward.",
                "exits": {"up": "canyon_view"},
                "objects": ["nest"]
            },
            "stream": {
                "description": "You are in a small chamber filled with water. The only exit is to the west.",
                "exits": {"west": "reservoir"},
                "objects": ["water"]
            }
        }
        
        # Special location properties
        self.dark_locations = {"cellar"}
        self.grue_warning_given = False

    def reset(self) -> Dict[str, Any]:
        """
        Reset the game environment to its initial state.

        Returns:
            Dict containing the initial observation and game info
        """
        self.__init__()
        self.moves = 0
        self.score = 0
        self.game_over = False
        
        return {
            "observation": self._get_location_description(),
            "score": self.score,
            "done": self.game_over,
            "moves": self.moves,
            "valid_actions": self.get_valid_actions(),
            "inventory": self.get_inventory(),
            "location": self.current_location
        }

    def step(self, action: str) -> Dict[str, Any]:
        """
        Take a step in the game by executing the given action.

        Args:
            action: Text command to execute in the game

        Returns:
            Dict containing the observation, score, done flag, and additional info
        """
        self.moves += 1
        
        # Check for maximum moves
        if self.moves >= self.max_moves:
            self.game_over = True
            return {
                "observation": "You have exceeded the maximum number of moves.",
                "score": self.score,
                "done": self.game_over,
                "moves": self.moves,
                "valid_actions": [],
                "inventory": self.get_inventory(),
                "location": self.current_location
            }
        
        # Process the action
        result = self._process_action(action.lower())
        
        # Check for death by grue in dark locations
        if self.current_location in self.dark_locations and not self._has_light():
            if not self.grue_warning_given and "grue" not in result:
                self.grue_warning_given = True
                result = "It is pitch black. You are likely to be eaten by a grue.\n\n" + result
            elif self.grue_warning_given and self.moves % 3 == 0:
                self.game_over = True
                result = "Oh, no! You have walked into the slavering fangs of a lurking grue!\n\n***** You have died *****"
        
        return {
            "observation": result,
            "score": self.score,
            "done": self.game_over,
            "moves": self.moves,
            "valid_actions": self.get_valid_actions(),
            "inventory": self.get_inventory(),
            "location": self.current_location
        }

    def get_valid_actions(self) -> List[str]:
        """
        Get a list of valid actions in the current game state.

        Returns:
            List of valid action strings
        """
        valid_actions = []
        
        # Add movement actions
        location = self.locations[self.current_location]
        for direction, destination in location["exits"].items():
            if destination:
                if direction == "window":
                    valid_actions.append(f"enter window")
                    valid_actions.append(f"go through window")
                else:
                    valid_actions.append(f"go {direction}")
                    valid_actions.append(direction)
        
        # Add object interactions for visible objects
        visible_objects = self._get_visible_objects()
        for obj in visible_objects:
            valid_actions.append(f"examine {obj}")
            valid_actions.append(f"look at {obj}")
            
            if obj not in self.inventory:
                valid_actions.append(f"take {obj}")
                valid_actions.append(f"get {obj}")
            
            if obj in self.inventory:
                valid_actions.append(f"drop {obj}")
            
            # Object-specific actions
            if obj == "mailbox":
                valid_actions.append(f"open {obj}")
                valid_actions.append(f"close {obj}")
            
            if obj == "lamp" and obj in self.inventory:
                valid_actions.append(f"turn on {obj}")
                valid_actions.append(f"turn off {obj}")
            
            if obj == "leaflet" and (obj in self.inventory or self.object_states["mailbox"]["open"] and self.object_states["leaflet"]["location"] == "in_mailbox"):
                valid_actions.append(f"read {obj}")
            
            if obj == "rug":
                valid_actions.append(f"move {obj}")
                valid_actions.append(f"lift {obj}")
        
        # Add general actions
        valid_actions.extend([
            "look", "inventory", "i", "help", "score"
        ])
        
        return valid_actions

    def get_inventory(self) -> str:
        """
        Get the current inventory.

        Returns:
            String describing the current inventory
        """
        if not self.inventory:
            return "You are not carrying anything."
        
        inventory_text = "You are carrying:\n"
        for item in self.inventory:
            if item == "lamp":
                status = " (providing light)" if self.object_states["lamp"]["on"] else " (turned off)"
                inventory_text += f"  A brass lamp{status}\n"
            elif item == "sword":
                inventory_text += "  A sword of Elvish workmanship\n"
            elif item == "leaflet":
                inventory_text += "  A small leaflet\n"
            elif item == "egg":
                inventory_text += "  A jewel-encrusted egg\n"
            else:
                inventory_text += f"  {item}\n"
        
        return inventory_text.strip()

    def _get_location_description(self) -> str:
        """
        Get the description of the current location.

        Returns:
            String describing the current location
        """
        if self.current_location in self.dark_locations and not self._has_light():
            return "It is pitch black."
        
        location = self.locations[self.current_location]
        description = location["description"]
        
        # Add visible objects
        visible_objects = []
        for obj in location["objects"]:
            if self.object_states.get(obj, {}).get("location", "") == self.current_location:
                if obj == "mailbox":
                    status = "open" if self.object_states["mailbox"]["open"] else "closed"
                    visible_objects.append(f"There is a {status} mailbox here.")
                    
                    # If mailbox is open and contains leaflet
                    if self.object_states["mailbox"]["open"] and self.object_states["leaflet"]["location"] == "in_mailbox":
                        visible_objects.append("There is a small leaflet in the mailbox.")
                elif obj == "lamp":
                    status = "lit" if self.object_states["lamp"]["on"] else "turned off"
                    visible_objects.append(f"There is a brass lamp here ({status}).")
                elif obj == "sword":
                    visible_objects.append("There is a sword of Elvish workmanship here.")
                elif obj == "trophy_case":
                    visible_objects.append("There is a trophy case here.")
                elif obj == "rug":
                    status = "moved aside" if self.object_states.get("rug", {}).get("moved", False) else "lying in the center of the room"
                    visible_objects.append(f"There is a large oriental rug {status}.")
                else:
                    visible_objects.append(f"There is a {obj} here.")
        
        if visible_objects:
            description += "\n\n" + "\n".join(visible_objects)
        
        return description

    def _get_visible_objects(self) -> List[str]:
        """
        Get a list of visible objects in the current location.

        Returns:
            List of visible object names
        """
        if self.current_location in self.dark_locations and not self._has_light():
            return []
        
        visible_objects = []
        
        # Add objects in the current location
        for obj in self.locations[self.current_location]["objects"]:
            if self.object_states.get(obj, {}).get("location", "") == self.current_location:
                visible_objects.append(obj)
        
        # Add objects in open containers in the current location
        if "mailbox" in visible_objects and self.object_states["mailbox"]["open"] and self.object_states["leaflet"]["location"] == "in_mailbox":
            visible_objects.append("leaflet")
        
        return visible_objects

    def _has_light(self) -> bool:
        """
        Check if the player has a light source.

        Returns:
            True if the player has a light source, False otherwise
        """
        return "lamp" in self.inventory and self.object_states["lamp"]["on"]

    def _process_action(self, action: str) -> str:
        """
        Process the given action and update the game state.

        Args:
            action: Text command to execute

        Returns:
            String describing the result of the action
        """
        # Split the action into words
        words = action.lower().split()
        if not words:
            return "I don't understand that."
        
        # Extract the verb and object
        verb = words[0]
        obj = words[-1] if len(words) > 1 else ""
        
        # Handle moving the rug (special case)
        if (verb == "move" or verb == "lift") and obj == "rug":
            return self._handle_move_rug()
            
        # Handle movement
        elif verb in ["go", "walk", "north", "south", "east", "west", "up", "down", "enter"] or verb in self.locations[self.current_location]["exits"]:
            return self._handle_movement(action)
        
        # Handle looking
        elif verb in ["look", "l"] and len(words) == 1:
            return self._get_location_description()
        
        # Handle examining objects
        elif verb in ["examine", "look"] and obj and obj != "at":
            return self._handle_examine(obj)
        
        # Handle inventory
        elif verb in ["inventory", "i"]:
            return self.get_inventory()
        
        # Handle taking objects
        elif verb in ["take", "get", "pick"]:
            return self._handle_take(obj)
        
        # Handle dropping objects
        elif verb in ["drop", "put"]:
            return self._handle_drop(obj)
        
        # Handle opening objects
        elif verb == "open":
            return self._handle_open(obj)
        
        # Handle closing objects
        elif verb == "close":
            return self._handle_close(obj)
        
        # Handle turning on/off the lamp
        elif verb == "turn" and len(words) > 1:
            if words[1] == "on" and obj == "lamp":
                return self._handle_turn_on_lamp()
            elif words[1] == "off" and obj == "lamp":
                return self._handle_turn_off_lamp()
        
        # Handle reading
        elif verb == "read":
            return self._handle_read(obj)
        
        # Handle moving the rug
        elif (verb == "move" or verb == "lift") and obj == "rug":
            return self._handle_move_rug()
        
        # Handle score
        elif verb == "score":
            return f"Your score is {self.score} (in {self.moves} moves)."
        
        # Handle help
        elif verb == "help":
            return (
                "Some useful commands:\n"
                "- Movement: north, south, east, west, up, down\n"
                "- Actions: look, examine [object], take [object], drop [object]\n"
                "- Inventory: inventory or i\n"
                "- Object interaction: open [object], close [object], read [object]\n"
                "- Lamp: turn on lamp, turn off lamp\n"
                "- Other: score, help"
            )
        
        return "I don't understand that command."

    def _handle_movement(self, action: str) -> str:
        """
        Handle movement actions.

        Args:
            action: Movement command

        Returns:
            String describing the result of the movement
        """
        # Extract the direction
        words = action.lower().split()
        direction = words[0]
        
        # If the command is "go direction" or similar, use the last word
        if direction in ["go", "move", "walk", "enter"]:
            if len(words) > 1:
                direction = words[-1]
            else:
                return "Go where?"
        
        # Handle "enter window" or "go through window"
        if ("enter" in words or "through" in words) and "window" in words:
            direction = "window"
        
        # Check if the direction is valid
        exits = self.locations[self.current_location]["exits"]
        if direction not in exits:
            return f"You can't go that way."
        
        # Check if the exit is blocked
        destination = exits[direction]
        if destination is None:
            if direction == "west" and self.current_location == "living_room":
                return "The door is nailed shut."
            elif direction == "down" and self.current_location == "living_room":
                return "You can't go that way."
            return "You can't go that way."
        
        # Move to the new location
        self.current_location = destination
        
        # Return the description of the new location
        return self._get_location_description()

    def _handle_examine(self, obj: str) -> str:
        """
        Handle examining objects.

        Args:
            obj: Object to examine

        Returns:
            String describing the object
        """
        # Check if the object is visible
        visible_objects = self._get_visible_objects()
        if obj not in visible_objects and obj not in self.inventory:
            return f"You don't see that here."
        
        # Return the description of the object
        if obj == "mailbox":
            status = "open" if self.object_states["mailbox"]["open"] else "closed"
            description = f"It's a small {status} mailbox."
            if self.object_states["mailbox"]["open"] and self.object_states["leaflet"]["location"] == "in_mailbox":
                description += " There is a small leaflet inside."
            return description
        elif obj == "leaflet":
            return "A small leaflet. It appears to contain instructions."
        elif obj == "lamp":
            status = "on" if self.object_states["lamp"]["on"] else "off"
            return f"It's a brass lamp. It is currently {status}."
        elif obj == "sword":
            return "The sword is made of Elvish workmanship with strange runes on the blade."
        elif obj == "trophy_case":
            return "The trophy case is empty and waiting for treasures."
        elif obj == "rug":
            status = "moved aside, revealing a trapdoor" if self.object_states.get("rug", {}).get("moved", False) else "lying in the center of the room"
            return f"It's a large oriental rug, {status}."
        elif obj == "egg":
            return "The egg is covered with fine gold inlay, and is extremely valuable."
        elif obj == "water":
            return "The water is clear and refreshing."
        else:
            return f"You see nothing special about the {obj}."

    def _handle_take(self, obj: str) -> str:
        """
        Handle taking objects.

        Args:
            obj: Object to take

        Returns:
            String describing the result of taking the object
        """
        # Check if the object is visible
        visible_objects = self._get_visible_objects()
        if obj not in visible_objects:
            return f"You don't see that here."
        
        # Check if the object is already in inventory
        if obj in self.inventory:
            return f"You're already carrying that."
        
        # Check if the object can be taken
        if obj in ["mailbox", "trophy_case", "rug"]:
            return f"You can't take that."
        
        # Check if the object is in a container
        if obj == "leaflet" and self.object_states["leaflet"]["location"] == "in_mailbox":
            if not self.object_states["mailbox"]["open"]:
                return "The mailbox is closed."
        
        # Take the object
        if obj == "leaflet":
            self.object_states["leaflet"]["location"] = "inventory"
        elif obj == "lamp":
            self.object_states["lamp"]["location"] = "inventory"
        elif obj == "sword":
            self.object_states["sword"]["location"] = "inventory"
        elif obj == "egg":
            self.object_states["egg"]["location"] = "inventory"
            self.score += 5  # Award points for finding a treasure
        elif obj == "water":
            return "The water slips through your fingers."
        else:
            return f"You can't take that."
        
        self.inventory.append(obj)
        return f"Taken."

    def _handle_drop(self, obj: str) -> str:
        """
        Handle dropping objects.

        Args:
            obj: Object to drop

        Returns:
            String describing the result of dropping the object
        """
        # Check if the object is in inventory
        if obj not in self.inventory:
            return f"You're not carrying that."
        
        # Drop the object
        self.inventory.remove(obj)
        
        if obj == "leaflet":
            self.object_states["leaflet"]["location"] = self.current_location
        elif obj == "lamp":
            self.object_states["lamp"]["location"] = self.current_location
        elif obj == "sword":
            self.object_states["sword"]["location"] = self.current_location
        elif obj == "egg":
            self.object_states["egg"]["location"] = self.current_location
        
        return f"Dropped."

    def _handle_open(self, obj: str) -> str:
        """
        Handle opening objects.

        Args:
            obj: Object to open

        Returns:
            String describing the result of opening the object
        """
        # Check if the object is visible
        visible_objects = self._get_visible_objects()
        if obj not in visible_objects and obj not in self.inventory:
            return f"You don't see that here."
        
        # Handle specific objects
        if obj == "mailbox":
            if self.object_states["mailbox"]["open"]:
                return "It's already open."
            
            self.object_states["mailbox"]["open"] = True
            
            if self.object_states["leaflet"]["location"] == "in_mailbox":
                return "Opening the mailbox reveals a small leaflet."
            return "Opened."
        elif obj == "trophy_case":
            return "The trophy case is already open."
        else:
            return f"You can't open that."

    def _handle_close(self, obj: str) -> str:
        """
        Handle closing objects.

        Args:
            obj: Object to close

        Returns:
            String describing the result of closing the object
        """
        # Check if the object is visible
        visible_objects = self._get_visible_objects()
        if obj not in visible_objects and obj not in self.inventory:
            return f"You don't see that here."
        
        # Handle specific objects
        if obj == "mailbox":
            if not self.object_states["mailbox"]["open"]:
                return "It's already closed."
            
            self.object_states["mailbox"]["open"] = False
            return "Closed."
        else:
            return f"You can't close that."

    def _handle_turn_on_lamp(self) -> str:
        """
        Handle turning on the lamp.

        Returns:
            String describing the result of turning on the lamp
        """
        # Check if the lamp is in inventory
        if "lamp" not in self.inventory:
            return "You're not carrying that."
        
        # Check if the lamp is already on
        if self.object_states["lamp"]["on"]:
            return "The lamp is already on."
        
        # Turn on the lamp
        self.object_states["lamp"]["on"] = True
        return "The lamp is now on and providing light."

    def _handle_turn_off_lamp(self) -> str:
        """
        Handle turning off the lamp.

        Returns:
            String describing the result of turning off the lamp
        """
        # Check if the lamp is in inventory
        if "lamp" not in self.inventory:
            return "You're not carrying that."
        
        # Check if the lamp is already off
        if not self.object_states["lamp"]["on"]:
            return "The lamp is already off."
        
        # Turn off the lamp
        self.object_states["lamp"]["on"] = False
        
        # Check if in a dark location
        if self.current_location in self.dark_locations:
            return "The lamp is now off. It is pitch black."
        
        return "The lamp is now off."

    def _handle_read(self, obj: str) -> str:
        """
        Handle reading objects.

        Args:
            obj: Object to read

        Returns:
            String describing the result of reading the object
        """
        # Check if the object is visible or in inventory
        visible_objects = self._get_visible_objects()
        if obj not in visible_objects and obj not in self.inventory:
            return f"You don't see that here."
        
        # Handle specific objects
        if obj == "leaflet":
            if not self.object_states["leaflet"]["read"]:
                self.object_states["leaflet"]["read"] = True
                self.score += 1  # Award a point for reading the leaflet
            
            return (
                "WELCOME TO ZORK!\n\n"
                "ZORK is a game of adventure, danger, and low cunning. "
                "In it you will explore some of the most amazing territory ever seen by mortals. "
                "No computer should be without one!"
            )
        else:
            return f"There's nothing written on the {obj}."

    def _handle_move_rug(self) -> str:
        """
        Handle moving the rug.

        Returns:
            String describing the result of moving the rug
        """
        # Check if the rug is visible
        visible_objects = self._get_visible_objects()
        if "rug" not in visible_objects:
            return "You don't see that here."
        
        # Check if the rug is already moved
        if self.object_states.get("rug", {}).get("moved", False):
            return "The rug has already been moved aside."
        
        # Move the rug
        self.object_states["rug"] = {"moved": True, "location": "living_room"}
        self.score += 2  # Award points for discovering the trapdoor
        
        # Update the exits
        self.locations["living_room"]["exits"]["down"] = "cellar"
        
        return "You move the rug aside, revealing a closed trapdoor in the floor."
