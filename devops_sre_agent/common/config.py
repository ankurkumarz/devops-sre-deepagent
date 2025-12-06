"""Configuration management for DevOps SRE Agent."""

import os
from functools import lru_cache
from typing import Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()


class MCPConfig(BaseModel):
    """MCP server configuration."""

    endpoint: Optional[str] = None
    transport: str = "stdio"  # stdio, sse, or streamable-http
    env: Optional[Dict[str, str]] = None


class AgentConfig(BaseModel):
    """Main agent configuration."""

    # LLM Configuration
    llm_provider: str = Field(default="openai", description="LLM provider (openai, anthropic, google)")
    model_name: str = Field(default="gpt-4", description="Model name")
    temperature: float = Field(default=0.7, description="Temperature for LLM")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens for LLM")

    # LangSmith Configuration
    langsmith_api_key: Optional[str] = Field(default=None, description="LangSmith API key")
    langsmith_project: str = Field(default="devops-sre-agent", description="LangSmith project name")
    langsmith_tracing: bool = Field(default=True, description="Enable LangSmith tracing")

    # Mem0ai Configuration
    mem0_api_key: Optional[str] = Field(default=None, description="Mem0ai API key (optional)")
    mem0_vector_store: str = Field(default="chroma", description="Vector store type")
    mem0_database_url: str = Field(
        default="sqlite:///memory.db", description="Database URL for memory storage"
    )

    # MCP Server Configuration
    mcp_servers: Dict[str, MCPConfig] = Field(
        default_factory=dict, description="MCP server configurations"
    )

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_config() -> AgentConfig:
    """Get singleton agent configuration.

    Returns:
        AgentConfig: The agent configuration instance
    """
    return AgentConfig(
        llm_provider=os.getenv("LLM_PROVIDER", "openai"),
        model_name=os.getenv("MODEL_NAME", "gpt-4"),
        temperature=float(os.getenv("TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("MAX_TOKENS", "0")) if os.getenv("MAX_TOKENS") else None,
        langsmith_api_key=os.getenv("LANGSMITH_API_KEY"),
        langsmith_project=os.getenv("LANGSMITH_PROJECT", "devops-sre-agent"),
        langsmith_tracing=os.getenv("LANGSMITH_TRACING", "true").lower() == "true",
        mem0_api_key=os.getenv("MEM0_API_KEY"),
        mem0_vector_store=os.getenv("MEM0_VECTOR_STORE", "chroma"),
        mem0_database_url=os.getenv("MEM0_DATABASE_URL", "sqlite:///memory.db"),
        mcp_servers={
            "kubernetes": MCPConfig(
                endpoint=os.getenv("KUBERNETES_MCP_ENDPOINT"),
                transport=os.getenv("KUBERNETES_MCP_TRANSPORT", "stdio"),
            ),
            "grafana": MCPConfig(
                endpoint=os.getenv("GRAFANA_MCP_ENDPOINT"),
                transport=os.getenv("GRAFANA_MCP_TRANSPORT", "stdio"),
            ),
            "stackoverflow": MCPConfig(
                endpoint=os.getenv("STACKOVERFLOW_MCP_ENDPOINT"),
                transport=os.getenv("STACKOVERFLOW_MCP_TRANSPORT", "stdio"),
            ),
            "servicenow": MCPConfig(
                endpoint=os.getenv("SERVICENOW_MCP_ENDPOINT"),
                transport=os.getenv("SERVICENOW_MCP_TRANSPORT", "stdio"),
            ),
            "github": MCPConfig(
                endpoint=os.getenv("GITHUB_MCP_ENDPOINT"),
                transport=os.getenv("GITHUB_MCP_TRANSPORT", "stdio"),
            ),
        },
    )

