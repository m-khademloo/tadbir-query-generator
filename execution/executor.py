"""Execute validated SELECT with timeout and row limit."""

import logging
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of running a query."""

    success: bool
    columns: list[str] = field(default_factory=list)
    rows: list[tuple[Any, ...]] = field(default_factory=list)
    row_count: int = 0
    execution_time_seconds: float = 0.0
    error_message: str = ""


class QueryExecutor:
    """Executes SELECT queries with connection pooling and timeout."""

    def __init__(
        self,
        connection_string: str | None = None,
        driver: str = "ODBC Driver 18 for SQL Server",
        server: str = "localhost",
        database: str = "CoreInsurance-Dev",
        user: str | None = None,
        password: str | None = None,
        trusted_connection: bool = False,
        timeout_seconds: int = 30,
        max_rows: int = 500,
    ) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_rows = max_rows
        self._connection_string = connection_string
        self._driver = driver
        self._server = server
        self._database = database
        self._user = user
        self._password = password
        self._trusted_connection = trusted_connection
        self._conn = None

    def _build_connection_string(self) -> str:
        if self._connection_string:
            return self._connection_string
        parts = [
            f"DRIVER={{{self._driver}}}",
            f"SERVER={self._server}",
            f"DATABASE={self._database}",
        ]
        if self._trusted_connection:
            parts.append("Trusted_Connection=yes")
        elif self._user:
            parts.append(f"UID={self._user}")
            if self._password:
                parts.append(f"PWD={self._password}")
        return ";".join(parts)

    def execute(self, sql: str, request_id: str | None = None) -> ExecutionResult:
        """
        Execute the SELECT query. Enforces max_rows via TOP if not present.
        Returns ExecutionResult with columns, rows, timing.
        """
        import pyodbc

        sql = self._ensure_row_limit(sql)
        conn_str = self._build_connection_string()
        start = time.perf_counter()
        try:
            conn = pyodbc.connect(conn_str, timeout=self.timeout_seconds)
            conn.timeout = self.timeout_seconds
            cursor = conn.cursor()
            cursor.execute(sql)
            columns = [d[0] for d in cursor.description] if cursor.description else []
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            elapsed = time.perf_counter() - start
            return ExecutionResult(
                success=True,
                columns=columns,
                rows=[tuple(r) for r in rows],
                row_count=len(rows),
                execution_time_seconds=elapsed,
            )
        except Exception as e:
            elapsed = time.perf_counter() - start
            logger.error("Query execution failed, request_id=%s: %s", request_id, e, exc_info=True)
            return ExecutionResult(
                success=False,
                error_message=str(e),
                execution_time_seconds=elapsed,
            )

    def _ensure_row_limit(self, sql: str) -> str:
        """If SQL does not contain TOP (n) or LIMIT n, add TOP (max_rows) for SQL Server."""
        import re
        if re.search(r"\bTOP\s*\(\s*\d+\s*\)", sql, re.IGNORECASE):
            return sql
        if re.search(r"\bLIMIT\s+\d+", sql, re.IGNORECASE):
            return sql
        # Insert TOP (max_rows) after SELECT [DISTINCT]
        sql_stripped = sql.strip()
        if re.match(r"^\s*SELECT\s+", sql_stripped, re.IGNORECASE):
            insert = f"TOP ({self.max_rows}) "
            new_sql = re.sub(r"(\s*SELECT\s+)(?!TOP\s)", r"\1" + insert, sql_stripped, count=1, flags=re.IGNORECASE)
            return new_sql
        return sql


def get_executor_from_config(config: Any) -> QueryExecutor:
    """Build QueryExecutor from AppConfig."""
    db = config.db_connection
    return QueryExecutor(
        connection_string=db.connection_string,
        driver=db.driver,
        server=db.server,
        database=db.database,
        user=db.user,
        password=db.password,
        trusted_connection=db.trusted_connection,
        timeout_seconds=config.timeout_seconds,
        max_rows=config.max_rows,
    )
