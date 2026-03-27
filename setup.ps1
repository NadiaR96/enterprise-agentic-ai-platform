# setup.ps1
# One-command setup for Enterprise Agentic AI Platform (Windows)

# ---- Activate or create venv ----
if (Test-Path ".venv") {
    Write-Host "Deleting old .venv..."
    Remove-Item -Recurse -Force .venv
}

Write-Host "Creating new virtual environment..."
python -m venv .venv
.venv\Scripts\activate

# ---- Upgrade pip, setuptools, wheel ----
Write-Host "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# ---- Install backend dependencies ----
Write-Host "Installing backend dependencies..."
pip install fastapi uvicorn
pip install langchain langchain-community langchain-openai
pip install faiss-cpu
pip install tiktoken pypdf python-docx

# ---- Install frontend dependencies ----
Write-Host "Installing frontend dependencies..."
cd frontend
if (Test-Path "node_modules") {
    Write-Host "Removing old node_modules..."
    Remove-Item -Recurse -Force node_modules
}
npm install

Write-Host "`nSetup complete! You can now run the backend and frontend:"
Write-Host "Backend: cd ..\backend ; uvicorn main:app --reload"
Write-Host "Frontend: npm start (inside frontend folder)"