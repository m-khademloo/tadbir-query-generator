"""Load table descriptions and column schema for selected tables."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TableDescription:
    """One table from tables-description file: name, description, dependencies."""

    full_name: str  # e.g. Accounting.Document
    description: str
    depends_on: list[str] = field(default_factory=list)


@dataclass
class TableInfo:
    """Table with its column definitions (from compressed schema)."""

    full_name: str
    columns: list[tuple[str, str]]  # (column_name, type_str e.g. "int", "str")
    pk_column: Optional[str] = None
    fk_columns: dict[str, str] = field(default_factory=dict)  # col -> "Schema.Table.Col"


class SchemaLoader:
    """Loads table descriptions and extracts schema for given tables."""

    def __init__(
        self,
        tables_description_path: Path,
        schema_compressed_path: Path,
    ) -> None:
        self.tables_description_path = tables_description_path
        self.schema_compressed_path = schema_compressed_path
        self._descriptions: list[TableDescription] | None = None
        self._compressed_lines: list[str] | None = None

    def load_table_descriptions(self) -> list[TableDescription]:
        """Parse tables-description file into TableDescription list."""
        if self._descriptions is not None:
            return self._descriptions
        path = Path(self.tables_description_path)
        if not path.exists():
            self._descriptions = []
            return self._descriptions

        descriptions: list[TableDescription] = []
        current: dict[str, str | list[str]] = {}
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    if current.get("table"):
                        dep = current.get("depends on", "")
                        deps = [x.strip() for x in str(dep).split(",")] if dep else []
                        descriptions.append(
                            TableDescription(
                                full_name=current["table"].strip(),
                                description=(current.get("description") or "").strip(),
                                depends_on=[d for d in deps if d],
                            )
                        )
                    current = {}
                    continue
                if line.lower().startswith("table:"):
                    current["table"] = line[6:].strip()
                elif line.lower().startswith("description:"):
                    current["description"] = line[12:].strip()
                elif line.lower().startswith("depends on:"):
                    current["depends on"] = line[11:].strip()
            if current.get("table"):
                dep = current.get("depends on", "")
                deps = [x.strip() for x in str(dep).split(",")] if dep else []
                descriptions.append(
                    TableDescription(
                        full_name=current["table"].strip(),
                        description=(current.get("description") or "").strip(),
                        depends_on=[d for d in deps if d],
                    )
                )
        self._descriptions = descriptions
        return self._descriptions

    def _load_compressed_lines(self) -> list[str]:
        if self._compressed_lines is not None:
            return self._compressed_lines
        path = Path(self.schema_compressed_path)
        if not path.exists():
            self._compressed_lines = []
            return self._compressed_lines
        with open(path, encoding="utf-8") as f:
            self._compressed_lines = [line.rstrip() for line in f]
        return self._compressed_lines

    def get_schema_for_tables(self, table_names: list[str]) -> list[TableInfo]:
        """Return TableInfo for each table in table_names that exists in compressed schema."""
        lines = self._load_compressed_lines()
        name_set = {n.strip() for n in table_names if n.strip()}
        result: list[TableInfo] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("TABLE "):
                full_name = line[6:].strip()
                if full_name in name_set:
                    columns: list[tuple[str, str]] = []
                    pk_column: Optional[str] = None
                    fk_columns: dict[str, str] = {}
                    i += 1
                    while i < len(lines) and lines[i] and not lines[i].startswith("TABLE "):
                        col_line = lines[i]
                        # Format: "ColName type [PK] [FK->Schema.Table.Col]"
                        parts = col_line.split()
                        if len(parts) >= 2:
                            cname = parts[0]
                            ctype = parts[1]
                            columns.append((cname, ctype))
                            if "[PK]" in col_line:
                                pk_column = cname
                            if "[FK->" in col_line:
                                start = col_line.index("[FK->") + 5
                                end = col_line.index("]", start)
                                fk_columns[cname] = col_line[start:end]
                        i += 1
                    result.append(
                        TableInfo(
                            full_name=full_name,
                            columns=columns,
                            pk_column=pk_column,
                            fk_columns=fk_columns,
                        )
                    )
                    continue
            i += 1
        return result

    def format_tables_text_for_prompt(self, descriptions: list[TableDescription]) -> str:
        """Format table list with descriptions for the table-selection prompt."""
        blocks = []
        for t in descriptions:
            dep = ", ".join(t.depends_on) if t.depends_on else "none"
            blocks.append(f"table: {t.full_name}\ndescription: {t.description}\ndepends on: {dep}")
        return "\n\n".join(blocks)

    def format_schema_text_for_prompt(self, table_infos: list[TableInfo]) -> str:
        """Format schema (columns) for the SQL generation prompt."""
        lines = []
        for t in table_infos:
            lines.append(f"TABLE {t.full_name}")
            for cname, ctype in t.columns:
                pk = " [PK]" if cname == t.pk_column else ""
                fk = f" [FK->{t.fk_columns[cname]}]" if cname in t.fk_columns else ""
                lines.append(f"  {cname} {ctype}{pk}{fk}")
            lines.append("")
        return "\n".join(lines).strip()
