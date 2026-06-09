"""AI provider integration using litellm."""

from typing import Any

import litellm

# Suppress litellm verbose logging
litellm.suppress_debug_info = True


def ask_ai(
    prompt: str,
    system_prompt: str,
    config: dict[str, Any],
) -> str:
    """Send a prompt to the AI model and return the response text."""
    model = config.get("model", "gpt-4o-mini")
    api_key = config.get("api_key")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1024,
    }

    if api_key:
        kwargs["api_key"] = api_key

    response = litellm.completion(**kwargs)
    return response.choices[0].message.content.strip()
