"""
Unit tests for the LangGraph workflow.
"""
import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Add the src directory to the path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agent.implicit.workflow import create_agent_workflow, AgentState, run_agent_workflow


class TestWorkflow(unittest.TestCase):
    """Test cases for the LangGraph workflow."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock environment
        self.mock_env = MagicMock()
        self.mock_env.reset.return_value = {
            "observation": "You are in a test room.",
            "valid_actions": ["look", "go north", "examine test"],
            "inventory": [],
            "location": "test_room",
            "score": 0,
            "moves": 0,
            "done": False
        }
        self.mock_env.step.return_value = {
            "observation": "You examined the test object.",
            "valid_actions": ["look", "go north", "take test"],
            "inventory": [],
            "location": "test_room",
            "score": 1,
            "moves": 1,
            "done": False
        }

        # Create a mock LLM
        self.mock_llm = MagicMock()
        self.mock_llm.invoke.side_effect = [
            MagicMock(content="I should examine the test object to learn more about it."),
            MagicMock(content="examine test")
        ]

    @patch('src.agent.implicit.workflow.ChatOpenAI')
    def test_create_workflow(self, mock_chat_openai):
        """Test creating the workflow."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Create the workflow
        workflow = create_agent_workflow()

        # Assert that the workflow was created
        self.assertIsNotNone(workflow)
        
        # Assert that the ChatOpenAI was called with the correct arguments
        mock_chat_openai.assert_called_once()
        
        # Compile the workflow to ensure it's valid
        app = workflow.compile()
        self.assertIsNotNone(app)

    @patch('src.agent.implicit.workflow.ChatOpenAI')
    def test_observe_node(self, mock_chat_openai):
        """Test the observe node."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Create the workflow
        workflow = create_agent_workflow()
        
        # Create a test state
        state = AgentState(
            observation="You are in a test room.",
            valid_actions=["look", "go north", "examine test"],
            inventory=[],
            location="test_room",
            thought=None,
            action=None,
            history=[],
            score=0,
            moves=0,
            done=False
        )
        
        # Compile the workflow
        app = workflow.compile()
        
        # Run the workflow
        result = app.invoke(state)
        
        # Assert that the result has a thought and action
        self.assertIsNotNone(result.get("thought"))
        self.assertIsNotNone(result.get("action"))
        
        # Assert that the LLM was called twice (once for thought, once for action)
        self.assertEqual(self.mock_llm.invoke.call_count, 2)

    @patch('src.agent.implicit.workflow.ChatOpenAI')
    def test_run_workflow(self, mock_chat_openai):
        """Test running the workflow."""
        # Set up the mock
        mock_chat_openai.return_value = self.mock_llm

        # Run the workflow
        result = run_agent_workflow(
            environment=self.mock_env,
            model_name="test-model",
            api_key="test-key",
            max_steps=1
        )
        
        # Assert that the environment was reset
        self.mock_env.reset.assert_called_once()
        
        # Assert that the environment step was called with the correct action
        self.mock_env.step.assert_called_once_with("examine test")
        
        # Assert that the result has the correct values
        self.assertEqual(result["location"], "test_room")
        self.assertEqual(result["score"], 1)
        self.assertEqual(result["moves"], 1)
        
        # Assert that the LLM was called twice (once for thought, once for action)
        self.assertEqual(self.mock_llm.invoke.call_count, 2)


if __name__ == '__main__':
    unittest.main()
