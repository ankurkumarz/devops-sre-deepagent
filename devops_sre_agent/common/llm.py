"""LLM configuration and management using LiteLLM."""

from functools import lru_cache
from typing import Optional

from langchain_core.language_models import BaseChatModel

try:
    from langchain_community.chat_models import ChatLiteLLM
except ImportError:
    # Fallback to OpenAI if LiteLLM not available
    from langchain_openai import ChatOpenAI as ChatLiteLLM  # type: ignore

from devops_sre_agent.common.config import get_config


@lru_cache()
def get_llm(model_name: Optional[str] = None, **kwargs) -> BaseChatModel:
    """Get configured LLM instance with LiteLLM.

    Args:
        model_name: Optional model name override
        **kwargs: Additional LLM parameters

    Returns:
        BaseChatModel: Configured LLM instance
    """
    config = get_config()

    # Use provided model_name or fall back to config
    final_model_name = model_name or config.model_name

    # Prepare LLM parameters
    llm_params = {
        "model": final_model_name,
        "temperature": kwargs.get("temperature", config.temperature),
    }

    if config.max_tokens:
        llm_params["max_tokens"] = config.max_tokens

    # Add any additional kwargs
    llm_params.update(kwargs)

    # Initialize LLM with LiteLLM
    # LiteLLM automatically handles provider routing based on model name
    try:
        llm = ChatLiteLLM(**llm_params)
    except Exception:
        # Fallback to OpenAI if LiteLLM fails
        from langchain_openai import ChatOpenAI

        llm_params["model"] = final_model_name.replace("gpt-", "").replace("claude-", "")
        llm = ChatOpenAI(**llm_params)

    return llm

