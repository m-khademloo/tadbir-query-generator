#!/usr/bin/env python3
"""Compress SQL Server schema to LLM-friendly format: tables, columns, types, PK, FK only."""
import re
import sys

def norm_type(t):
    t = t.upper()
    if not t:
        return "str"
    if "INT" in t or "BIGINT" in t or "SMALLINT" in t or "TINYINT" in t:
        return "int"
    if "VARCHAR" in t or "NVARCHAR" in t or "CHAR" in t or "NCHAR" in t:
        if "MAX)" in t:
            return "text"
        return "str"
    if "TEXT" in t or "NTEXT" in t:
        return "text"
    if "BIT" in t:
        return "bool"
    if "DATETIME" in t or "TIMESTAMP" in t or "DATE" in t:
        return "datetime"
    if "DECIMAL" in t or "NUMERIC" in t or "FLOAT" in t or "REAL" in t:
        return "float"
    if "UNIQUEIDENTIFIER" in t:
        return "str"
    if "MONEY" in t:
        return "float"
    return "str"

def main():
    path = "lifecore.sql"
    out_path = "lifecore-compressed"
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # Collect FKs: (schema.table, column) -> (ref_schema.ref_table, ref_column)
    # Use (?:.(?!ALTER TABLE))*? so we don't match across ALTER TABLE boundaries
    fk_map = {}
    for m in re.finditer(
        r"ALTER TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s+(?:(?!ALTER TABLE).)*?FOREIGN KEY\s*\(\s*\[([^\]]+)\]\s*\)\s*REFERENCES\s*\[([^\]]+)\]\.\[([^\]]+)\]\s*\(\s*\[([^\]]+)\]\s*\)",
        content,
        re.IGNORECASE | re.DOTALL,
    ):
        tbl = f"{m.group(1)}.{m.group(2)}"
        col = m.group(3)
        ref_tbl = f"{m.group(4)}.{m.group(5)}"
        ref_col = m.group(6)
        fk_map[(tbl, col)] = f"{ref_tbl}.{ref_col}"

    # Parse CREATE TABLE blocks
    table_blocks = list(
        re.finditer(
            r"CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\)\s*ON\s*\[",
            content,
            re.IGNORECASE | re.DOTALL,
        )
    )
    # Some tables may end with ) ON [PRIMARY] without TEXTIMAGE
    if not table_blocks:
        table_blocks = list(
            re.finditer(
                r"CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\)\s*ON\s+\[PRIMARY\]",
                content,
                re.IGNORECASE | re.DOTALL,
            )
        )
    # Fallback: up to next ") ON " or "GO"
    if not table_blocks:
        table_blocks = list(
            re.finditer(
                r"CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\)\s*ON\s+",
                content,
                re.IGNORECASE | re.DOTALL,
            )
        )

    lines_out = []
    for block in table_blocks:
        schema_name = block.group(1)
        table_name = block.group(2)
        full_table = f"{schema_name}.{table_name}"
        body = block.group(3)

        # Find PRIMARY KEY columns
        pk_match = re.search(
            r"CONSTRAINT\s+\[[^\]]*\]\s+PRIMARY KEY[^(]*\(\s*\[([^\]]+)\](?:\s+ASC)?\s*\)",
            body,
            re.IGNORECASE,
        )
        pk_col = pk_match.group(1) if pk_match else None
        if not pk_match:
            pk_match = re.search(r"PRIMARY KEY\s*\(\s*\[([^\]]+)\]", body, re.IGNORECASE)
            pk_col = pk_match.group(1) if pk_match else None

        # Column lines: [Name] [type] ...
        col_re = re.compile(r"\[\s*([^\]]+)\s*\]\s*\[\s*([^\]]+)\s*\]", re.IGNORECASE)
        columns = []
        for line in body.split("\n"):
            line = line.strip()
            if not line or line.startswith("CONSTRAINT") or line.startswith(")"):
                continue
            m = col_re.match(line)
            if m:
                cname = m.group(1).strip()
                ctype = m.group(2).strip()
                if cname == pk_col and "PRIMARY" in body and "CONSTRAINT" in body:
                    continue
                columns.append((cname, ctype))

        # If we skipped PK column above (because it's in CONSTRAINT block), ensure it's first in list
        # Actually we parse column definitions only; PK might be (Id) and we have [Id] [int] in columns
        if pk_col and not any(c[0] == pk_col for c in columns):
            pk_type = "int"
            for c, t in columns:
                if c.lower() == "id":
                    pk_type = norm_type(t)
                    break
            columns.insert(0, (pk_col, pk_type))

        lines_out.append(f"TABLE {full_table}")
        for cname, raw_type in columns:
            short_type = norm_type(raw_type)
            pk_tag = " [PK]" if cname == pk_col else ""
            fk_tag = ""
            key = (full_table, cname)
            if key in fk_map:
                fk_tag = f" [FK->{fk_map[key]}]"
            lines_out.append(f"{cname} {short_type}{pk_tag}{fk_tag}")
        lines_out.append("")

    # Tables without CONSTRAINT PRIMARY KEY (e.g. proTemp): body has no CONSTRAINT block
    # Re-parse to catch tables that end with ) ON [PRIMARY] only
    alt_blocks = re.finditer(
        r"CREATE TABLE \[([^\]]+)\]\.\[([^\]]+)\]\s*\((.*?)\)\s*\)\s* ON",
        content,
        re.IGNORECASE | re.DOTALL,
    )
    seen = {m.group(1) + "." + m.group(2) for m in table_blocks}
    for block in alt_blocks:
        full = f"{block.group(1)}.{block.group(2)}"
        if full in seen:
            continue
        seen.add(full)
        body = block.group(3)
        pk_match = re.search(r"PRIMARY KEY[^(]*\(\s*\[([^\]]+)\]", body, re.IGNORECASE)
        pk_col = pk_match.group(1) if pk_match else None
        col_re = re.compile(r"\[\s*([^\]]+)\s*\]\s*\[\s*([^\]]+)\s*\]", re.IGNORECASE)
        columns = []
        for line in body.split("\n"):
            line = line.strip()
            if not line or line.startswith("CONSTRAINT") or line.startswith(")"):
                continue
            m = col_re.match(line)
            if m:
                columns.append((m.group(1).strip(), m.group(2).strip()))
        if columns:
            lines_out.append(f"TABLE {full}")
            for cname, raw_type in columns:
                pk_tag = " [PK]" if cname == pk_col else ""
                fk_tag = f" [FK->{fk_map[(full, cname)]}]" if (full, cname) in fk_map else ""
                lines_out.append(f"{cname} {norm_type(raw_type)}{pk_tag}{fk_tag}")
            lines_out.append("")

    with open(out_path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines_out))

    print(f"Wrote {out_path}", file=sys.stderr)
    print(f"Tables: {len(seen)}", file=sys.stderr)

if __name__ == "__main__":
    main()
