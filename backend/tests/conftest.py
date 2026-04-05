# Backend tests configuration
import pytest
import os
import sys
from pathlib import Path

# Add backend to path for imports
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

# Set dummy API key for tests
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["JWT_SECRET_KEY"] = "test-secret"

@pytest.fixture
def sample_query():
    """Sample query for testing."""
    return "What is machine learning?"

@pytest.fixture
def sample_user():
    """Sample user data for testing."""
    return {
        "user_id": "test_user",
        "email": "test@example.com",
        "roles": ["user"]
    }

@pytest.fixture
def auth_headers():
    """Mock authorization headers for testing."""
    from auth.security import create_access_token
    token = create_access_token({"sub": "test_user", "roles": ["user"]})
    return {"Authorization": f"Bearer {token}"}