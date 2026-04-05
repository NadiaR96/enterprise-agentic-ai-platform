import pytest
from unittest.mock import patch, MagicMock
from services.orchestrator import route_query

class TestOrchestrator:
    """Test cases for the query orchestrator."""

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.qa_agent')
    @patch('services.orchestrator.evaluator_agent')
    def test_route_query_qa_flow(self, mock_evaluator, mock_qa, mock_planner):
        """Test routing to QA agent."""
        mock_planner.return_value = "qa"
        mock_qa.return_value = "Test answer"
        mock_evaluator.return_value = 0.9

        result = route_query("What is AI?")

        assert result["answer"] == "Test answer"
        assert result["confidence"] == 0.9
        assert result["grounded"] == True
        mock_planner.assert_called_once_with("What is AI?")
        mock_qa.assert_called_once_with("What is AI?")
        mock_evaluator.assert_called_once()

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.summary_agent')
    def test_route_query_summary_flow(self, mock_summary, mock_planner):
        """Test routing to summary agent."""
        mock_planner.return_value = "summary"
        mock_summary.return_value = "Test summary"

        result = route_query("Summarize this document")

        assert result["answer"] == "Test summary"
        assert result["confidence"] == 1.0
        assert result["grounded"] == True
        mock_planner.assert_called_once()
        mock_summary.assert_called_once()

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.qa_agent')
    @patch('services.orchestrator.evaluator_agent')
    def test_route_query_evaluation_flow(self, mock_evaluator, mock_qa, mock_planner):
        """Test routing to evaluator agent."""
        mock_planner.return_value = "evaluator"
        mock_qa.return_value = "Test answer"
        mock_evaluator.return_value = 0.85

        result = route_query("Evaluate this answer")

        assert result["confidence"] == 0.85
        assert result["answer"] == "Test answer"
        assert result["grounded"] == True  # 0.85 >= 0.7 threshold
        mock_planner.assert_called_once()
        mock_qa.assert_called_once()
        mock_evaluator.assert_called_once()

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.qa_agent')
    @patch('services.orchestrator.evaluator_agent')
    def test_route_query_unknown_agent(self, mock_evaluator, mock_qa, mock_planner):
        """Test handling of unknown agent type."""
        mock_planner.return_value = "unknown_agent"
        mock_qa.return_value = "Test answer"
        mock_evaluator.return_value = 0.8

        result = route_query("Test query")
        
        # Should default to QA flow for unknown agents
        assert result["answer"] == "Test answer"
        assert result["confidence"] == 0.8

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.qa_agent')
    @patch('services.orchestrator.evaluator_agent')
    def test_route_query_empty_input(self, mock_evaluator, mock_qa, mock_planner):
        """Test routing with empty input."""
        mock_planner.return_value = "qa"
        mock_qa.return_value = "Empty response"
        mock_evaluator.return_value = 0.0

        result = route_query("")
        assert result["answer"] == "Empty response"
        assert result["confidence"] == 0.0

    @patch('services.orchestrator.planner_agent')
    @patch('services.orchestrator.qa_agent')
    def test_route_query_error_handling(self, mock_qa, mock_planner):
        """Test error handling in orchestrator."""
        mock_planner.return_value = "qa"
        mock_qa.side_effect = Exception("Agent failed")

        with pytest.raises(Exception):
            route_query("Test query")