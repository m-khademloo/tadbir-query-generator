"""Load configuration from YAML and environment variables."""

from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConnectionConfig(BaseSettings):
    """Database connection settings."""

    model_config = SettingsConfigDict(env_prefix="DB_", extra="ignore")

    driver: str = Field(default="ODBC Driver 18 for SQL Server", description="ODBC driver name")
    server: str = Field(default="localhost", description="Server hostname")
    database: str = Field(default="CoreInsurance-Dev", description="Database name")
    trusted_connection: bool = Field(default=False, description="Use Windows auth")
    connection_string: str | None = Field(default=None, description="Full connection string; overrides other fields")
    user: str | None = Field(default=None, description="Username (if not trusted)")
    password: str | None = Field(default=None, description="Password (use env DB_PASSWORD)")


class LLMSettings(BaseSettings):
    """LLM provider and model settings."""

    model_config = SettingsConfigDict(env_prefix="LLM_", extra="ignore")

    provider: str = Field(default="openai", description="openai | deepseek | claude | ollama")
    model: str = Field(default="gpt-4o-mini", description="Model name")
    timeout_seconds: int = Field(default=30, ge=1, le=300)
    retry_count: int = Field(default=3, ge=1, le=10)
    api_key: str | None = Field(default=None, description="API key (use env OPENAI_API_KEY etc.)")
    base_url: str | None = Field(default=None, description="Ollama/custom base URL (OLLAMA_BASE_URL)")


class AppConfig(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Paths (resolved relative to project root if not absolute)
    project_root: Path = Field(default_factory=lambda: Path.cwd())
    schema_sql_path: str = Field(default="lifecore.sql")
    schema_compressed_path: str = Field(default="lifecore-compressed")
    tables_description_path: str = Field(default="lifecore-tables-description.txt")
    forbid_columns_path: str = Field(default="forbid-columns.txt")

    # Query safety
    max_rows: int = Field(default=500, ge=1, le=10_000)
    timeout_seconds: int = Field(default=30, ge=1, le=300)

    # Logging
    log_level: str = Field(default="INFO")
    log_structured: bool = Field(default=True)
    log_prompts: bool = Field(default=False)

    # Nested configs (loaded from YAML; env overrides applied via model_config)
    db_connection: DBConnectionConfig = Field(default_factory=DBConnectionConfig)
    llm_settings: LLMSettings = Field(default_factory=LLMSettings)

    def resolve_path(self, path_key: str) -> Path:
        """Resolve a path config key to an absolute Path."""
        value = getattr(self, path_key)
        p = Path(value)
        if not p.is_absolute():
            p = self.project_root / p
        return p


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Merge override into base (override wins)."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(
    config_path: str | Path | None = None,
    project_root: Path | None = None,
) -> AppConfig:
    """Load configuration from YAML file and environment. Env takes precedence."""
    root = project_root or Path.cwd()
    # Load .env so DEEPSEEK_API_KEY, LLM_*, DB_* etc. are available
    try:
        from dotenv import load_dotenv
        load_dotenv(root / ".env")
    except ImportError:
        pass
    config_path = config_path or root / "config" / "config.yaml"

    file_config: dict[str, Any] = {}
    if Path(config_path).exists():
        with open(config_path, encoding="utf-8") as f:
            file_config = yaml.safe_load(f) or {}

    # Nested configs: load from env first (BaseSettings), then override with file
    db_file = file_config.get("db_connection", {})
    llm_file = file_config.get("llm_settings", {})
    db = DBConnectionConfig()
    for k, v in db_file.items():
        if hasattr(db, k):
            setattr(db, k, v)
    llm = LLMSettings()
    for k, v in llm_file.items():
        if hasattr(llm, k):
            setattr(llm, k, v)

    config_dict = {
        "project_root": root,
        "schema_sql_path": file_config.get("schema_sql_path", "lifecore.sql"),
        "schema_compressed_path": file_config.get("schema_compressed_path", "lifecore-compressed"),
        "tables_description_path": file_config.get("tables_description_path", "lifecore-tables-description.txt"),
        "forbid_columns_path": file_config.get("forbid_columns_path", "forbid-columns.txt"),
        "max_rows": file_config.get("max_rows", 500),
        "timeout_seconds": file_config.get("timeout_seconds", 30),
        "log_level": file_config.get("log_level", "INFO"),
        "log_structured": file_config.get("log_structured", True),
        "log_prompts": file_config.get("log_prompts", False),
        "db_connection": db,
        "llm_settings": llm,
    }
    return AppConfig(**config_dict)
