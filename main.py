"""Main entry point for DevOps SRE Agent."""

import sys

from devops_sre_agent.common import setup_logging
from devops_sre_agent.orchestrator import OrchestratorAgent


def main():
    """Main entry point."""
    # Set up logging
    setup_logging()

    # Initialize orchestrator
    orchestrator = OrchestratorAgent()

    # Simple CLI interface
    if len(sys.argv) > 1:
        issue = " ".join(sys.argv[1:])
        print(f"Troubleshooting issue: {issue}")
        result = orchestrator.troubleshoot(issue)
        print(f"\nResults: {result}")
    else:
        print("DevOps SRE Agent")
        print("Usage: python main.py <issue description>")
        print("\nFor LangGraph dev server, use: uv run langgraph dev")


if __name__ == "__main__":
    main()
