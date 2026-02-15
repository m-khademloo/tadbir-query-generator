"""Render query results as a CLI table (rich)."""

from typing import Any

from rich.console import Console
from rich.table import Table

from .executor import ExecutionResult


def render_result(result: ExecutionResult, *, show_time: bool = True) -> None:
    """Print result to stdout using rich Table."""
    console = Console()
    if not result.success:
        console.print(f"[red]Error:[/red] {result.error_message}")
        return
    if not result.columns:
        console.print("No columns returned.")
        return
    table = Table(show_header=True, header_style="bold")
    for col in result.columns:
        table.add_column(str(col))
    for row in result.rows:
        table.add_row(*[str(v) if v is not None else "" for v in row])
    console.print(table)
    console.print(f"[dim]Rows: {result.row_count}[/dim]")
    if show_time:
        console.print(f"[dim]Execution time: {result.execution_time_seconds:.2f}s[/dim]")
