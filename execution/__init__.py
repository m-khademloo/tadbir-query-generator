"""Execution layer: read-only connection, timeout, row limit."""

from .executor import ExecutionResult, QueryExecutor, get_executor_from_config
from .renderer import render_result

__all__ = ["QueryExecutor", "ExecutionResult", "get_executor_from_config", "render_result"]
