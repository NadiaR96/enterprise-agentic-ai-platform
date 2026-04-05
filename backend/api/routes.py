from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

try:
    from backend.services.orchestrator import route_query
    from backend.database import save_conversation, get_user_history, get_all_users
    from backend.auth.security import get_current_active_user, require_role, User
except ModuleNotFoundError:
    from services.orchestrator import route_query
    from database import save_conversation, get_user_history, get_all_users
    from auth.security import get_current_active_user, require_role, User

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_endpoint(
    request: QueryRequest,
    current_user: User = Depends(get_current_active_user)
):
    """Process a query with authentication."""
    try:
        response = route_query(request.query)
        # Save to database with authenticated user
        save_conversation(current_user.user_id, request.query, response)
        return {
            "response": response,
            "user_id": current_user.user_id,
            "timestamp": response.get("timestamp")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@router.get("/history")
def get_history(current_user: User = Depends(get_current_active_user)):
    """Get conversation history for the authenticated user."""
    history = get_user_history(current_user.user_id)
    return {"user_id": current_user.user_id, "history": history}

@router.get("/users")
def list_users(current_user: User = Depends(require_role("admin"))):
    """Get list of all users (admin only)."""
    users = get_all_users()
    return {"users": users}

@router.get("/admin/metrics")
def get_admin_metrics(current_user: User = Depends(require_role("admin"))):
    """Get system metrics (admin only)."""
    # This would integrate with your monitoring/metrics.py
    try:
        from backend.monitoring.metrics import get_system_metrics
        metrics = get_system_metrics()
        return metrics
    except ImportError:
        return {"message": "Metrics not available", "status": "demo"}
