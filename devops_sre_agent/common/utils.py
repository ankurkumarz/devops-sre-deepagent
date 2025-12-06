"""Common utility functions for DevOps SRE Agent."""

import json
from datetime import datetime
from typing import Any, Dict, Optional


def format_response(data: Any, format_type: str = "json") -> str:
    """Format response data.

    Args:
        data: Data to format
        format_type: Format type (json, markdown, text)

    Returns:
        str: Formatted response string
    """
    if format_type == "json":
        return json.dumps(data, indent=2, default=str)
    elif format_type == "markdown":
        # Basic markdown formatting
        if isinstance(data, dict):
            return "\n".join(f"**{k}**: {v}" for k, v in data.items())
        return str(data)
    else:
        return str(data)


def handle_error(error: Exception, context: Optional[str] = None) -> Dict[str, Any]:
    """Handle and format errors.

    Args:
        error: Exception that occurred
        context: Optional context about where the error occurred

    Returns:
        Dict containing error information
    """
    error_info = {
        "error": str(error),
        "error_type": type(error).__name__,
        "timestamp": datetime.utcnow().isoformat(),
    }

    if context:
        error_info["context"] = context

    return error_info


def format_timestamp(timestamp: Optional[datetime] = None) -> str:
    """Format timestamp to ISO format.

    Args:
        timestamp: Datetime object, defaults to current time

    Returns:
        str: ISO formatted timestamp
    """
    if timestamp is None:
        timestamp = datetime.utcnow()
    return timestamp.isoformat()


def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely parse JSON string.

    Args:
        json_str: JSON string to parse
        default: Default value if parsing fails

    Returns:
        Parsed JSON object or default value
    """
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

