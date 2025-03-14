"""
Unit tests for the MCP agent.
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the src directory to the path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Import the agent modules
from src.agent.mcp.agent import run_agent, generate_thought, select_action


class TestMcpAgent(unittest.TestCase):
    """Test cases for the MCP agent."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock environment
        self.mock_env = MagicMock()
        self.mock_env.reset.return_value = {
            "observation": "You are in a test room.",
            "valid_actions": ["look", "go north", "examine test"],
            "inventory": "You are not carrying anything.",
            "location": "test_room",
            "score": 0,
            "moves": 0,
            "done": False
        }
        self.mock_env.step.return_value = {
            "observation": "You examined the test object.",
            "valid_actions": ["look", "go north", "take test"],
            "inventory": "You are not carrying anything.",
            "location": "test_room",
            "score": 1,
            "moves": 1,
            "done": False
        }

        # Create a mock LLM
        self.mock_client = MagicMock()
        self.mock_response = MagicMock()
        self.mock_response.choices = [MagicMock()]
        self.mock_response.choices[0].message = MagicMock()
        self.mock_response.choices[0].message.content = "examine test"
        self.mock_client.chat.completions.create.return_value = self.mock_response

    @patch('src.agent.mcp.agent.create_environment')
    @patch('src.agent.mcp.agent.OpenAI')
    def test_run_agent(self, mock_openai, mock_create_environment):
        """Test running the agent."""
        # Set up the mocks
        mock_openai.return_value = self.mock_client
        mock_create_environment.return_value = self.mock_env

        # Run the agent with a max of 1 step
        with patch('builtins.print'):  # Suppress print output
            with patch('time.sleep'):  # Skip sleep delay
                run_agent(max_steps=1)

        # Assert that the environment was reset
        self.mock_env.reset.assert_called_once()
        
        # Assert that the environment step was called
        self.mock_env.step.assert_called_once()
        
        # Assert that the LLM was called twice (once for thought, once for action)
        self.assertEqual(self.mock_client.chat.completions.create.call_count, 2)

    def test_generate_thought(self):
        """Test generating a thought."""
        game_state = {
            "observation": "You are in a test room.",
            "location": "test_room",
            "inventory": "You are not carrying anything.",
            "score": 0,
            "moves": 0
        }
        
        # Generate a thought
        thought = generate_thought(self.mock_client, "test-model", game_state)
        
        # Assert that the LLM was called
        self.mock_client.chat.completions.create.assert_called_once()
        
        # Assert that the thought is the expected value
        self.assertEqual(thought, "examine test")

    def test_select_action(self):
        """Test selecting an action."""
        game_state = {
            "observation": "You are in a test room.",
            "location": "test_room",
            "inventory": "You are not carrying anything.",
            "score": 0,
            "moves": 0
        }
        thought = "I should examine the test object."
        
        # Select an action
        action = select_action(self.mock_client, "test-model", game_state, thought)
        
        # Assert that the LLM was called
        self.mock_client.chat.completions.create.assert_called_once()
        
        # Assert that the action is the expected value
        self.assertEqual(action, "examine test")


if __name__ == '__main__':
    unittest.main()
