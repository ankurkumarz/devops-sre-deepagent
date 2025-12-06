"""Common modules for DevOps SRE Agent.

This module provides shared configuration, LLM, logging, memory, and MCP utilities
used across all agents.
"""

from devops_sre_agent.common.config import AgentConfig, get_config
from devops_sre_agent.common.llm import get_llm
from devops_sre_agent.common.logging import get_logger, setup_logging
from devops_sre_agent.common.memory import (
    get_memory_client,
    search_similar_issues,
    store_troubleshooting_session,
)
from devops_sre_agent.common.mcp import (
    get_grafana_mcp_client,
    get_github_mcp_client,
    get_kubernetes_mcp_client,
    get_servicenow_mcp_client,
    get_stackoverflow_mcp_client,
)
from devops_sre_agent.common.utils import format_response, handle_error

__all__ = [
    # Config
    "AgentConfig",
    "get_config",
    # LLM
    "get_llm",
    # Logging
    "get_logger",
    "setup_logging",
    # Memory
    "get_memory_client",
    "search_similar_issues",
    "store_troubleshooting_session",
    # MCP
    "get_kubernetes_mcp_client",
    "get_grafana_mcp_client",
    "get_stackoverflow_mcp_client",
    "get_servicenow_mcp_client",
    "get_github_mcp_client",
    # Utils
    "format_response",
    "handle_error",
]

