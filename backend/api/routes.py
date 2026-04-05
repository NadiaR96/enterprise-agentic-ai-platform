from fastapi import APIRouter
from pydantic import BaseModel

try:
    from backend.services.orchestrator import route_query
    from backend.database import save_conversation, get_user_history, get_all_users
except ModuleNotFoundError:
    from services.orchestrator import route_query
    from database import save_conversation, get_user_history, get_all_users

router = APIRouter()

class QueryRequest(BaseModel):
    query: str
    user_id: str = "default"

@router.post("/query")
def query_endpoint(request: QueryRequest):
    response = route_query(request.query)
    # Save to database
    save_conversation(request.user_id, request.query, response)
    return response

@router.get("/history/{user_id}")
def get_history(user_id: str):
    """Get conversation history for a user."""
    history = get_user_history(user_id)
    return {"user_id": user_id, "history": history}

@router.get("/users")
def list_users():
    """Get list of all users who have interacted with the system."""
    users = get_all_users()
    return {"users": users}
