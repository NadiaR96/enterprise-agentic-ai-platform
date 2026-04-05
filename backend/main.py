# backend/main.py
import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend package imports work whether this file is run as a script or a module.
ROOT = Path(__file__).resolve().parent
ROOT_PARENT = ROOT.parent
for path in (str(ROOT), str(ROOT_PARENT)):
    if path not in sys.path:
        sys.path.insert(0, path)

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Debug: Check if OPENAI_API_KEY is loaded
print(f"OPENAI_API_KEY loaded: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")

from api.routes import router  # Make sure this imports your endpoints
from auth.routes import router as auth_router  # Authentication routes

app = FastAPI(
    title="Enterprise Agentic AI Platform",
    description="Backend API for your AI platform",
    version="1.0.0",
)

# === CORS Setup ===
# Add your frontend URLs here. For development, you can use localhost:3000
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your production frontend domain here, e.g., "https://myapp.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Handles GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# === API Routes ===
app.include_router(router, prefix="/api", tags=["API"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# === Root Endpoint (Optional) ===
@app.get("/")
async def root():
    return {"message": "Enterprise Agentic AI Platform Backend is running."}

# === Run with: uvicorn main:app --reload ===

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)