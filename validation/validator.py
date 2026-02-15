"""Non-LLM validation: SELECT only, injection patterns, forbidden columns, structural checks."""

import re
from dataclasses import dataclass, field

import sqlparse
from sqlparse.sql import Statement, Token
from sqlparse.tokens import Keyword, DML


@dataclass
class ValidationResult:
    """Result of validating a SQL query."""

    valid: bool
    error_message: str = ""
    selected_columns: list[str] = field(default_factory=list)  # normalized table.column or column


# Patterns that indicate dangerous/injection attempts
INJECTION_PATTERNS = [
    re.compile(r";\s*(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|EXEC|EXECUTE)", re.IGNORECASE),
    re.compile(r"\bUNION\s+ALL\s+SELECT\s+.*\bFROM\s+(sys\.|information_schema\.)", re.IGNORECASE),
    re.compile(r"\bxp_\w+|sp_executesql|CHAR\s*\(\s*\d+", re.IGNORECASE),
]
# Configurable dangerous functions (can be extended via config)
DANGEROUS_FUNCTIONS = {"xp_cmdshell", "sp_executesql", "exec", "execute"}


def _normalize_identifier(s: str) -> str:
    """Remove brackets and strip."""
    return s.replace("[", "").replace("]", "").strip()


def _extract_selected_columns_from_parsed(parsed: list[Statement]) -> list[str]:
    """Extract column references from first SELECT (simple heuristic)."""
    columns: list[str] = []
    for stmt in parsed:
        tokens = stmt.tokens
        in_select_list = False
        for i, t in enumerate(tokens):
            if t.ttype is DML and _normalize_identifier(t.value).upper() == "SELECT":
                in_select_list = True
                continue
            if in_select_list:
                if t.ttype is Keyword and _normalize_identifier(t.value).upper() in ("FROM", "INTO"):
                    break
                # Collect identifiers (simple: word tokens before FROM)
                if hasattr(t, "value"):
                    val = _normalize_identifier(t.value)
                    if val and val.upper() not in ("AS", "SELECT", "DISTINCT", "TOP", "(", ")", ","):
                        if re.match(r"^[\w.]+$", val):
                            columns.append(val)
        break
    return columns


def _extract_columns_regex(sql: str) -> list[str]:
    """Fallback: extract possible table.column or column with regex."""
    # After SELECT ... FROM: we care about what's selected. Simple: find tokens that look like a.b or id
    seen = set()
    # Match qualified (a.b) or single word that could be column
    for m in re.finditer(r"\b([a-zA-Z_][\w.]*)\b", sql):
        s = m.group(1)
        if s.upper() in ("SELECT", "FROM", "WHERE", "JOIN", "ON", "AND", "OR", "AS", "TOP", "DISTINCT", "ORDER", "BY", "GROUP", "LEFT", "RIGHT", "INNER", "OUTER"):
            continue
        if "." in s or (s not in seen and len(s) < 50):
            seen.add(s)
    return list(seen)


def _has_select_star(sql: str) -> bool:
    """True if query has SELECT * or SELECT table.* (star in select list)."""
    return bool(re.search(r"\bSELECT\s+(\w+\.)?\*\s+FROM", sql, re.IGNORECASE | re.DOTALL))


def _extract_from_tables(sql: str) -> set[str]:
    """Extract normalized table names from FROM and JOIN clauses."""
    tables = set()
    # FROM [schema].[table] or schema.table or table
    for m in re.finditer(r"\b(?:FROM|JOIN)\s+\[?([\w.]+)\]?(?:\s+AS\s+\w+)?(?=\s+(?:ON|WHERE|JOIN|GROUP|ORDER|$|\s*;))", sql, re.IGNORECASE):
        tables.add(m.group(1).lower().replace("]", "").replace("[", ""))
    if not tables:
        # Simpler: FROM x or JOIN x
        for m in re.finditer(r"(?:FROM|JOIN)\s+([\w.]+)", sql, re.IGNORECASE):
            tables.add(m.group(1).lower())
    return tables


class QueryValidator:
    """Validates SQL before execution: type, injection, structure, forbidden columns."""

    def __init__(self, forbidden_columns: list[str]) -> None:
        """forbidden_columns: list of 'table.column' or 'schema.table.column' (normalized lower)."""
        self.forbidden_set = {c.strip().lower() for c in forbidden_columns if c.strip()}
        # Table names that contain a forbidden column (for SELECT * check)
        self._forbidden_tables: set[str] = set()
        for c in list(self.forbidden_set):
            parts = c.split(".")
            if len(parts) == 2:
                self.forbidden_set.add(parts[-1])
                self._forbidden_tables.add(parts[0])  # table
            elif len(parts) == 3:
                self.forbidden_set.add(f"{parts[1]}.{parts[2]}")
                self._forbidden_tables.add(f"{parts[0]}.{parts[1]}")  # schema.table

    def validate(self, sql: str) -> ValidationResult:
        """Run all checks. Returns ValidationResult with valid=True only if all pass."""
        sql_stripped = sql.strip()
        if not sql_stripped:
            return ValidationResult(valid=False, error_message="Empty query")

        # 1) Query type: must start with SELECT (allow leading whitespace)
        if not re.match(r"^\s*SELECT\b", sql_stripped, re.IGNORECASE):
            return ValidationResult(valid=False, error_message="Only SELECT queries are allowed")

        # 2) No multiple statements (semicolon followed by more content)
        if ";" in sql_stripped:
            parts = [p.strip() for p in sql_stripped.split(";") if p.strip()]
            if len(parts) > 1:
                return ValidationResult(valid=False, error_message="Multiple statements not allowed")

        # 3) Injection patterns
        for pat in INJECTION_PATTERNS:
            if pat.search(sql_stripped):
                return ValidationResult(valid=False, error_message="Query rejected by security policy (injection pattern)")

        # 4) Structural validation with sqlparse
        try:
            parsed = sqlparse.parse(sql_stripped)
        except Exception as e:
            return ValidationResult(valid=False, error_message=f"Invalid SQL syntax: {e}")
        if not parsed:
            return ValidationResult(valid=False, error_message="Could not parse SQL")
        first = parsed[0]
        # Ensure it's a SELECT (DML)
        dml = None
        for t in first.tokens:
            if t.ttype is DML:
                dml = _normalize_identifier(t.value).upper()
                break
        if dml != "SELECT":
            return ValidationResult(valid=False, error_message="Only SELECT is allowed")

        # 5) Extract selected columns and check forbidden
        try:
            selected = _extract_selected_columns_from_parsed(parsed)
        except Exception:
            selected = _extract_columns_regex(sql_stripped)
        if not selected:
            selected = _extract_columns_regex(sql_stripped)

        # 5a) SELECT *: if any FROM table has a forbidden column, reject
        if _has_select_star(sql_stripped) or not selected:
            from_tables = _extract_from_tables(sql_stripped)
            for tbl in from_tables:
                if tbl in self._forbidden_tables:
                    return ValidationResult(valid=False, error_message=f"Forbidden column in selected table (SELECT *): table {tbl}")

        for col_ref in selected:
            # Normalize: could be "col", "table.col", "schema.table.col"
            col_lower = col_ref.lower()
            if col_lower in self.forbidden_set:
                return ValidationResult(valid=False, error_message=f"Forbidden column referenced: {col_ref}")
            parts = col_lower.split(".")
            if len(parts) == 2 and parts[1] in self.forbidden_set:
                continue  # we already have table.col in forbidden_set in some form
            for fb in self.forbidden_set:
                if fb.endswith("." + col_lower) or fb == col_lower:
                    return ValidationResult(valid=False, error_message=f"Forbidden column referenced: {col_ref}")

        return ValidationResult(valid=True, selected_columns=selected)
