# DevOps SRE Agent Implementation Plan

## Overview

Transform the current research agent template into a production-grade DevOps SRE troubleshooting agent with multi-agent architecture using LangGraph DeepAgent. The agent autonomously debugs and troubleshoots production-grade systems from DevOps, SRE, and Operations perspective.

## Architecture Components

### Agent Structure

A multi-agent architecture with an **Orchestrator Agent** coordinating specialized sub-agents:

- **Orchestrator Agent**: Coordinates troubleshooting workflow, delegates to sub-agents, manages incidents via ServiceNow MCP, and creates/updates GitHub issues/PRs for tracking
- **Observability Agent**: Queries Grafana MCP for metrics, dashboards, alerts, and observability data
- **Infrastructure Agent**: Queries Kubernetes MCP for cluster state, pods, services, logs, and resource metrics
- **Knowledge Search Agent**: Queries Stackoverflow MCP for troubleshooting knowledge, error messages, and stack trace analysis

### Technology Stack

- **LangGraph**: Agent orchestration framework
- **LangGraph DeepAgent**: Multi-agent coordination pattern
- **LiteLLM**: Unified LLM provider access (OpenAI, Anthropic, Google, etc.)
- **LangSmith**: Observability, tracing, monitoring, and debugging for agent workflows
- **Mem0ai**: Memory management for agent context, learning from past troubleshooting sessions, and maintaining conversation history
- **MCP Servers** (via Docker Hub: https://hub.docker.com/mcp):
  - **Kubernetes MCP** ([kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server)): Pod status, logs, events, resource metrics, service discovery
  - **Grafana MCP** ([mcp-grafana](https://github.com/grafana/mcp-grafana)): Dashboards, metrics queries, alerts, Prometheus/Loki datasources
  - **Stackoverflow MCP** ([stackoverflow-mcp](https://github.com/gscalzo/stackoverflow-mcp)): Search by error messages, tags, and stack trace analysis
  - **ServiceNow MCP** ([servicenow-mcp](https://github.com/echelon-ai-labs/servicenow-mcp)): Incident management, change requests, knowledge base
  - **GitHub MCP** (Official): Issues, pull requests, repository operations

## Implementation Details

### File Structure

```
devops_sre_agent/
├── __init__.py              # Update exports
├── common/                  # Common/shared modules
│   ├── __init__.py
│   ├── config.py            # Configuration management
│   ├── llm.py               # LiteLLM setup and LLM configuration
│   ├── logging.py            # Logging configuration
│   ├── memory.py            # Mem0ai memory management
│   ├── mcp.py                # MCP client setup and utilities
│   └── utils.py             # Common utilities
├── prompts.py               # Shared prompts and orchestrator prompts
├── tools.py                 # Shared tools (think_tool, etc.)
├── orchestrator.py          # Orchestrator agent definition
└── sub_agents/
    ├── __init__.py          # Sub-agents exports
    ├── observability/
    │   ├── __init__.py
    │   ├── agent.py         # Observability agent definition
    │   ├── prompts.py       # Observability-specific prompts
    │   └── tools.py         # Grafana MCP tools
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── agent.py         # Infrastructure agent definition
    │   ├── prompts.py       # Infrastructure-specific prompts
    │   └── tools.py         # Kubernetes MCP tools
    ├── knowledge_search/
    │   ├── __init__.py
    │   ├── agent.py         # Knowledge search agent definition
    │   ├── prompts.py       # Knowledge search-specific prompts
    │   └── tools.py         # Stackoverflow MCP tools
    ├── incident_management/
    │   ├── __init__.py
    │   ├── agent.py         # Incident management agent definition
    │   ├── prompts.py       # Incident management-specific prompts
    │   └── tools.py         # ServiceNow MCP tools
    └── code_management/
        ├── __init__.py
        ├── agent.py         # Code management agent definition
        ├── prompts.py       # Code management-specific prompts
        └── tools.py         # GitHub MCP tools

tests/
├── __init__.py
├── unit/                    # Unit tests
│   ├── __init__.py
│   ├── test_orchestrator.py
│   ├── test_observability_agent.py
│   ├── test_infrastructure_agent.py
│   ├── test_knowledge_search_agent.py
│   ├── test_incident_management_agent.py
│   └── test_code_management_agent.py
├── integration/            # Integration tests
│   ├── __init__.py
│   ├── test_mcp_integration.py
│   ├── test_agent_workflow.py
│   └── test_end_to_end.py
├── evals/                   # Evaluation framework
│   ├── __init__.py
│   ├── test_cases/          # Test case JSON files
│   │   ├── pod_crash_loop.json
│   │   ├── high_latency.json
│   │   ├── resource_exhaustion.json
│   │   ├── service_unavailable.json
│   │   ├── network_issues.json
│   │   └── database_connection_failure.json
│   ├── evaluators.py        # Evaluation logic
│   ├── run_evals.py         # Evaluation runner
│   └── eval_results/        # Evaluation results
└── fixtures/                # Test fixtures
    ├── __init__.py
    ├── mock_mcp_responses.py
    └── sample_issues.py

agent.py                     # NEW: LangGraph agent entry point (for langgraph dev)
main.py                      # Update: CLI entry point with LiteLLM/LangSmith (optional)
langgraph.json               # Update: Fix graph reference for langgraph dev
pyproject.toml               # Project configuration (uv build tool)
uv.lock                      # Dependency lock file (uv, auto-generated)
.env.example                 # NEW: Environment template
.env                         # Local environment (gitignored)
pytest.ini                   # NEW: Pytest configuration
IMPLEMENTATION_PLAN.md       # This file
```

### Key Implementation Steps

#### 1. Create Common Module (`devops_sre_agent/common/`)

- **Create `common/config.py`**:
  - Load environment variables using `python-dotenv`
  - Configuration management (settings, defaults)
  - MCP server endpoint configuration
  - Model configuration (model names, temperature, max_tokens)
  - LangSmith configuration (API key, project name, tracing)
  - Configuration validation using Pydantic models
  - Singleton pattern for global config access
  - Example structure:
    ```python
    class AgentConfig:
        llm_provider: str
        model_name: str
        temperature: float
        langsmith_api_key: str
        langsmith_project: str
        mcp_servers: Dict[str, MCPConfig]
    ```

- **Create `common/llm.py`**:
  - LiteLLM initialization and setup
  - LLM provider configuration (OpenAI, Anthropic, Google)
  - Model selection and fallback logic
  - LLM client factory function
  - Shared LLM instance management (singleton pattern)
  - LangSmith callback integration for tracing
  - Example structure:
    ```python
    def get_llm(model_name: str = None, **kwargs) -> BaseChatModel:
        """Get configured LLM instance with LiteLLM"""
        # Implementation
    ```

- **Create `common/logging.py`**:
  - Structured logging configuration
  - Log levels configuration (DEBUG, INFO, WARNING, ERROR)
  - Agent-specific loggers (orchestrator, observability, etc.)
  - LangSmith trace integration
  - Log formatting and handlers (console, file)
  - Context managers for agent-specific logging
  - Example structure:
    ```python
    def get_logger(agent_name: str) -> logging.Logger:
        """Get agent-specific logger"""
        # Implementation
    ```

- **Create `common/mcp.py`**:
  - MCP client initialization
  - MCP server connection management
  - MCP tool registration utilities
  - Error handling for MCP connections
  - MCP client factory functions for each server type
  - Connection pooling and retry logic
  - Example structure:
    ```python
    def get_kubernetes_mcp_client() -> MCPClient:
        """Get Kubernetes MCP client"""
        # Implementation
    
    def get_grafana_mcp_client() -> MCPClient:
        """Get Grafana MCP client"""
        # Implementation
    ```

- **Create `common/memory.py`**:
  - Mem0ai initialization and setup
  - Memory storage configuration (vector store, database)
  - Memory retrieval functions for past troubleshooting sessions
  - Memory storage functions for current session context
  - Similar issue search using memory
  - Memory management utilities (add, search, update, delete)
  - Integration with agent workflows
  - Example structure:
    ```python
    from mem0 import Memory
    
    def get_memory_client() -> Memory:
        """Get Mem0ai memory client"""
        # Implementation
    
    def store_troubleshooting_session(session_id: str, issue: str, solution: str):
        """Store troubleshooting session in memory"""
        # Implementation
    
    def search_similar_issues(query: str) -> List[Dict]:
        """Search memory for similar past issues"""
        # Implementation
    ```

- **Create `common/utils.py`**:
  - Common utility functions
  - Response formatting helpers
  - Error handling utilities
  - Data transformation helpers
  - Time formatting utilities
  - JSON serialization helpers

#### 2. Create Agent Structure

- **Create `devops_sre_agent/orchestrator.py`**: Main orchestrator agent that coordinates sub-agents
  - Import common modules (config, llm, logging, memory)
  - Use shared LLM instance from `common.llm`
  - Use shared logging from `common.logging`
  - Use memory management from `common.memory`
  - Search memory for similar past issues before delegating
  - Store successful troubleshooting sessions in memory
  
- **Create `devops_sre_agent/sub_agents/` folder structure**: Organize each sub-agent in its own folder
- **Create sub-agent modules**:
  - `sub_agents/observability/`: Grafana MCP integration
  - `sub_agents/infrastructure/`: Kubernetes MCP integration
  - `sub_agents/knowledge_search/`: Stackoverflow MCP integration
  - `sub_agents/incident_management/`: ServiceNow MCP integration
  - `sub_agents/code_management/`: GitHub MCP integration
- Each sub-agent folder contains:
  - `agent.py`: Agent definition (uses common.llm, common.logging, common.memory)
  - `prompts.py`: Agent-specific prompts
  - `tools.py`: MCP tools for that agent (uses common.mcp)
  - `__init__.py`: Module exports
- **Create `agent.py`** (root): LangGraph entry point that imports orchestrator
- Configure agent delegation strategy
- Set up MCP server connections using `common.mcp`
- All agents use shared LLM configuration from `common.llm`
- All agents use shared logging from `common.logging`
- All agents use shared memory management from `common.memory`
- Orchestrator searches memory for similar past issues before delegating
- Successful troubleshooting sessions are stored in memory for future reference
- Configure LangSmith for observability and tracing

#### 2. Create Prompts Structure

- **Update `devops_sre_agent/prompts.py`**: Shared prompts and orchestrator-specific prompts:
  - Orchestrator Workflow: Issue triage, troubleshooting workflow, delegation strategy
  - Incident creation/updates via ServiceNow
  - GitHub issue/PR creation for tracking

- **Create sub-agent prompts**:
  - `sub_agents/observability/prompts.py`: 
    - Metrics analysis and dashboard queries
    - Alert investigation
    - Prometheus/Loki query patterns
  - `sub_agents/infrastructure/prompts.py`:
    - Kubernetes resource inspection patterns
    - Pod/Service/Deployment troubleshooting
    - Log analysis workflows
  - `sub_agents/knowledge_search/prompts.py`:
    - Error message search strategies
    - Stack trace analysis
    - Similar issue identification
  - `sub_agents/incident_management/prompts.py`:
    - Incident creation and management workflows
    - Change request handling
  - `sub_agents/code_management/prompts.py`:
    - Issue and PR creation workflows
    - Repository operations

#### 3. Create Tools Structure

- **Update `devops_sre_agent/tools.py`**: Shared tools (keep `think_tool`, remove `tavily_search`)

- **Create sub-agent tools**:
  - `sub_agents/observability/tools.py`: 
    - Grafana MCP tools: Dashboard queries, metric retrieval, alert status, datasource operations
  - `sub_agents/infrastructure/tools.py`:
    - Kubernetes MCP tools: Pod operations, log retrieval, event queries, resource metrics
  - `sub_agents/knowledge_search/tools.py`:
    - Stackoverflow MCP tools: Error search, tag-based search, stack trace analysis
  - `sub_agents/incident_management/tools.py`:
    - ServiceNow MCP tools: Incident CRUD, change management, knowledge base queries
  - `sub_agents/code_management/tools.py`:
    - GitHub MCP tools: Issue creation/updates, PR operations, repository queries

#### 4. Configuration Updates

- **`langgraph.json`**: Update graph reference to point to correct agent entry point
  - Update graph name from "research" to "devops_sre_agent"
  - Point to correct agent entry point: `"./agent.py:agent"`
  - Ensure dependencies include the package
  - Configure environment file path: `".env"`
  - Example:
    ```json
    {
      "dependencies": ["."],
      "graphs": {
        "devops_sre_agent": "./agent.py:agent"
      },
      "env": ".env"
    }
    ```

- **`.env.example`**: Add environment variables for:
  - LiteLLM configuration (API keys for OpenAI/Anthropic/Google)
  - LangSmith API key and project name
  - MCP server endpoints/configuration (if needed)
  - Model configuration

- **`pyproject.toml`**: Update dependencies using uv
  - Add `langgraph-cli[inmem]` for local development: `uv add langgraph-cli[inmem]`
  - Add testing dependencies: `uv add --dev pytest pytest-asyncio pytest-mock`
  - Ensure all dependencies are properly specified
  - Run `uv sync` to install dependencies and generate `uv.lock`

- **Local Development Setup with uv**:
  - Install dependencies: `uv sync`
  - Ensure `langgraph-cli[inmem]` is installed (via `uv add langgraph-cli[inmem]`)
  - Configure `agent.py` to export the agent graph properly
  - Set up `.env` file from `.env.example`
  - Test with `uv run langgraph dev` command

#### 5. Main Entry Point and LangGraph Dev Setup

- **Create `agent.py` (root)**: LangGraph entry point
  - Export agent graph for `langgraph dev`
  - Import orchestrator and configure graph
  - Ensure proper graph structure for LangGraph CLI
  - Example:
    ```python
    from devops_sre_agent.orchestrator import create_orchestrator_agent
    
    agent = create_orchestrator_agent()
    ```

- **Update `main.py`**: CLI entry point (optional, for direct Python execution)
  - Import common modules (config, logging)
  - Initialize configuration from `common.config`
  - Set up logging from `common.logging`
  - Initialize agent (which uses `common.llm` and `common.mcp`)
  - Set up LangSmith tracing
  - Create CLI interface for agent interaction

- **Local Development with `langgraph dev`**:
  - Install `langgraph-cli[inmem]` package
  - Configure `langgraph.json` properly
  - Create `.env` file with required variables
  - Run: `langgraph dev`
  - Access agent via LangGraph Studio UI (typically http://localhost:8123)

#### 6. Update Module Exports

- **Create `devops_sre_agent/common/__init__.py`**: Export common modules (config, llm, logging, memory, mcp, utils)
- **Update `devops_sre_agent/__init__.py`**: Export orchestrator, common modules, and shared components
- **Update `devops_sre_agent/sub_agents/__init__.py`**: Export all sub-agents
- **Update each sub-agent `__init__.py`**: Export agent, prompts, and tools for that sub-agent
- Remove research agent exports

### Workflow Design

1. **User reports issue** → Orchestrator analyzes the problem
2. **Orchestrator searches memory** → Check for similar past issues and solutions
3. **Orchestrator creates troubleshooting plan** → Breaks down into tasks (incorporates memory insights)
4. **Delegates to appropriate sub-agents**:
   - Infrastructure Agent: Check Kubernetes resources, pods, logs
   - Observability Agent: Query Grafana for metrics, alerts, dashboards
   - Knowledge Agent: Search Stackoverflow for similar issues
5. **Orchestrator synthesizes findings** → Combines insights from all agents and memory
6. **Generates actionable recommendations** → Provides solution steps
7. **Store successful session in memory** → Save issue, solution, and context for future reference
8. **Optional**: Creates ServiceNow incident or GitHub issue for tracking

## Dependencies

### Python Packages

- `deepagents>=0.2.8` - Multi-agent coordination
- `langchain-*` - LangChain integrations
- `langgraph-cli[inmem]>=0.1.55` - LangGraph CLI for local development (to be added)
- `litellm` - Unified LLM provider access (to be added)
- `langsmith` - Observability, tracing, and evaluation (to be added)
- `mem0ai` - Memory management for agent context and learning (to be added)
- `pytest>=8.0.0` - Testing framework (to be added)
- `pytest-asyncio>=0.23.0` - Async test support (to be added)
- `pytest-mock>=3.12.0` - Mocking utilities (to be added)
- `httpx>=0.28.1` - HTTP client
- `pydantic>=2.12.5` - Data validation
- `python-dotenv>=1.2.1` - Environment variable management

### MCP Servers

MCP servers deployed separately via Docker Hub registry: https://hub.docker.com/mcp

- **Kubernetes MCP**: Available as Docker image from Docker Hub
- **Grafana MCP**: Available as Docker image from Docker Hub  
- **Stackoverflow MCP**: Available as Docker image from Docker Hub
- **ServiceNow MCP**: Available as Docker image from Docker Hub (community)
- **GitHub MCP**: Official GitHub MCP Server from Docker Hub

MCP servers can be run as Docker containers or via stdio/SSE/HTTP transport protocols.

### External Services

- **LiteLLM**: Configure with API keys for desired LLM providers
- **LangSmith**: Requires API key and project configuration
- **MCP Servers**: Deployed separately, accessible via configured transport

## Testing and Evaluation

### Test Structure

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_orchestrator.py
│   ├── test_observability_agent.py
│   ├── test_infrastructure_agent.py
│   ├── test_knowledge_search_agent.py
│   ├── test_incident_management_agent.py
│   └── test_code_management_agent.py
├── integration/
│   ├── __init__.py
│   ├── test_mcp_integration.py
│   ├── test_agent_workflow.py
│   └── test_end_to_end.py
├── evals/
│   ├── __init__.py
│   ├── test_cases/
│   │   ├── pod_crash_loop.json
│   │   ├── high_latency.json
│   │   ├── resource_exhaustion.json
│   │   ├── service_unavailable.json
│   │   ├── network_issues.json
│   │   └── database_connection_failure.json
│   ├── evaluators.py
│   ├── run_evals.py
│   └── eval_results/
│       └── .gitkeep
└── fixtures/
    ├── __init__.py
    ├── mock_mcp_responses.py
    └── sample_issues.py
```

### Unit Tests

- **Orchestrator Tests** (`test_orchestrator.py`):
  - Issue triage logic
  - Agent delegation decisions
  - Workflow coordination
  - Response synthesis

- **Sub-Agent Tests**:
  - Each sub-agent has dedicated test file
  - Test agent-specific logic
  - Test prompt handling
  - Test tool integration (mocked)

- **Mock MCP Responses**:
  - Create fixtures for common MCP responses
  - Test error handling
  - Test response parsing

### Integration Tests

- **MCP Integration Tests** (`test_mcp_integration.py`):
  - Test actual MCP server connections (optional)
  - Test MCP tool calls
  - Test error handling for connection failures

- **Agent Workflow Tests** (`test_agent_workflow.py`):
  - Test orchestrator → sub-agent delegation
  - Test parallel agent execution
  - Test response aggregation

- **End-to-End Tests** (`test_end_to_end.py`):
  - Full troubleshooting workflow
  - Real-world scenario simulation
  - Performance benchmarks

### Evaluation Framework

#### Evaluation Metrics

1. **Accuracy Metrics**:
   - Correct issue identification rate
   - Correct root cause analysis
   - Solution effectiveness

2. **Efficiency Metrics**:
   - Time to identify issue
   - Number of MCP calls required
   - Token usage per scenario

3. **Completeness Metrics**:
   - All relevant data sources queried
   - All sub-agents utilized appropriately
   - Comprehensive solution provided

4. **Quality Metrics**:
   - Actionable recommendations
   - Clear explanation of findings
   - Proper incident/issue creation (if applicable)

#### Test Cases

Create structured test cases in `tests/evals/test_cases/`:

**Example Test Case Structure** (`pod_crash_loop.json`):
```json
{
  "id": "pod_crash_loop_001",
  "name": "Pod Crash Loop - Memory Limit",
  "description": "Application pod crashing due to memory limit exceeded",
  "scenario": {
    "issue_type": "infrastructure",
    "symptoms": [
      "Pod restarting every 30 seconds",
      "OOMKilled events in pod logs",
      "Memory usage spiking to 100%"
    ],
    "expected_agents": ["infrastructure", "observability"],
    "expected_actions": [
      "Check pod status and events",
      "Query pod logs for OOM errors",
      "Check resource metrics",
      "Identify memory limit configuration"
    ]
  },
  "mock_responses": {
    "kubernetes": {
      "pod_status": "CrashLoopBackOff",
      "events": ["OOMKilled"],
      "logs": ["Out of memory error"]
    },
    "grafana": {
      "memory_metrics": "100% usage"
    }
  },
  "expected_output": {
    "root_cause": "Memory limit too low for application workload",
    "recommendations": [
      "Increase memory limit in deployment",
      "Optimize application memory usage",
      "Add memory monitoring alerts"
    ]
  },
  "evaluation_criteria": {
    "must_identify_root_cause": true,
    "must_provide_solution": true,
    "must_check_logs": true,
    "must_check_metrics": true
  }
}
```

**Test Case Categories**:

1. **Infrastructure Issues**:
   - Pod crash loops
   - Resource exhaustion (CPU/Memory)
   - Network connectivity issues
   - Storage problems

2. **Performance Issues**:
   - High latency
   - Slow response times
   - Throughput degradation
   - Database connection pool exhaustion

3. **Availability Issues**:
   - Service unavailability
   - Health check failures
   - Load balancer issues
   - DNS resolution problems

4. **Application Issues**:
   - Application errors
   - Database connection failures
   - API timeouts
   - Authentication failures

5. **Observability Issues**:
   - Missing metrics
   - Alert false positives
   - Dashboard data gaps
   - Log aggregation failures

#### Evaluation Implementation

**Create `tests/evals/evaluators.py`**:

```python
from langsmith import Client
from langchain.smith import RunEvaluator
from typing import Dict, Any

class DevOpsSREEvaluator:
    """Evaluator for DevOps SRE Agent performance"""
    
    def evaluate_root_cause_accuracy(self, run, example):
        """Evaluate if root cause was correctly identified"""
        # Implementation
        pass
    
    def evaluate_solution_quality(self, run, example):
        """Evaluate solution quality and actionability"""
        # Implementation
        pass
    
    def evaluate_agent_utilization(self, run, example):
        """Evaluate if correct sub-agents were used"""
        # Implementation
        pass
    
    def evaluate_completeness(self, run, example):
        """Evaluate if all relevant data sources were queried"""
        # Implementation
        pass
```

**Create `tests/evals/run_evals.py`**:

- Load test cases from `test_cases/` directory
- Run agent against each test case
- Evaluate using evaluators
- Generate evaluation report
- Track results in LangSmith

#### LangSmith Integration

- Use LangSmith for evaluation tracking
- Create evaluation datasets
- Run evaluations via LangSmith API
- Track evaluation metrics over time
- Compare agent versions

### Evaluation Workflow

1. **Prepare Test Cases**:
   - Create test case JSON files
   - Define expected outcomes
   - Set up mock MCP responses

2. **Run Evaluations**:
   ```bash
   uv run python tests/evals/run_evals.py --test-cases tests/evals/test_cases/
   ```
   Or with activated virtual environment:
   ```bash
   source .venv/bin/activate
   python tests/evals/run_evals.py --test-cases tests/evals/test_cases/
   ```

3. **Review Results**:
   - Check evaluation metrics
   - Review LangSmith traces
   - Identify areas for improvement

4. **Iterate**:
   - Update prompts based on failures
   - Refine agent logic
   - Add new test cases

### Continuous Evaluation

- Run evaluations on CI/CD pipeline
- Track metrics over time
- Set evaluation thresholds for PRs
- Generate evaluation reports

## Environment Setup

### Required Environment Variables

Create `.env` file from `.env.example`:

```bash
# LiteLLM Configuration
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GOOGLE_API_KEY=your-google-key

# LangSmith Configuration
LANGSMITH_API_KEY=your-langsmith-key
LANGSMITH_PROJECT=devops-sre-agent

# Mem0ai Configuration
MEM0_API_KEY=your-mem0-api-key  # Optional, if using Mem0 cloud
MEM0_VECTOR_STORE=chroma  # or pinecone, weaviate, etc.
MEM0_DATABASE_URL=sqlite:///memory.db  # or postgresql://, etc.

# MCP Server Configuration (if needed)
KUBERNETES_MCP_ENDPOINT=http://localhost:8080
GRAFANA_MCP_ENDPOINT=http://localhost:3000
# ... other MCP endpoints
```

### Local Development with LangGraph Dev

1. **Install LangGraph CLI using uv**:
   ```bash
   uv add langgraph-cli[inmem]
   ```
   This adds the dependency to `pyproject.toml` and installs it.

2. **Configure `langgraph.json`**:
   - Ensure graph name matches your agent
   - Point to correct entry point: `"./agent.py:agent"`
   - Set environment file: `".env"`

3. **Start Development Server**:
   ```bash
   uv run langgraph dev
   ```
   Or with activated virtual environment:
   ```bash
   source .venv/bin/activate
   langgraph dev
   ```

4. **Access LangGraph Studio**:
   - Open browser to http://localhost:8123 (default)
   - Interact with agent through UI
   - View traces and debug agent execution

5. **Development Workflow**:
   - Make code changes
   - LangGraph dev server auto-reloads
   - Test changes immediately in UI
   - View LangSmith traces for debugging

### Build Tool: uv

This project uses **uv** as the build tool and package manager:

- **Install dependencies**: `uv sync`
- **Add new dependency**: `uv add package-name`
- **Add dev dependency**: `uv add --dev package-name`
- **Run commands**: `uv run command` (runs in virtual environment)
- **Activate venv**: `source .venv/bin/activate` (after `uv sync`, optional)
- **Update dependencies**: `uv sync --upgrade`
- **Lock file**: `uv.lock` (auto-generated, commit to git)
- **Project structure**: Uses `pyproject.toml` for project configuration

**Benefits of uv**:
- Fast dependency resolution and installation
- Automatic virtual environment management
- Compatible with PEP 517/518 standards
- Lock file for reproducible builds

### Build Tool: uv

This project uses **uv** as the build tool and package manager:

- **Install dependencies**: `uv sync`
- **Add new dependency**: `uv add package-name`
- **Add dev dependency**: `uv add --dev package-name`
- **Run commands**: `uv run command` (runs in virtual environment)
- **Activate venv**: `source .venv/bin/activate` (after `uv sync`)
- **Update dependencies**: `uv sync --upgrade`
- **Lock file**: `uv.lock` (auto-generated, commit to git)

## Implementation Checklist

- [ ] Create `common/` module with shared configuration:
  - [ ] `common/config.py` - Configuration management
  - [ ] `common/llm.py` - LiteLLM setup and LLM configuration
  - [ ] `common/logging.py` - Logging configuration
  - [ ] `common/memory.py` - Mem0ai memory management
  - [ ] `common/mcp.py` - MCP client utilities
  - [ ] `common/utils.py` - Common utilities
  - [ ] `common/__init__.py` - Common module exports
- [ ] Create `sub_agents/` folder structure with all sub-agent folders
- [ ] Create `orchestrator.py` with LangGraph DeepAgent orchestrator (using common modules)
- [ ] Create each sub-agent module (agent.py, prompts.py, tools.py, __init__.py):
  - [ ] Observability agent (using common.llm, common.logging, common.memory, common.mcp)
  - [ ] Infrastructure agent (using common.llm, common.logging, common.memory, common.mcp)
  - [ ] Knowledge search agent (using common.llm, common.logging, common.memory, common.mcp)
  - [ ] Incident management agent (using common.llm, common.logging, common.memory, common.mcp)
  - [ ] Code management agent (using common.llm, common.logging, common.memory, common.mcp)
- [ ] Update `prompts.py` with orchestrator and shared prompts
- [ ] Update `tools.py` to remove tavily_search, keep shared tools
- [ ] Create `agent.py` (root) as LangGraph entry point
- [ ] Update all `__init__.py` files to export correct components
- [ ] Update `main.py` to use common modules (config, logging, memory) and initialize agent
- [ ] Integrate memory management in orchestrator:
  - [ ] Search memory for similar past issues
  - [ ] Store successful troubleshooting sessions
  - [ ] Use memory context in agent decision-making
- [ ] Update `langgraph.json` to reference correct agent entry point and configure for local dev
- [ ] Create `agent.py` (root) as LangGraph entry point for `langgraph dev`
- [ ] Create `.env.example` with all required environment variables
- [ ] Test local development setup with `langgraph dev`
- [ ] Create test structure (`tests/` directory)
- [ ] Create unit tests for orchestrator and sub-agents
- [ ] Create integration tests for MCP connections
- [ ] Create evaluation framework (`tests/evals/`)
- [ ] Create test case JSON files for common scenarios
- [ ] Implement evaluators for accuracy, quality, and completeness
- [ ] Set up LangSmith evaluation tracking
- [ ] Create `run_evals.py` script for running evaluations
- [ ] Document evaluation process and metrics
- [ ] Test agent with sample troubleshooting scenarios
- [ ] Document MCP server setup and configuration

## References

- [LangGraph DeepAgent Quickstarts](https://github.com/langchain-ai/deepagents-quickstarts/)
- [Kubernetes MCP Server](https://github.com/containers/kubernetes-mcp-server)
- [Grafana MCP Server](https://github.com/grafana/mcp-grafana)
- [Stackoverflow MCP Server](https://github.com/gscalzo/stackoverflow-mcp)
- [ServiceNow MCP Server](https://github.com/echelon-ai-labs/servicenow-mcp)
- [Docker Hub MCP Registry](https://hub.docker.com/mcp)

