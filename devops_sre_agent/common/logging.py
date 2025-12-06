"""Logging configuration for DevOps SRE Agent."""

import logging
import os
import sys
from typing import Optional

from devops_sre_agent.common.config import get_config


def setup_logging(level: Optional[str] = None) -> None:
    """Set up logging configuration.

    Args:
        level: Optional log level override (DEBUG, INFO, WARNING, ERROR)
    """
    config = get_config()

    # Determine log level
    log_level = level or os.getenv("LOG_LEVEL", "INFO").upper()

    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )

    # Set LangSmith logging if enabled
    if config.langsmith_tracing:
        logging.getLogger("langsmith").setLevel(logging.INFO)


def get_logger(agent_name: str) -> logging.Logger:
    """Get agent-specific logger.

    Args:
        agent_name: Name of the agent (e.g., 'orchestrator', 'observability')

    Returns:
        logging.Logger: Configured logger instance
    """
    logger_name = f"devops_sre_agent.{agent_name}"
    return logging.getLogger(logger_name)

