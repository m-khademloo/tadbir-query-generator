"""LLM client using litellm with retries, timeout, and optional JSON response."""

import json
import logging
import os
import time
import uuid
from typing import Any

import litellm

logger = logging.getLogger(__name__)


class LLMClient:
    """Abstraction over litellm for completion with retries and timeout."""

    def __init__(
        self,
        provider: str,
        model: str,
        timeout_seconds: int = 30,
        retry_count: int = 3,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.provider = provider
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.retry_count = retry_count
        self.api_key = api_key if api_key is not None else self._resolve_api_key()
        self.base_url = base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

    def _resolve_api_key(self) -> str | None:
        key_map = {
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
            "ollama": None,
        }
        env_key = key_map.get(self.provider.lower())
        return os.environ.get(env_key) if env_key else None

    def _model_string(self) -> str:
        """Return litellm model string, e.g. openai/gpt-4o-mini or ollama/llama2."""
        p = self.provider.lower()
        if p == "ollama":
            return f"ollama/{self.model}"
        if p == "openai":
            return f"openai/{self.model}"
        if p == "deepseek":
            return f"deepseek/{self.model}"
        if p == "claude":
            return f"anthropic/{self.model}"
        return f"{p}/{self.model}"

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        request_id: str | None = None,
        json_mode: bool = False,
    ) -> str:
        """
        Send messages to the LLM and return the content string.
        Retries with exponential backoff on transient failures.
        """
        request_id = request_id or str(uuid.uuid4())
        last_error: Exception | None = None
        for attempt in range(self.retry_count):
            try:
                kwargs: dict[str, Any] = {
                    "model": self._model_string(),
                    "messages": messages,
                    "timeout": self.timeout_seconds,
                }
                if self.base_url and self.provider.lower() == "ollama":
                    kwargs["api_base"] = self.base_url
                if self.api_key and self.provider.lower() != "ollama":
                    kwargs["api_key"] = self.api_key
                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                response = litellm.completion(**kwargs)
                content = response.choices[0].message.content or ""
                return content.strip()
            except Exception as e:
                last_error = e
                logger.warning(
                    "LLM call failed (attempt %s/%s), request_id=%s: %s",
                    attempt + 1,
                    self.retry_count,
                    request_id,
                    str(e),
                    exc_info=logger.isEnabledFor(logging.DEBUG),
                )
                if attempt < self.retry_count - 1:
                    backoff = 2**attempt
                    time.sleep(backoff)
        raise last_error or RuntimeError("LLM completion failed")

    def complete_json(
        self,
        messages: list[dict[str, str]],
        *,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        """Call complete with json_mode=True and parse result as JSON."""
        raw = self.complete(messages, request_id=request_id, json_mode=True)
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.error("LLM returned invalid JSON, request_id=%s: %s", request_id, e)
            raise ValueError(f"Invalid JSON from LLM: {e}") from e
