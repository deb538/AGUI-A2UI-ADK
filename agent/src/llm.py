"""LLM configuration helpers.

Supports both:
- OpenAI direct (`OPENAI_API_KEY`)
- AI Credits OpenAI-compatible endpoint (`AI_CREDIT_API_KEY`)
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load env vars from both agent/.env and repo-root .env
_SRC_DIR = Path(__file__).resolve().parent
_AGENT_DIR = _SRC_DIR.parent
_ROOT_DIR = _AGENT_DIR.parent
load_dotenv(_AGENT_DIR / ".env")
load_dotenv(_ROOT_DIR / ".env")


def _is_truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def create_chat_openai(
    *,
    openai_default_model: str,
    ai_credits_default_model: str,
    model_kwargs: dict | None = None,
) -> ChatOpenAI:
    """Create a ChatOpenAI model configured from environment variables."""

    openai_api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    ai_credits_api_key = (os.getenv("AI_CREDIT_API_KEY") or "").strip()

    explicit_base_url = (os.getenv("OPENAI_BASE_URL") or "").strip()
    use_ai_credits = _is_truthy(os.getenv("USE_AI_CREDITS"))

    # Some setups put AI Credits key into OPENAI_API_KEY (e.g. sk-live-...)
    # while expecting OpenAI-compatible routing to AI Credits.
    inferred_ai_credits_key = (
        openai_api_key if (openai_api_key.startswith("sk-live-") and not ai_credits_api_key) else ""
    )
    effective_ai_credits_key = ai_credits_api_key or inferred_ai_credits_key

    # Auto-select AI Credits when its key exists and OpenAI key is absent,
    # or when explicitly requested.
    if (effective_ai_credits_key and not openai_api_key) or use_ai_credits or bool(inferred_ai_credits_key):
        model_name = (
            os.getenv("AI_CREDIT_MODEL")
            or os.getenv("OPENAI_MODEL")
            or ai_credits_default_model
        )
        return ChatOpenAI(
            model=model_name,
            api_key=effective_ai_credits_key,
            base_url=explicit_base_url or "https://api.aicredits.in/v1",
            model_kwargs=model_kwargs or {},
        )

    if openai_api_key:
        model_name = os.getenv("OPENAI_MODEL") or openai_default_model
        kwargs = {
            "model": model_name,
            "api_key": openai_api_key,
            "model_kwargs": model_kwargs or {},
        }
        if explicit_base_url:
            kwargs["base_url"] = explicit_base_url
        return ChatOpenAI(**kwargs)

    raise ValueError(
        "No API key found. Set OPENAI_API_KEY for OpenAI, or set "
        "AI_CREDIT_API_KEY (and optional USE_AI_CREDITS=true)."
    )
