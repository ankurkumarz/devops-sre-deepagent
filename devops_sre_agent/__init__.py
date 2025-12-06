"""Deep Research based DevOps and SRE Agent

"""

from devops_sre_agent.prompts import (
    DEVOPS_SRE_AGENT_INSTRUCTIONS,
    DEVOPS_SRE_AGENT_WORKFLOW_INSTRUCTIONS,
    SUBAGENT_DELEGATION_INSTRUCTIONS,
)
from devops_sre_agent.tools import tavily_search, think_tool

__all__ = [
    "tavily_search",
    "think_tool",
    "RESEARCHER_INSTRUCTIONS",
    "RESEARCH_WORKFLOW_INSTRUCTIONS",
    "SUBAGENT_DELEGATION_INSTRUCTIONS",
]