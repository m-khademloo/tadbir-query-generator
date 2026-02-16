"""Per-run LLM prompt and result logging to a file in logs/."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _format_messages(messages: list[dict[str, str]]) -> str:
    """Format messages for human-readable log (role: content)."""
    lines = []
    for m in messages:
        role = m.get("role", "?")
        content = m.get("content", "")
        lines.append(f"[{role}]\n{content}")
    return "\n\n".join(lines)


def get_run_log_path(request_id: str, logs_dir: Path | None = None) -> Path:
    """Return path for this run's LLM log file. Creates logs_dir if needed. Uses prefix 1-, 2-, 3- by existing file count."""
    base = logs_dir or Path.cwd() / "logs"
    base.mkdir(parents=True, exist_ok=True)
    # Count existing LLM log files (*.txt) to get next run number
    existing = list(base.glob("*.txt"))
    run_number = len(existing) + 1
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    return base / f"{run_number}-llm_{request_id}_{ts}.txt"


def write_run_header(
    log_path: Path,
    request_id: str,
    user_input: str,
) -> None:
    """Write run header (request_id, user_input, timestamp) to the log file."""
    ts = datetime.now(timezone.utc).isoformat()
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"request_id: {request_id}\n")
        f.write(f"user_input: {user_input}\n")
        f.write(f"timestamp: {ts}\n")
        f.write("\n")


def append_llm_step(
    log_path: Path,
    step_name: str,
    messages: list[dict[str, str]],
    result: str | dict[str, Any],
) -> None:
    """Append one LLM step (prompt + result) to the run log file."""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write(f"STEP: {step_name}\n")
        f.write("=" * 80 + "\n\n")
        f.write("--- PROMPT (messages) ---\n\n")
        f.write(_format_messages(messages))
        f.write("\n\n--- RESULT ---\n\n")
        if isinstance(result, dict):
            f.write(json.dumps(result, indent=2, default=str))
        else:
            f.write(result)
        f.write("\n\n")
