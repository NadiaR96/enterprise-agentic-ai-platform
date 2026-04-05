import pytest
from unittest.mock import patch, MagicMock

class TestPlannerAgent:
    """Test cases for the planner agent."""

    @patch('agents.planner_agent.ChatOpenAI')
    def test_planner_agent_basic_query(self, mock_chat_class):
        """Test planner agent with a basic query."""
        # Mock the ChatOpenAI instance
        mock_instance = MagicMock()
        mock_chat_class.return_value = mock_instance

        # Mock the chain invoke
        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = "qa"

            from agents.planner_agent import planner_agent
            result = planner_agent("What is AI?")

            assert result == "qa"
            mock_invoke.assert_called_once()

    def test_planner_agent_error_handling(self):
        """Test planner agent error handling."""
        with patch('agents.planner_agent.ChatOpenAI') as mock_chat_class:
            mock_instance = MagicMock()
            mock_chat_class.return_value = mock_instance

            with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
                mock_invoke.side_effect = Exception("API Error")

                from agents.planner_agent import planner_agent
                with pytest.raises(Exception):
                    planner_agent("Test query")

    @patch('agents.planner_agent.ChatOpenAI')
    def test_planner_agent_complex_query(self, mock_chat_class):
        """Test planner agent with a complex query requiring multiple agents."""
        mock_instance = MagicMock()
        mock_chat_class.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = "summary"

            from agents.planner_agent import planner_agent
            result = planner_agent("Summarize this long document about machine learning")

            assert result == "summary"

    @patch('agents.planner_agent.ChatOpenAI')
    def test_planner_agent_input_validation(self, mock_chat_class):
        """Test planner agent input validation."""
        mock_instance = MagicMock()
        mock_chat_class.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = "qa"

            from agents.planner_agent import planner_agent
            result = planner_agent("")

            assert result == "qa"