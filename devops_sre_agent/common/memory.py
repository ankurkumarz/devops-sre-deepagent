"""Memory management using Mem0ai for DevOps SRE Agent."""

from functools import lru_cache
from typing import Dict, List, Optional

from devops_sre_agent.common.config import get_config

try:
    from mem0 import Memory
except ImportError:
    Memory = None  # type: ignore


@lru_cache()
def get_memory_client() -> Optional["Memory"]:
    """Get Mem0ai memory client.

    Returns:
        Optional[Memory]: Mem0ai memory client instance, or None if not configured
    """
    if Memory is None:
        return None

    config = get_config()

    # Initialize Mem0ai memory client
    memory_config = {
        "vector_store": {
            "provider": config.mem0_vector_store,
            "config": {},
        },
    }

    # Add database configuration if provided
    if config.mem0_database_url:
        memory_config["database"] = {
            "provider": "sqlite" if "sqlite" in config.mem0_database_url else "postgresql",
            "config": {"url": config.mem0_database_url},
        }

    # Add API key if provided (for cloud)
    if config.mem0_api_key:
        memory_config["api_key"] = config.mem0_api_key

    try:
        memory = Memory.from_config(memory_config)
        return memory
    except Exception as e:
        # Log error but don't fail - memory is optional
        import logging

        logger = logging.getLogger("devops_sre_agent.common.memory")
        logger.warning(f"Failed to initialize Mem0ai memory: {e}")
        return None


def store_troubleshooting_session(
    session_id: str,
    issue: str,
    solution: str,
    context: Optional[Dict] = None,
) -> bool:
    """Store troubleshooting session in memory.

    Args:
        session_id: Unique session identifier
        issue: Description of the issue
        solution: Solution that was applied
        context: Additional context (metrics, logs, etc.)

    Returns:
        bool: True if stored successfully, False otherwise
    """
    memory = get_memory_client()
    if memory is None:
        return False

    try:
        # Create memory entry
        memory_entry = {
            "issue": issue,
            "solution": solution,
            "session_id": session_id,
        }

        if context:
            memory_entry.update(context)

        # Store in memory
        memory.add(memory_entry)
        return True
    except Exception as e:
        import logging

        logger = logging.getLogger("devops_sre_agent.common.memory")
        logger.error(f"Failed to store troubleshooting session: {e}")
        return False


def search_similar_issues(query: str, limit: int = 5) -> List[Dict]:
    """Search memory for similar past issues.

    Args:
        query: Search query (issue description)
        limit: Maximum number of results to return

    Returns:
        List[Dict]: List of similar issues with solutions
    """
    memory = get_memory_client()
    if memory is None:
        return []

    try:
        # Search memory for similar issues
        results = memory.search(query, limit=limit)
        return results
    except Exception as e:
        import logging

        logger = logging.getLogger("devops_sre_agent.common.memory")
        logger.error(f"Failed to search memory: {e}")
        return []

