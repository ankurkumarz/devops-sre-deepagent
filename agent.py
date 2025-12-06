"""LangGraph agent entry point for langgraph dev."""

from typing import Annotated, TypedDict

from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages

from devops_sre_agent.common import setup_logging
from devops_sre_agent.orchestrator import OrchestratorAgent

# Set up logging
setup_logging()

# Define state for the graph
class AgentState(TypedDict):
    """State for the DevOps SRE Agent graph."""
    messages: Annotated[list, add_messages]
    issue_description: str
    session_id: str
    findings: dict
    recommendations: list


# Create orchestrator agent
orchestrator = OrchestratorAgent()


def troubleshoot_node(state: AgentState) -> AgentState:
    """Node that handles troubleshooting."""
    issue = state.get("issue_description") or state.get("messages", [])[-1].content if state.get("messages") else ""
    
    if not issue and state.get("messages"):
        # Extract issue from last message
        issue = str(state["messages"][-1].content)
    
    result = orchestrator.troubleshoot(issue, state.get("session_id"))
    
    # Update state with results
    state["findings"] = result.get("findings", {})
    state["recommendations"] = result.get("recommendations", [])
    
    return state


# Build the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("troubleshoot", troubleshoot_node)

# Set entry point
workflow.add_edge(START, "troubleshoot")
workflow.add_edge("troubleshoot", END)

# Compile the graph
agent = workflow.compile()

