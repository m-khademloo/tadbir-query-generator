"""Structured logging for audit and observability."""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


def _structured_message(level: str, msg: str, **kwargs: Any) -> str:
    """Format as one-line JSON for structured logs."""
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": msg,
        **{k: v for k, v in kwargs.items() if v is not None},
    }
    return json.dumps(record, default=str)


class StructuredHandler(logging.Handler):
    """Handler that writes JSON lines to a stream."""

    def __init__(self, stream: Any = None) -> None:
        super().__init__()
        self.stream = stream or sys.stderr

    def emit(self, record: logging.LogRecord) -> None:
        try:
            extra = {k: v for k, v in record.__dict__.items() if k not in (
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "message", "taskName",
            )}
            msg = self.format(record)
            out = _structured_message(record.levelname, msg, **extra)
            self.stream.write(out + "\n")
            self.stream.flush()
        except Exception:
            self.handleError(record)


def setup_logging(
    level: str = "INFO",
    structured: bool = True,
) -> None:
    """Configure root logger with level and optional structured output."""
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))
    # Suppress noisy LiteLLM INFO logs (LLM prompts/results go to logs/ instead)
    logging.getLogger("LiteLLM").setLevel(logging.WARNING)
    if root.handlers:
        for h in root.handlers[:]:
            root.removeHandler(h)
    if structured:
        handler = StructuredHandler(sys.stderr)
        handler.setFormatter(logging.Formatter("%(message)s"))
        root.addHandler(handler)
    else:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Return a logger for the given module name."""
    return logging.getLogger(name)
