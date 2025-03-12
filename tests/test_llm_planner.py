"""
Test the LLM-based planner for the Zork AI agent.

This module tests the LLM-based planner's ability to generate actions
based on observations and memory.
"""
import unittest
from src.agent.memory import AgentMemory
from src.agent.llm_planner import LLMActionPlanner


class TestLLMPlanner(unittest.TestCase):
    """Test cases for the LLM-based planner."""

    def setUp(self):
        """Set up the test environment."""
        self.planner = LLMActionPlanner()
        self.memory = AgentMemory()

    def test_initialization(self):
        """Test that the planner initializes correctly."""
        self.assertIsNotNone(self.planner)
        self.assertEqual(self.planner.model_name, "gpt-3.5-turbo")
        self.assertEqual(len(self.planner.context_window), 0)
        self.assertEqual(self.planner.max_context_items, 10)
        self.assertIsNotNone(self.planner.system_prompt)

    def test_update_context(self):
        """Test that the context window is updated correctly."""
        observation = "You are in a forest."
        valid_actions = ["go north", "go south", "look"]
        
        # Update context
        self.planner._update_context(observation, valid_actions, self.memory)
        
        # Check that context was updated
        self.assertEqual(len(self.planner.context_window), 1)
        self.assertEqual(self.planner.context_window[0]["observation"], observation)
        self.assertEqual(self.planner.context_window[0]["valid_actions"], valid_actions)
        
        # Update context again
        new_observation = "You are in a clearing."
        new_valid_actions = ["go north", "go east", "look"]
        self.planner._update_context(new_observation, new_valid_actions, self.memory)
        
        # Check that context was updated
        self.assertEqual(len(self.planner.context_window), 2)
        self.assertEqual(self.planner.context_window[1]["observation"], new_observation)
        self.assertEqual(self.planner.context_window[1]["valid_actions"], new_valid_actions)
        
        # Test context window size limit
        for i in range(10):
            self.planner._update_context(f"Observation {i}", [], self.memory)
        
        # Check that context window size is limited
        self.assertEqual(len(self.planner.context_window), 10)
        self.assertTrue(self.planner.context_window[0]["observation"].startswith("Observation"))

    def test_create_llm_prompt(self):
        """Test that the LLM prompt is created correctly."""
        observation = "You are in a forest."
        valid_actions = ["go north", "go south", "look"]
        
        # Create prompt
        prompt = self.planner._create_llm_prompt(observation, valid_actions, self.memory)
        
        # Check that prompt contains expected elements
        self.assertIn(observation, prompt)
        for action in valid_actions:
            self.assertIn(action, prompt)
        self.assertIn("Generate the next action:", prompt)

    def test_generate_action_fallback(self):
        """Test that the planner falls back to rule-based planning when needed."""
        observation = "You are in a forest."
        valid_actions = ["go north", "go south", "look"]
        
        # Generate action
        action = self.planner.generate_action(observation, valid_actions, self.memory)
        
        # Check that action is one of the valid actions
        self.assertIn(action, valid_actions)
        
        # Check that action was added to history
        self.assertIn(action, self.planner.action_history)

    def test_validate_action(self):
        """Test that actions are validated correctly."""
        valid_actions = ["go north", "go south", "look"]
        
        # Test valid action
        is_valid, action = self.planner.validate_action("go north", valid_actions)
        self.assertTrue(is_valid)
        self.assertEqual(action, "go north")
        
        # Test invalid action
        is_valid, action = self.planner.validate_action("go west", valid_actions)
        self.assertFalse(is_valid)
        
        # Test direction without "go"
        is_valid, action = self.planner.validate_action("north", valid_actions)
        self.assertTrue(is_valid)
        self.assertEqual(action, "go north")


if __name__ == "__main__":
    unittest.main()
