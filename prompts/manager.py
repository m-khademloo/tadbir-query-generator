"""Prompt manager: table selection, SQL generation, security check, limit enforcement."""

from .templates import (
    LIMIT_ENFORCEMENT_PROMPT,
    SECURITY_VALIDATION_PROMPT,
    SQL_GENERATION_PROMPT,
    TABLE_SELECTION_PROMPT,
)


class PromptManager:
    """Builds prompts for each pipeline step."""

    @staticmethod
    def table_selection(user_request: str, tables_text: str) -> list[dict[str, str]]:
        """Prompt for LLM to select relevant tables."""
        return [
            {"role": "system", "content": TABLE_SELECTION_PROMPT},
            {"role": "user", "content": f"User request: {user_request}\n\n{tables_text}\n\nReturn only a JSON object with key \"tables\" (array of full table names, e.g. [\"Accounting.Document\", \"dbo.User\"]). No other text."},
        ]

    @staticmethod
    def sql_generation(user_request: str, schema_text: str) -> list[dict[str, str]]:
        """Prompt for LLM to generate a single SELECT query."""
        return [
            {"role": "system", "content": SQL_GENERATION_PROMPT},
            {"role": "user", "content": f"User request: {user_request}\n\nSchema:\n{schema_text}\n\nReturn only the SQL SELECT statement. No comments, no explanations."},
        ]

    @staticmethod
    def security_validation(sql: str, forbidden_columns: list[str]) -> list[dict[str, str]]:
        """Prompt for LLM to check SQL against forbidden columns and suggest fix."""
        forbid_list = "\n".join(forbidden_columns) if forbidden_columns else "(none)"
        json_desc = '{"approved": true|false, "reason": "...", "corrected_sql": "..." (only if approved is false)}'
        return [
            {"role": "system", "content": SECURITY_VALIDATION_PROMPT},
            {"role": "user", "content": f"SQL to check:\n{sql}\n\nForbidden columns:\n{forbid_list}\n\nReturn JSON: {json_desc}."},
        ]

    @staticmethod
    def limit_enforcement(sql: str, max_rows: int = 500) -> list[dict[str, str]]:
        """Prompt for LLM to add TOP/LIMIT and avoid full scans where possible."""
        content = LIMIT_ENFORCEMENT_PROMPT.format(max_rows=max_rows)
        return [
            {"role": "system", "content": content},
            {"role": "user", "content": f"SQL:\n{sql}\n\nReturn only the modified SQL. Use TOP ({max_rows}) for SQL Server. No comments."},
        ]
