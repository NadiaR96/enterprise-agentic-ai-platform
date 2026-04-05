import pytest
import sqlite3
import os
from unittest.mock import patch, MagicMock
from database import init_db, save_conversation, get_user_history, get_all_users

class TestDatabase:
    """Test cases for database operations."""

    @pytest.fixture
    def temp_db(self, tmp_path):
        """Create a temporary database for testing."""
        db_path = tmp_path / "test.db"
        # Override the database path for testing
        with patch('database.DB_PATH', str(db_path)):
            init_db()
            yield str(db_path)
        # Cleanup
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_init_db(self, temp_db):
        """Test database initialization."""
        # Check if tables were created
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        # Check users table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None

        # Check conversations table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
        assert cursor.fetchone() is not None

        conn.close()

    @patch('database.sqlite3.connect')
    def test_save_conversation(self, mock_connect):
        """Test saving a conversation."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        result = save_conversation("user123", "Hello", {"answer": "Hi there", "confidence": 0.9})

        # save_conversation doesn't return anything, just check it doesn't raise
        assert result is None
        mock_cursor.execute.assert_called()
        mock_conn.commit.assert_called()

    @patch('database.sqlite3.connect')
    def test_get_user_history(self, mock_connect):
        """Test retrieving user conversation history."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the cursor.fetchall() to return raw database rows
        mock_cursor.fetchall.return_value = [
            ("Q1", '{"answer": "A1", "confidence": 0.8}', 0.8, "2024-01-01"),
            ("Q2", '{"answer": "A2", "confidence": 0.9}', 0.9, "2024-01-02")
        ]

        history = get_user_history("user123")

        assert len(history) == 2
        assert history[0]["query"] == "Q1"
        assert history[0]["response"]["answer"] == "A1"
        assert history[1]["query"] == "Q2"
        assert history[1]["response"]["answer"] == "A2"

    @patch('database.sqlite3.connect')
    def test_get_all_users(self, mock_connect):
        """Test retrieving all users."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock the cursor.fetchall() to return user data
        mock_cursor.fetchall.return_value = [
            ("alice", "2024-01-01"),
            ("bob", "2024-01-02")
        ]

        users = get_all_users()

        assert len(users) == 2
        assert "alice" in users
        assert "bob" in users

    @patch('database.sqlite3.connect')
    def test_save_conversation_error_handling(self, mock_connect):
        """Test error handling in save_conversation."""
        # Mock the database connection to raise an exception
        mock_connect.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            save_conversation("user123", "Hello", {"answer": "Hi there", "confidence": 0.9})

    @patch('database.sqlite3.connect')
    def test_get_user_history_empty(self, mock_connect):
        """Test getting history for user with no conversations."""
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Mock empty result
        mock_cursor.fetchall.return_value = []

        history = get_user_history("nonexistent_user")

        assert history == []