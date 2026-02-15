#!/usr/bin/env python3
"""
Run all hard-case queries via CLI (dry-run), collect results, then write QA_REPORT_OLLAMA_HARD_CASES.md.
Usage: python run_qa_hard.py [--timeout 180] [--max N]
"""
import json
import subprocess
import sys
from pathlib import Path

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent))
from qa_hard_cases import HARD_CASES

PROJECT_ROOT = Path(__file__).resolve().parent
RESULTS_JSON = PROJECT_ROOT / "qa_hard_results.json"
PYTHON = PROJECT_ROOT / ".venv" / "bin" / "python"
MAIN_PY = PROJECT_ROOT / "main.py"
DEFAULT_TIMEOUT = 180
MAX_DEFAULT = 100


def run_one(query: str, timeout: int | None) -> dict:
    """Run main.py --dry-run '<query>', return {exit_code, stdout, stderr, timeout_hit}. timeout=None = no limit."""
    kwargs = dict(
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if timeout is not None:
        kwargs["timeout"] = timeout
    try:
        r = subprocess.run(
            [str(PYTHON), str(MAIN_PY), "--dry-run", query],
            **kwargs,
        )
        return {
            "exit_code": r.returncode,
            "stdout": r.stdout or "",
            "stderr": r.stderr or "",
            "timeout_hit": False,
        }
    except subprocess.TimeoutExpired as e:
        return {
            "exit_code": -1,
            "stdout": (e.stdout or "") if isinstance(e.stdout, str) else "",
            "stderr": (e.stderr or "") if isinstance(e.stderr, str) else str(e),
            "timeout_hit": True,
        }
    except Exception as e:
        return {
            "exit_code": -2,
            "stdout": "",
            "stderr": str(e),
            "timeout_hit": False,
        }


def main(results_file: Path, report_path: Path, timeout: int | None, max_run: int, resume: bool) -> int:
    queries = HARD_CASES[:max_run]
    results = []
    if resume and results_file.exists():
        try:
            with open(results_file, encoding="utf-8") as f:
                results = json.load(f)
        except Exception:
            results = []

    start_idx = len(results)
    for i in range(start_idx, len(queries)):
        q = queries[i]
        print(f"[{i+1}/{len(queries)}] Running: {q[:55]}...", flush=True)
        out = run_one(q, timeout=timeout)
        out["query"] = q
        out["index"] = i + 1
        results.append(out)
        if out["timeout_hit"]:
            print("  -> TIMEOUT", flush=True)
        else:
            print(f"  -> exit {out['exit_code']}", flush=True)
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=0)

    report_title = None
    if "WITHOUT_TIMEOUT" in str(report_path):
        report_title = "QA Report - Ollama Hard Cases (100) - No Timeout"
    elif "TIMEOUT_600" in str(report_path):
        report_title = "QA Report - Ollama Hard Cases (100) - Timeout 600s"
    write_report(results, out_path=report_path, title=report_title)
    print(f"Done. Results in {results_file}, report in {report_path}")
    return 0


def write_report(results: list[dict], out_path: Path | None = None, title: str | None = None) -> None:
    """Generate report markdown from results list. Fills up to 100 with PENDING if needed."""
    out_path = out_path or PROJECT_ROOT / "QA_REPORT_OLLAMA_HARD_CASES.md"
    title = title or "QA Report - Ollama Hard Cases (100 Edge / Join / Complex)"
    # Build full list: results + PENDING for any of HARD_CASES not yet run
    by_idx = {r.get("index"): r for r in results if r.get("index")}
    full_list = []
    for i in range(1, len(HARD_CASES) + 1):
        if i in by_idx:
            full_list.append(by_idx[i])
        else:
            full_list.append({"index": i, "query": HARD_CASES[i - 1], "exit_code": None, "timeout_hit": False, "stdout": "", "stderr": "", "pending": True})
    results = full_list
    lines = [
        f"# {title}",
        "",
        "**Date:** 2026-02-15  ",
        "**Environment:** Ollama http://127.0.0.1:11434, model qwen2.5-coder:7b, dry-run  ",
        "**Retry:** 1  ",
    ]
    if title and "600" in title:
        lines.append("**Timeout per query:** 600s  ")
    lines.extend([
        "",
        "---",
        "",
        "## Summary",
        "",
        "| # | Query (abbrev) | Result | Exit | Timeout |",
        "|---|----------------|--------|------|---------|",
    ]
    passed = sum(1 for r in results if r.get("exit_code") == 0)
    failed = sum(1 for r in results if r.get("exit_code") not in (0, None) and not r.get("timeout_hit"))
    to_count = sum(1 for r in results if r.get("timeout_hit"))
    pending = sum(1 for r in results if r.get("pending"))
    for r in results:
        idx = r.get("index", 0)
        q = r.get("query", "")
        q_short = (q[:48] + "...") if len(q) > 48 else q
        q_short = q_short.replace("|", "\\|")
        code = r.get("exit_code") if r.get("exit_code") is not None else "-"
        to = "Yes" if r.get("timeout_hit") else "No"
        if r.get("pending"):
            res = "PENDING"
        else:
            res = "PASS" if code == 0 else ("TIMEOUT" if r.get("timeout_hit") else "FAIL")
        lines.append(f"| {idx} | {q_short} | {res} | {code} | {to} |")
    lines.extend([
        "",
        f"**Totals:** {len(results)} cases, {passed} PASS, {failed} FAIL, {to_count} TIMEOUT, {pending} PENDING",
        "",
        "---",
        "",
        "## Per-case: Query, Result, Logs (excerpt)",
        "",
    ])
    for r in results:
        idx = r.get("index", 0)
        q = r.get("query", "")
        code = r.get("exit_code")
        to = r.get("timeout_hit", False)
        if r.get("pending"):
            res = "PENDING"
        else:
            res = "PASS" if code == 0 else ("TIMEOUT" if to else "FAIL")
        stdout = (r.get("stdout") or "")[:1200]
        stderr = (r.get("stderr") or "")[:800]
        # Escape code blocks in markdown
        stdout = stdout.replace("```", "` ` `")
        stderr = stderr.replace("```", "` ` `")
        lines.append(f"### Case {idx}: {res}")
        lines.append("")
        lines.append(f"- **Query:** `{q}`")
        lines.append(f"- **Exit code:** {code if code is not None else '-'}  ")
        lines.append(f"- **Timeout:** {to}  ")
        lines.append("")
        if r.get("pending"):
            lines.append("*Not run yet.*")
        else:
            lines.append("<details>")
            lines.append("<summary>stdout (excerpt)</summary>")
            lines.append("")
            lines.append("```")
            lines.append(stdout.strip() or "(empty)")
            lines.append("```")
            lines.append("</details>")
            lines.append("")
            if stderr.strip():
                lines.append("<details>")
                lines.append("<summary>stderr (excerpt)</summary>")
                lines.append("")
                lines.append("```")
                lines.append(stderr.strip()[:800])
                lines.append("```")
                lines.append("</details>")
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="Per-query timeout seconds (ignored if --no-timeout)")
    p.add_argument("--no-timeout", action="store_true", help="No per-query timeout (infinite wait)")
    p.add_argument("--max", type=int, default=MAX_DEFAULT, help="Max number of queries to run")
    p.add_argument("--resume", action="store_true", help="Resume from existing results file")
    p.add_argument("--report", type=str, default="", help="Output report path (default: QA_REPORT_OLLAMA_HARD_CASES.md)")
    p.add_argument("--results-file", type=str, default="", help="Results JSON path (default: qa_hard_results.json)")
    p.add_argument("--report-only", action="store_true", help="Only generate report from existing results")
    args = p.parse_args()

    results_file = Path(args.results_file) if args.results_file else RESULTS_JSON
    report_path = Path(args.report) if args.report else PROJECT_ROOT / "QA_REPORT_OLLAMA_HARD_CASES.md"
    timeout = None if args.no_timeout else args.timeout

    if args.report_only:
        if not results_file.exists():
            print(f"No results file at {results_file}. Run without --report-only first.")
            sys.exit(1)
        with open(results_file, encoding="utf-8") as f:
            results = json.load(f)
        title = None
        if "WITHOUT_TIMEOUT" in str(report_path):
            title = "QA Report - Ollama Hard Cases (100) - No Timeout"
        elif "TIMEOUT_600" in str(report_path):
            title = "QA Report - Ollama Hard Cases (100) - Timeout 600s"
        write_report(results, out_path=report_path, title=title)
        sys.exit(0)

    sys.exit(main(results_file=results_file, report_path=report_path, timeout=timeout, max_run=min(args.max, len(HARD_CASES)), resume=args.resume))
