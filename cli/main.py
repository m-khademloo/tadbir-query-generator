"""CLI entry and main pipeline: natural language -> tables -> SQL -> validate -> limit -> execute -> render."""

import json
import re
import uuid
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

# Local imports
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import load_config, AppConfig
from schema import SchemaLoader, TableDescription
from llm import LLMClient
from prompts import PromptManager
from validation import QueryValidator, ValidationResult
from execution import QueryExecutor, get_executor_from_config, render_result, ExecutionResult
from app_logging import setup_logging, get_logger


def load_forbidden_columns(path: Path) -> list[str]:
    """Load forbid-columns.txt; one column per line, # comments ignored."""
    if not path.exists():
        return []
    lines = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                lines.append(line)
    return lines


def run_pipeline(
    user_input: str,
    config: AppConfig,
    *,
    dry_run: bool = False,
) -> bool:
    """Run the full pipeline and print results or errors. Returns True on success, False on error."""
    request_id = str(uuid.uuid4())[:8]
    log = get_logger("pipeline")
    console = Console()

    log.info(
        "Query received",
        extra={
            "request_id": request_id,
            "user_input": user_input,
        },
    )

    # Paths
    root = config.project_root
    tables_desc_path = root / config.tables_description_path
    schema_compressed_path = root / config.schema_compressed_path
    forbid_path = root / config.forbid_columns_path

    # 1) Schema loader
    schema_loader = SchemaLoader(tables_desc_path, schema_compressed_path)
    all_descriptions = schema_loader.load_table_descriptions()
    if not all_descriptions:
        console.print("[red]No table descriptions found. Check paths in config.[/red]")
        log.error("No table descriptions", extra={"request_id": request_id})
        return False

    tables_text = schema_loader.format_tables_text_for_prompt(all_descriptions)

    # 2) LLM: table selection
    llm_cfg = config.llm_settings
    llm = LLMClient(
        provider=llm_cfg.provider,
        model=llm_cfg.model,
        timeout_seconds=llm_cfg.timeout_seconds,
        retry_count=llm_cfg.retry_count,
        api_key=llm_cfg.api_key,
        base_url=llm_cfg.base_url,
    )
    pm = PromptManager()
    try:
        table_messages = pm.table_selection(user_input, tables_text)
        if config.log_prompts:
            log.debug("Table selection prompt", extra={"messages": str(table_messages)[:500]})
        table_response = llm.complete_json(table_messages, request_id=request_id)
    except Exception as e:
        log.exception("LLM table selection failed", extra={"request_id": request_id})
        console.print(f"[red]LLM error (table selection): {e}[/red]")
        return False

    table_names = table_response.get("tables") or []
    if not isinstance(table_names, list):
        table_names = [table_names] if table_names else []
    # Cap tables to avoid huge schema prompts (some local LLMs return too many)
    max_tables = 15
    if len(table_names) > max_tables:
        log.warning("Too many tables selected, capping to %s", max_tables, extra={"request_id": request_id, "count": len(table_names)})
        table_names = table_names[:max_tables]
    log.info("Tables selected", extra={"request_id": request_id, "tables_selected": table_names})

    if not table_names:
        console.print("[yellow]No tables selected for this request.[/yellow]")
        return False

    # 3) Load schema for selected tables
    table_infos = schema_loader.get_schema_for_tables(table_names)
    if not table_infos:
        console.print("[red]Could not load schema for selected tables.[/red]")
        return False
    schema_text = schema_loader.format_schema_text_for_prompt(table_infos)

    # 4) LLM: SQL generation
    try:
        sql_messages = pm.sql_generation(user_input, schema_text)
        if config.log_prompts:
            log.debug("SQL generation prompt", extra={"messages": str(sql_messages)[:500]})
        raw_sql = llm.complete(sql_messages, request_id=request_id)
    except Exception as e:
        log.exception("LLM SQL generation failed", extra={"request_id": request_id})
        console.print(f"[red]LLM error (SQL generation): {e}[/red]")
        return False

    # Normalize: extract only SQL (strip markdown code blocks if present)
    raw_sql = raw_sql.strip()
    if raw_sql.startswith("```"):
        raw_sql = re.sub(r"^```\w*\n?", "", raw_sql)
        raw_sql = re.sub(r"\n?```\s*$", "", raw_sql)
    generated_sql = raw_sql.strip()
    log.info("Generated SQL", extra={"request_id": request_id, "generated_sql": generated_sql[:200]})

    # 5) Validation (non-LLM)
    forbidden = load_forbidden_columns(forbid_path)
    validator = QueryValidator(forbidden)
    validation = validator.validate(generated_sql)
    if not validation.valid:
        log.warning("Validation failed", extra={"request_id": request_id, "error": validation.error_message})
        console.print(f"[red]Validation failed: {validation.error_message}[/red]")
        return False

    # Optional: LLM security validation (if you want double-check)
    # ...

    # 6) LLM: limit enforcement
    try:
        limit_messages = pm.limit_enforcement(generated_sql, config.max_rows)
        limited_sql = llm.complete(limit_messages, request_id=request_id)
        limited_sql = limited_sql.strip()
        if limited_sql.startswith("```"):
            limited_sql = re.sub(r"^```\w*\n?", "", limited_sql)
            limited_sql = re.sub(r"\n?```\s*$", "", limited_sql)
        final_sql = limited_sql.strip()
    except Exception as e:
        log.warning("Limit enforcement LLM failed, using original SQL", extra={"request_id": request_id})
        console.print(f"[yellow]Warning: Limit enforcement failed ({e}), using original SQL.[/yellow]")
        final_sql = generated_sql

    # Re-validate after limit rewrite
    validation2 = validator.validate(final_sql)
    if not validation2.valid:
        console.print(f"[red]Validation failed after limit rewrite: {validation2.error_message}[/red]")
        return False

    if dry_run:
        console.print(Panel(final_sql, title="Generated SQL (dry run)", border_style="blue"))
        return True

    # 7) Execute
    executor = get_executor_from_config(config)
    result = executor.execute(final_sql, request_id=request_id)
    log.info(
        "Query executed",
        extra={
            "request_id": request_id,
            "row_count": result.row_count,
            "execution_time": result.execution_time_seconds,
        },
    )
    if not result.success:
        console.print(f"[red]Execution error: {result.error_message}[/red]")
        return False

    # 8) Render
    render_result(result, show_time=True)
    return True


def run_cli() -> None:
    """Parse argv and run pipeline."""
    import argparse
    parser = argparse.ArgumentParser(description="Natural-language SQL query generator")
    parser.add_argument("query", nargs="?", help="Natural language query (or use -i)")
    parser.add_argument("--config", "-c", help="Path to config.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Only print generated SQL, do not execute")
    parser.add_argument("--verbose", "-v", action="store_true", help="Set log level to DEBUG")
    args = parser.parse_args()

    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)
    setup_logging(
        level="DEBUG" if args.verbose else config.log_level,
        structured=config.log_structured,
    )
    query = (args.query or "").strip()
    if not query:
        parser.print_help()
        print("\nExample: query-cli 'Show active users created last week'")
        sys.exit(0)

    success = run_pipeline(query, config, dry_run=args.dry_run)
    if not success:
        console = Console()
        console.print("[red]Error: pipeline failed.[/red]")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    run_cli()
