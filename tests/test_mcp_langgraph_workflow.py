"""
Unit tests for the MCP LangGraph workflow.
"""
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the src directory to the path
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

# Import the workflow modules
from src.agent.mcp_langgraph.workflow import (  # noqa: E402
    create_agent_workflow, run_agent_workflow)


class TestMcpLangGraphWorkflow(unittest.TestCase):
    """Test cases for the MCP LangGraph workflow."""

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
        self.mock_llm = MagicMock()
        self.mock_llm.invoke.side_effect = [
            MagicMock(
                content="I should examine the test object to learn more about it."),
            MagicMock(
                content='{"tool": "examine", "args": {"object": "test"}}')
        ]

    @patch('src.agent.mcp_langgraph.workflow.ChatOpenAI')
    def test_create_workflow(self, mock_chat_openai):
        """Test creating the workflow."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Create the workflow
        workflow, initial_state = create_agent_workflow(
            environment=self.mock_env,
            model_name="test-model",
            api_key="test-key",
            max_steps=1
        )

        # Assert that the workflow was created
        self.assertIsNotNone(workflow)
        
        # Assert that the ChatOpenAI was called with the correct arguments
        mock_chat_openai.assert_called_once_with(model="test-model", api_key="test-key")
        
        # Assert that the initial state has the expected structure
        self.assertIsNone(initial_state["observation"])
        self.assertEqual(initial_state["thought"], "")
        self.assertEqual(initial_state["action"], "")
        self.assertEqual(initial_state["score"], 0)
        self.assertEqual(initial_state["moves"], 0)
        self.assertEqual(initial_state["done"], False)
        self.assertEqual(initial_state["inventory"], [])
        self.assertEqual(initial_state["location"], "")
        self.assertEqual(initial_state["valid_actions"], [])
        self.assertIsNone(initial_state["tool_name"])
        self.assertIsNone(initial_state["tool_args"])
        self.assertIsNone(initial_state["tool_result"])

    @patch('src.agent.mcp_langgraph.workflow.ChatOpenAI')
    def test_observe_node(self, mock_chat_openai):
        """Test the observe node."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Create the workflow
        workflow, initial_state = create_agent_workflow(
            environment=self.mock_env,
            model_name="test-model",
            api_key="test-key",
            max_steps=1
        )
        
        # Run the workflow for one step
        result = workflow.invoke(initial_state)
        
        # Assert that the result has the expected structure
        self.assertIsNotNone(result.get("observation"))
        self.assertIsNotNone(result.get("thought"))
        self.assertIsNotNone(result.get("action"))
        self.assertIsNotNone(result.get("tool_name"))
        self.assertIsNotNone(result.get("tool_args"))
        
        # Assert that the LLM was called twice (once for thought, once for tool selection)
        self.assertEqual(self.mock_llm.invoke.call_count, 2)

    @patch('src.agent.mcp_langgraph.workflow.ChatOpenAI')
    def test_run_workflow(self, mock_chat_openai):
        """Test running the workflow."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Mock the environment step method to return a test result
        self.mock_env.step.return_value = {
            "observation": "You examined the test object.",
            "valid_actions": ["look", "go north", "take test"],
            "inventory": "You are not carrying anything.",
            "location": "test_room",
            "score": 1,
            "moves": 1,
            "done": False
        }
        
        # Run the workflow
        run_agent_workflow(
            environment=self.mock_env,
            model_name="test-model",
            api_key="test-key",
            max_steps=1
        )
        
        # Assert that the environment was reset
        self.mock_env.reset.assert_called_once()
        
        # Assert that the environment step was called at least once
        self.mock_env.step.assert_called()


if __name__ == '__main__':
    unittest.main()
