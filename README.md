# DevOps SRE Agent

Autonomous debugging and troubleshooting agent for production-grade systems from DevOps, SRE, and Operations perspective.

## Architecture

Multi-agent architecture with an **Orchestrator Agent** coordinating specialized sub-agents:

- **Observability Agent**: Queries Grafana for metrics, dashboards, and alerts
- **Infrastructure Agent**: Queries Kubernetes for cluster state, pods, services, and logs
- **Knowledge Search Agent**: Queries Stackoverflow for troubleshooting knowledge
- **Incident Management**: ServiceNow integration for incident tracking
- **Code Management**: GitHub integration for issues and PRs

## Technology Stack

- **LangGraph DeepAgent**: Multi-agent orchestration, Deep Agent is n Agent harness built using LangChain as framework (for tools, model access) and LangGraph as Runtime (for checkpoints, memory)
- **LiteLLM**: Unified LLM provider access
- **LangSmith**: Observability and tracing
- **MCP Servers** (via [Docker Hub](https://hub.docker.com/mcp)):
  - Kubernetes MCP Server
  - Grafana MCP Server
  - Stackoverflow MCP Server
  - ServiceNow MCP Server
  - GitHub MCP Server

## Quick Start

1. Install dependencies: `uv sync`
2. Configure environment variables (see `.env.example`)
3. Deploy MCP servers separately
4. Run agent: `python main.py`

## Detailed Implementation

See [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md) for complete implementation details.

## References

- [LangGraph DeepAgent Quickstarts](https://github.com/langchain-ai/deepagents-quickstarts/)
