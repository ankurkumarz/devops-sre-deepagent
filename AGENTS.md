## Repository Layout for LangGraph Agents
- `devops_sre_agent`: Core/root folder for DevOps & SRE Agent
- `subagents`:  Specific subagents for orchestrator to assign tasks to: `code_management_agent`, `incident_management_agent`, `infrastructure_agent`, `knowledge_search_agent`, `observability_agent`
- `main.py`: CLI entry point for running the agent
- `agent.py`: LangGraph entry point for dev server
- `pyproject.toml`: Project dependencies and configuration

## Dev & Local Build Instructions

### Prerequisites
- Python 3.13 (specified in `.python-version`)
- `uv` package manager installed ([Install uv](https://github.com/astral-sh/uv))

### Setup Steps

1. **Install dependencies using uv:**
   ```bash
   uv sync
   ```

2. Configure environment variables as per `.env.example`

### Running the Agent

#### Option 1: CLI Mode (Simple troubleshooting)
```bash
# Run using uv
uv run python main.py "Pod payment-service is crash-looping in production"
```

#### Option 2: LangGraph Dev Server (Interactive mode)
```bash
# Start the LangGraph development server
uv run langgraph dev
```

## Testing instructions

TBD

## PR instructions

TBD

