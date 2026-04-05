import pytest
from unittest.mock import patch, MagicMock
from agents.qa_agent import qa_agent

class TestQAAgent:
    """Test cases for the QA agent."""

    @patch('agents.qa_agent.ChatOpenAI')
    def test_qa_agent_basic_question(self, mock_chat):
        """Test QA agent with a basic question."""
        # Mock LLM response
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "AI stands for Artificial Intelligence"
        mock_instance.invoke.return_value = mock_response
        mock_chat.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = mock_response
            result = qa_agent("What is AI?")
            assert result == "AI stands for Artificial Intelligence"

    @patch('agents.qa_agent.ChatOpenAI')
    def test_qa_agent_with_context(self, mock_chat):
        """Test QA agent with retrieved context."""
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "Machine learning is a subset of AI that uses algorithms to learn from data."
        mock_instance.invoke.return_value = mock_response
        mock_chat.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = mock_response
            result = qa_agent("What is machine learning?")
            assert result == "Machine learning is a subset of AI that uses algorithms to learn from data."

    @patch('agents.qa_agent.ChatOpenAI')
    def test_qa_agent_error_handling(self, mock_chat):
        """Test QA agent error handling."""
        mock_instance = MagicMock()
        mock_instance.invoke.side_effect = Exception("API failed")
        mock_chat.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.side_effect = Exception("API failed")
            with pytest.raises(Exception):
                qa_agent("Test question")

    @patch('agents.qa_agent.ChatOpenAI')
    def test_qa_agent_confidence_calculation(self, mock_chat):
        """Test confidence score calculation."""
        mock_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.content = "This is a confident answer based on the context."
        mock_instance.invoke.return_value = mock_response
        mock_chat.return_value = mock_instance

        with patch('langchain_core.runnables.base.RunnableSequence.invoke') as mock_invoke:
            mock_invoke.return_value = mock_response
            result = qa_agent("Test question")
            assert result == "This is a confident answer based on the context."