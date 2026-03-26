---
name: enterprise-agentic-ai-platform
description: "Use when: implementing features or fixes in the Enterprise Agentic AI Platform. Follow architectural patterns, maintain multi-agent design, and ensure observability across Python (FastAPI, agents, RAG) and React frontend."
applies: all-files
---

# Copilot Instructions: Enterprise Agentic AI Platform

## Project Vision
Enterprise-grade AI orchestration platform with modular agent design, RAG pipelines, observability, and cost-efficient architecture.

## Architecture Overview
```
User → API (FastAPI) → Orchestrator → Agents → RAG Pipeline → Response
```

**Key Components:**
- **Backend** (`backend/main.py`): FastAPI server routing queries, maintaining user memory
- **Orchestrator** (`orchestrator/orchestrator.py`): Routes queries to appropriate agents
- **Agents** (`agents/`): Specialized agents (QA, Summary) with focused responsibilities
- **RAG Pipelie** (`rag/pipeline.py`): Knowledge retrieval and answer synthesis
- **Monitoring** (`monitoring/metrics.py`): Metrics and cost tracking
- **Frontend** (`frontend/`): React SPA for user interaction

## Coding Conventions

### Python Style (Backend, Agents, RAG)
- **Type hints**: Use them for function parameters and return types where possible
- **Naming**: snake_case for functions/variables, UPPER_SNAKE_CASE for constants
- **Structure**: Minimal, focused modules—each file has a single responsibility
- **Imports**: Group stdlib, third-party, local imports with blank lines
- **Docstrings**: Add brief docstrings to functions explaining purpose and return value
- **Error handling**: Use proper exceptions, avoid silent failures

### JavaScript/React Style (Frontend)
- **Naming**: camelCase for variables/functions, PascalCase for components
- **Hooks**: Use functional components and React hooks (useState, useEffect)
- **State management**: Lift state to parent components; use Context API if needed
- **Styling**: Inline styles or CSS files; avoid hardcoded colors/sizes
- **Async**: Use async/await with proper error handling; avoid callback chains

## Multi-Agent Design Principles
- **Single responsibility**: Each agent has one clear purpose (e.g., QA, Summarization)
- **Modularity**: Agents are independent; composition happens in the Orchestrator
- **Observability**: Log agent calls, inputs, outputs, and execution time
- **Caching**: Minimize redundant RAG calls; cache context where appropriate
- **Scalability**: Design agents to be stateless for horizontal scaling

## Implementation Workflow

### Adding a New Feature
1. **Define the flow**: Where does input enter? Which agents touch it? What's the expected output?
2. **Update orchestrator**: Add routing logic if introducing a new agent or pipeline branch
3. **Write/modify agents**: Implement agent-specific logic; keep RAG calls explicit
4. **Add monitoring**: Log key steps, track latency and costs
5. **Test end-to-end**: Verify the full request path from API to response
6. **Update frontend**: Add UI if customer-facing (button, input, result display)

### Bug Fixes
- **Reproduce**: Identify which agent/component fails and under what conditions
- **Log context**: Add temporary logging to understand the failure
- **Fix at source**: Don't patch symptoms; address root cause
- **Test coverage**: Add a test case to prevent regression

## Tool Preferences

**When implementing or fixing code:**
- Prioritize correctness and clarity over brevity
- Explicitly handle error cases—don't assume happy paths
- Use logging strategically; avoid "print()" statements in final code
- Keep functions small and testable (< 20 lines preferred)
- Document non-obvious decisions with comments

## Multi-Step Task Guidance

When completing tasks with multiple steps:
1. **Break it down**: Identify all substeps before starting implementation
2. **Verify dependencies**: Ensure later steps don't depend on incomplete earlier ones
3. **Checkpoint**: After each major substep, confirm assumptions and adjust plan if needed
4. **Integration test**: Once complete, validate the assembled system works end-to-end

## Code Review Checklist
- [ ] Follows naming conventions (snake_case Python, camelCase JS)
- [ ] Error handling is explicit
- [ ] New functions/components have docstrings or comments
- [ ] Logging is in place for observability (agents, errors, latency)
- [ ] No hardcoded values (use constants or config)
- [ ] Frontend changes are responsive and tested in browser
- [ ] No silent failures or unhandled promises
- [ ] Architecture doesn't introduce circular dependencies between modules

## Common Patterns

### Querying the RAG Pipeline
```python
# Good: explicit import, error handling
from rag.pipeline import generate_answer
try:
    response = generate_answer(query)
except Exception as e:
    logger.error(f"RAG failed: {e}")
    response = "Unable to generate answer"
```

### FastAPI Endpoint with Logging
```python
from fastapi import FastAPI
import logging
logger = logging.getLogger(__name__)

@app.post("/endpoint")
def my_endpoint(data: dict):
    logger.info(f"Received: {data}")
    result = process(data)
    logger.info(f"Result: {result}")
    return {"result": result}
```

### React Component with State & Call Logging
```javascript
import { useState } from "react";
function Component() {
  const [state, setState] = useState(null);
  
  const handleAction = async () => {
    console.log("[Component] Action triggered");
    const res = await fetch("/api/endpoint");
    setState(res.data);
    console.log("[Component] State updated");
  };
  
  return <button onClick={handleAction}>Action</button>;
}
```

## When in Doubt
- **Architecture questions**: Trace the query path end-to-end; ask which component should own the feature
- **Naming questions**: Use the existing codebase as reference; consistency matters more than perfection
- **Performance questions**: Add logging first, measure, then optimize
- **Integration questions**: Write a simple end-to-end test before finalizing
