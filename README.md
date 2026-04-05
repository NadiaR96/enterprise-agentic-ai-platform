# Enterprise Agentic AI Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.2.0-blue.svg)](https://reactjs.org/)

A production-ready, enterprise-grade AI orchestration platform featuring multi-agent systems, RAG pipelines, observability, and scalable architecture. Built with FastAPI, React, LangChain, and Docker.

## 🚀 Features

- **Multi-Agent Orchestration**: Modular agent system with specialized roles (QA, Summary, Planner, Evaluator)
- **Retrieval-Augmented Generation (RAG)**: Knowledge base integration with FAISS vector storage
- **Multi-User Support**: SQLite-based user management with conversation persistence
- **Observability & Metrics**: Comprehensive logging and cost tracking simulation
- **Scalable Architecture**: Containerized deployment with Docker Compose
- **Modern Frontend**: React-based chat interface with real-time interactions
- **Cost Optimization**: Intelligent caching and efficient LLM usage patterns

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────────┐    ┌─────────────┐
│   Frontend  │────│     API     │────│   Orchestrator   │────│   Agents     │
│   (React)   │    │  (FastAPI)  │    │                 │    │             │
└─────────────┘    └─────────────┘    └─────────────────┘    └─────────────┘
                                                              │
                                                              ▼
                                                       ┌─────────────┐
                                                       │     RAG     │
                                                       │  Pipeline   │
                                                       └─────────────┘
```

**Data Flow**: User Query → API → Orchestrator → Specialized Agent → RAG Retrieval → AI Response

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for containerized deployment)
- OpenAI API key

## 🛠️ Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/enterprise-agentic-ai-platform.git
   cd enterprise-agentic-ai-platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

## ⚙️ Environment Configuration

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Configure your environment variables**
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./enterprise_ai.db
   LOG_LEVEL=INFO
   ```

## 🚀 Running the Application

### Local Development

1. **Start the backend**
   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the frontend** (in a new terminal)
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📚 API Documentation

### Key Endpoints

- `POST /api/query` - Process user queries with multi-user support
- `GET /api/users` - Retrieve all users
- `GET /api/history/{user_id}` - Get conversation history for a user
- `GET /api/metrics` - View system metrics and costs

### Example API Usage

```python
import requests

response = requests.post("http://localhost:8000/api/query",
    json={"query": "What is RAG?", "user_id": "user123"})
print(response.json())
```

## 📁 Project Structure

```
enterprise-agentic-ai-platform/
├── backend/
│   ├── api/           # FastAPI routes and models
│   ├── agents/        # Specialized AI agents
│   ├── services/      # Core business logic
│   ├── data/          # Knowledge base documents
│   ├── vectorstore/   # FAISS vector indices
│   ├── database.py    # SQLite database operations
│   └── main.py        # Application entry point
├── frontend/
│   ├── src/           # React components
│   └── public/        # Static assets
├── monitoring/
│   └── metrics.py     # Observability and metrics
├── docker-compose.yml # Container orchestration
├── Dockerfile.backend # Backend container config
└── Dockerfile.frontend # Frontend container config
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is a demonstration platform. For production use, ensure proper security measures, monitoring, and compliance with your organization's policies.
