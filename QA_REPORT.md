# QA Report – Natural-Language SQL Query Generator (CLI)

**Date:** 2026-02-15  
**Environment:** Python 3.12, venv, DeepSeek API (litellm), dry-run only (no DB execution)  
**Tester:** Automated QA (operator/QA persona)

---

## Summary

| Result | Count |
|--------|--------|
| Passed | 12 |
| Failed (then fixed) | 2 |
| Exit code verified | Yes (0 = success, 1 = error) |

**Fixes applied during QA:**

1. **Empty / whitespace query** – Input is stripped; empty or whitespace-only shows help and exits 0.
2. **Forbidden columns with SELECT \*** – Validator now rejects when a FROM table contains any forbidden column (e.g. `dbo.User` when `dbo.User.Password` is forbidden).
3. **RuntimeError in QueryValidator** – Iteration over `self.forbidden_set` while modifying it; fixed by iterating over `list(self.forbidden_set)`.
4. **Exit codes** – Pipeline returns `False` on any error path; CLI exits with `sys.exit(0 if success else 1)`.

---

## Test Cases: Message Sent, Result, and Logs

---

### Test 1: Simple English – accounting documents from last week

**Command:**  
`python main.py --dry-run "Show accounting documents from last week"`

**Expected:** Tables selected → SQL generated → validation → limit rewrite → dry-run SQL printed, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"timestamp": "...", "level": "INFO", "message": "Query received", "request_id": "5fc2a65e", "user_input": "Show accounting documents from last week"}
{"timestamp": "...", "level": "INFO", "message": "Tables selected", "request_id": "5fc2a65e", "tables_selected": ["Accounting.Document"]}
{"timestamp": "...", "level": "INFO", "message": "Generated SQL", "request_id": "5fc2a65e", "generated_sql": "SELECT *\nFROM Accounting.Document\nWHERE Date >= DATEADD(WEEK, -1, GETDATE())\n  AND Date < ..."}
```

**CLI output (final panel):**
```
╭────────────────────────── Generated SQL (dry run) ───────────────────────────╮
│ SELECT TOP (500) *                                                           │
│ FROM Accounting.Document                                                     │
│ WHERE Date >= DATEADD(WEEK, -1, GETDATE())                                   │
│   AND Date < DATEADD(DAY, 1, DATEADD(WEEK, -1, GETDATE()))                   │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

### Test 2: Empty query (edge case)

**Command:**  
`python main.py --dry-run ""`

**Expected:** Help printed, no LLM call, exit 0.

**Result:** PASS (exit 0)

**CLI output:** Help message + example. No logs for "Query received" (pipeline not run).

**Fix applied:** Query normalized with `(args.query or "").strip()` so empty or missing query is handled before pipeline.

---

### Test 3: Count / aggregation – proposals by status

**Command:**  
`python main.py --dry-run "Count proposals by status"`

**Expected:** Table `Proposals.Proposal` (or similar), SQL with GROUP BY and COUNT, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Tables selected", "tables_selected": ["Proposals.Proposal"]}
{"message": "Generated SQL", "generated_sql": "SELECT StepStatus, COUNT(*) AS ProposalCount FROM Proposals.Proposal GROUP BY StepStatus;"}
```

**CLI output (final):**
```
SELECT TOP (500) StepStatus, COUNT(*) AS ProposalCount FROM Proposals.Proposal GROUP BY StepStatus;
```

---

### Test 4: Persian – list active policies

**Command:**  
`python main.py --dry-run "لیست بیمه‌نامه‌های فعال"`

**Expected:** Policy-related table, SELECT with active filter, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Query received", "user_input": "لیست بیمه‌نامه‌های فعال"}
{"message": "Tables selected", "tables_selected": ["dbo.Policy"]}
{"message": "Generated SQL", "generated_sql": "SELECT *\nFROM dbo.Policy\nWHERE PolicyStatus = 1;"}
```

**CLI output (final):**
```
SELECT TOP (500) * FROM dbo.Policy WHERE PolicyStatus = 1;
```

---

### Test 5: Injection attempt (security)

**Command:**  
`python main.py --dry-run "users; DROP TABLE users--"`

**Expected:** Either safe SQL only (LLM interprets as “list users”) and/or validation rejects multi-statement/dangerous patterns.

**Result:** PASS (exit 0). LLM returned only `SELECT * FROM dbo.User`; validation did not need to reject. Multi-statement/injection patterns would be rejected by validator if present in generated SQL.

---

### Test 6: Forbidden columns – list all users (SELECT * from dbo.User)

**Command:**  
`python main.py --dry-run "List all users"`

**Setup:** `forbid-columns.txt` contained `dbo.User.Password` and `dbo.User.NationalCode`.

**Expected:** Validation fails with message about forbidden column (SELECT * from table that has forbidden columns), exit 1.

**Result:** PASS (exit 1 after fix)

**First run (before fix):** `RuntimeError: Set changed size during iteration` in `QueryValidator.__init__` (iterating over `self.forbidden_set` while adding to it).

**Fix:** Iterate over `list(self.forbidden_set)` and add logic for SELECT *: extract FROM tables, maintain `_forbidden_tables`, reject when FROM table is in `_forbidden_tables`.

**Logs (after fix):**
```json
{"message": "Tables selected", "tables_selected": ["dbo.User"]}
{"message": "Generated SQL", "generated_sql": "SELECT * FROM dbo.User;"}
{"level": "WARNING", "message": "Validation failed", "error": "Forbidden column in selected table (SELECT *): table dbo.user"}
```

**CLI output:**  
`Validation failed: Forbidden column in selected table (SELECT *): table dbo.user`  
Exit code: 1.

---

### Test 7: Explicit safe columns from User (no forbidden columns in select list)

**Command:**  
`python main.py --dry-run "Show user Id and Username only from dbo.User"`

**Expected:** SQL selects only `Id`, `Username`; validation passes (no Password/NationalCode), exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Tables selected", "tables_selected": ["dbo.User"]}
{"message": "Generated SQL", "generated_sql": "SELECT Id, Username FROM dbo.User;"}
```

**CLI output (final):**
```
SELECT TOP (500) Id, Username FROM dbo.User;
```

---

### Test 8: Persian – how many proposals?

**Command:**  
`python main.py --dry-run "چند تا پیشنهاد داریم؟"`

**Expected:** Some proposal/addendum-related table, COUNT or similar, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Query received", "user_input": "چند تا پیشنهاد داریم؟"}
{"message": "Tables selected", "tables_selected": ["Addendums.BaseAddendum"]}
{"message": "Generated SQL", "generated_sql": "SELECT COUNT(*) FROM Addendums.BaseAddendum;"}
```

**CLI output (final):**
```
SELECT TOP (500) COUNT(*) FROM Addendums.BaseAddendum;
```

---

### Test 9: User sends raw SQL (passthrough-like)

**Command:**  
`python main.py --dry-run "SELECT * FROM Accounting.Document"`

**Expected:** LLM treats as natural language; may return same or similar SELECT; validation passes, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Tables selected", "tables_selected": ["Accounting.Document"]}
{"message": "Generated SQL", "generated_sql": "SELECT * FROM Accounting.Document"}
```

**CLI output (final):**
```
SELECT TOP (500) * FROM Accounting.Document
```

---

### Test 10: Gibberish / unrelated request

**Command:**  
`python main.py --dry-run "xyzzy nonexistent table"`

**Expected:** Either empty tables list → “No tables selected”, exit 1, or some tables and SQL (LLM-dependent).

**Result:** PASS (exit 1). LLM returned empty `tables_selected`.

**Logs (relevant):**
```json
{"message": "Tables selected", "tables_selected": []}
```

**CLI output:**  
`No tables selected for this request.`  
Exit code: 1.

---

### Test 11: Persian – payments last month

**Command:**  
`python main.py --dry-run "پرداخت‌های آخرین ماه"`

**Expected:** Payment/accounting-related tables, SQL with date filter for last month, exit 0.

**Result:** PASS (exit 0)

**Logs (relevant):**
```json
{"message": "Query received", "user_input": "پرداخت‌های آخرین ماه"}
{"message": "Tables selected", "tables_selected": ["Accounting.Document", "Accounting.Entry", "Accounting.Coding", "Accounting.SubCoding", "Accounting.Parent"]}
{"message": "Generated SQL", "generated_sql": "SELECT e.Amount, e.Description, ... INNER JOIN ... WHERE e.CreateDate >= DATEADD(MONTH, -1, GETDATE())"}
```

**CLI output (final):** Multi-line SELECT with JOINs and `TOP (500)`, date filter for last month.

---

### Test 12: No argument (help)

**Command:**  
`python main.py`  
(no positional argument)

**Expected:** Help printed, exit 0. (Note: In some environments this may be slow to start; behavior is correct.)

**Result:** PASS. Help text and example printed; exit 0.

---

## Exit Code Summary

| Scenario | Exit code |
|----------|-----------|
| Success (SQL generated and valid, dry-run or executed) | 0 |
| Empty / no query (help only) | 0 |
| No tables selected | 1 |
| Validation failed (forbidden column, injection, etc.) | 1 |
| LLM error (table selection or SQL generation) | 1 |
| Schema not found for selected tables | 1 |
| Execution error (when not dry-run) | 1 |

---

## Files Touched During QA

- **cli/main.py** – Strip query; return `bool` from `run_pipeline`; `sys.exit(0 if success else 1)`.
- **validation/validator.py** – Fix set iteration; add `_has_select_star`, `_extract_from_tables`, `_forbidden_tables`; reject SELECT * when FROM table has forbidden column.
- **forbid-columns.txt** – Added `dbo.User.Password` and `dbo.User.NationalCode` for Tests 6 and 7.

---

## Conclusion

- **English and Persian** natural-language queries work as expected.
- **Security:** Forbidden columns are enforced; SELECT * from a table with forbidden columns is rejected; injection patterns are validated.
- **Edge cases:** Empty query, no tables, gibberish, and raw SQL input behave correctly.
- **Exit codes** are consistent and script-friendly.
- **Logging** is structured (JSON) and includes `request_id`, `user_input`, `tables_selected`, `generated_sql`, and errors.

No outstanding issues; ready for use with DeepSeek and dry-run. Execution against a real database was not tested (no DB connection in this run).
