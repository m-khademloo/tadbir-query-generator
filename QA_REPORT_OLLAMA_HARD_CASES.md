# QA Report - Ollama Hard Cases (100 Edge / Join / Complex)

**Date:** 2026-02-15  
**Environment:** Ollama http://127.0.0.1:11434, model qwen2.5-coder:7b, dry-run  
**Retry:** 1, **Timeout per query:** 55-180s (configurable)  

**How to run all 100:** `python run_qa_hard.py --max 100 --timeout 90 --resume` (persists after each run).  
**Refresh report:** `python run_qa_hard.py --report-only` (reads `qa_hard_results.json`).

---

## Summary

| # | Query (abbrev) | Result | Exit | Timeout |
|---|----------------|--------|------|---------|
| 1 | Show accounting documents with their entries and... | PASS | 0 | No |
| 2 | List proposals with their insured risks and insu... | TIMEOUT | -1 | Yes |
| 3 | Users and their roles with role name | PASS | 0 | No |
| 4 | Accounting document with parent and related docu... | TIMEOUT | -1 | Yes |
| 5 | Proposals joined to persons and proposal states | TIMEOUT | -1 | Yes |
| 6 | Payments with payment file and user who created | TIMEOUT | -1 | Yes |
| 7 | Documents with amendment requests and confirm us... | TIMEOUT | -1 | Yes |
| 8 | Addendums with base addendum and linked proposal... | TIMEOUT | -1 | Yes |
| 9 | Entries with document, coding and subcoding | TIMEOUT | -1 | Yes |
| 10 | Policy with beneficiary and insurer | PASS | 0 | No |
| 11 | Documents created in last 7 days where type is 1... | TIMEOUT | -1 | Yes |
| 12 | Proposals with status between 1 and 5 created af... | TIMEOUT | -1 | Yes |
| 13 | Users active and not deleted with email containi... | TIMEOUT | -1 | Yes |
| 14 | Accounting entries where amount greater than 100... | TIMEOUT | -1 | Yes |
| 15 | Policies that are active and have premium paymen... | PASS | 0 | No |
| 16 | Proposals by status with count greater than 10 | PASS | 0 | No |
| 17 | Documents where reference number is not null ord... | PASS | 0 | No |
| 18 | Users who have logged in in the last 30 days | TIMEOUT | -1 | Yes |
| 19 | Entries grouped by coding with sum of amount | PENDING | - | No |
| 20 | Addendums of type beneficiary change in last qua... | PENDING | - | No |
| 21 | Count of proposals per status | PENDING | - | No |
| 22 | Sum of amounts by document type in accounting | PENDING | - | No |
| 23 | Average premium by insurance plan | PENDING | - | No |
| 24 | Max and min date of documents per year | PENDING | - | No |
| 25 | Count distinct users per role | PENDING | - | No |
| 26 | Total entries per coding code | PENDING | - | No |
| 27 | Number of addendums per base addendum type | PENDING | - | No |
| 28 | Count policies grouped by status and plan | PENDING | - | No |
| 29 | Sum of payment amounts by month | PENDING | - | No |
| 30 | Count documents by parent and type | PENDING | - | No |
| 31 | Ù„ÛŒØ³Øª Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯Ù‡Ø§ÛŒ ØªØ§ÛŒÛŒØ¯ Ø´Ø¯Ù‡ | PENDING | - | No |
| 32 | ØªØ¹Ø¯Ø§Ø¯ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ù�Ø¹Ø§Ù„ | PENDING | - | No |
| 33 | Ø³Ù†Ø¯Ù‡Ø§ÛŒ Ø­Ø³Ø§Ø¨Ø¯Ø§Ø±ÛŒ Ù‡Ù�ØªÙ‡ Ú¯Ø°Ø´ØªÙ‡ | PENDING | - | No |
| 34 | Ø¨ÛŒÙ…Ù‡â€ŒÙ†Ø§Ù…Ù‡â€ŒÙ‡Ø§ÛŒ Ù…Ù†Ù‚Ø¶ÛŒ Ø´Ø¯Ù‡ | PENDING | - | No |
| 35 | Ù¾Ø±Ø¯Ø§Ø®Øªâ€ŒÙ‡Ø§ÛŒ Ù…ÙˆÙ�Ù‚ Ø¢Ø®Ø±ÛŒÙ† Ù…Ø§Ù‡ | PENDING | - | No |
| 36 | Ú¯Ø²Ø§Ø±Ø´ Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ø¨Ù‡ ØªÙ�Ú©ÛŒÚ© ÙˆØ¶Ø¹ÛŒØª | PENDING | - | No |
| 37 | Ø§Ù�Ø±Ø§Ø¯ Ø¨Ø§ Ú©Ø¯ Ù…Ù„ÛŒ Ø®Ø§Ù„ÛŒ | PENDING | - | No |
| 38 | Ú†Ù†Ø¯ ØªØ§ Ø³Ù†Ø¯ Ø§ØµÙ„Ø§Ø­ÛŒÙ‡ Ø¯Ø§Ø±ÛŒÙ… | PENDING | - | No |
| 39 | Ù„ÛŒØ³Øª Ù†Ù‚Ø´â€ŒÙ‡Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±ÛŒ | PENDING | - | No |
| 40 | Ù…Ø¬Ù…ÙˆØ¹ Ù…Ø¨Ø§Ù„Øº Ø¨Ù‡ ØªÙ�Ú©ÛŒÚ© Ù†ÙˆØ¹ Ø³Ù†Ø¯ | PENDING | - | No |
| 41 | Show me everything from last week | PENDING | - | No |
| 42 | Give me reports | PENDING | - | No |
| 43 | What do we have | PENDING | - | No |
| 44 | List data | PENDING | - | No |
| 45 | Summary | PENDING | - | No |
| 46 | All of them | PENDING | - | No |
| 47 | Recent stuff | PENDING | - | No |
| 48 | Important records | PENDING | - | No |
| 49 | Things that need attention | PENDING | - | No |
| 50 | Whatever is active | PENDING | - | No |
| 51 | I need a list of all accounting documents that w... | PENDING | - | No |
| 52 | Show proposals that are in status approved or pe... | PENDING | - | No |
| 53 | List every user with their username and email an... | PENDING | - | No |
| 54 | Accounting entries joined to their document and ... | PENDING | - | No |
| 55 | I want to see addendums of type beneficiary chan... | PENDING | - | No |
| 56 | Documents where type = 1 | PENDING | - | No |
| 57 | Select * from Accounting.Document where Date > '... | PENDING | - | No |
| 58 | User's list | PENDING | - | No |
| 59 | Proposals (active only) | PENDING | - | No |
| 60 | Count(*) from Document | PENDING | - | No |
| 61 | List users where id is 1 | PENDING | - | No |
| 62 | Show documents; comment | PENDING | - | No |
| 63 | Proposals where status in (1,2,3) | PENDING | - | No |
| 64 | Users order by Id | PENDING | - | No |
| 65 | Select Id from Accounting.Document | PENDING | - | No |
| 66 | acounting documnts | PENDING | - | No |
| 67 | proposlas by statu | PENDING | - | No |
| 68 | usrs and roels | PENDING | - | No |
| 69 | lisr of polocies | PENDING | - | No |
| 70 | docuemnts form last weak | PENDING | - | No |
| 71 | Documents from 2024-06-01 to 2024-06-30 | PENDING | - | No |
| 72 | Proposals created on 2025-01-15 | PENDING | - | No |
| 73 | Users with more than 5 logins | PENDING | - | No |
| 74 | Entries with amount between 100 and 500 | PENDING | - | No |
| 75 | Policies expiring in next 30 days | PENDING | - | No |
| 76 | Documents that are not type 0 | PENDING | - | No |
| 77 | Users who are not deleted | PENDING | - | No |
| 78 | Proposals not in draft status | PENDING | - | No |
| 79 | Entries without a linked subcoding | PENDING | - | No |
| 80 | Policies that do not have addendums | PENDING | - | No |
| 81 | Documents that have at least one entry with amou... | PENDING | - | No |
| 82 | Proposals that have insured risks and are in app... | PENDING | - | No |
| 83 | Users who have a role and are active | PENDING | - | No |
| 84 | Accounting documents with parent type 1 or no pa... | PENDING | - | No |
| 85 | Addendums linked to proposal insured risk where ... | PENDING | - | No |
| 86 | Top 10 documents by date with their entry count | PENDING | - | No |
| 87 | Proposals with their person name and state name ... | PENDING | - | No |
| 88 | Users with role, last login date, and count of o... | PENDING | - | No |
| 89 | Documents with parent reference and related docu... | PENDING | - | No |
| 90 | Payments grouped by user and by month with total... | PENDING | - | No |
| 91 | Policies with plan name and beneficiary count | PENDING | - | No |
| 92 | Entries with document reference and coding title... | PENDING | - | No |
| 93 | Addendums with base addendum date and type descr... | PENDING | - | No |
| 94 | Full join of document and entry and coding | PENDING | - | No |
| 95 | Proposals with person and state and plan and ins... | PENDING | - | No |
| 96 | Sum of debit and credit by document and coding | PENDING | - | No |
| 97 | Users with no role assigned | PENDING | - | No |
| 98 | Ø¢Ø®Ø±ÛŒÙ† Ù¾Ø±Ø¯Ø§Ø®Øª Ù‡Ø± Ú©Ø§Ø±Ø¨Ø± | PENDING | - | No |
| 99 | Documents with more than 10 entries | PENDING | - | No |
| 100 | Proposals created yesterday with person name | PENDING | - | No |

**Totals:** 100 cases, 6 PASS, 0 FAIL, 12 TIMEOUT, 82 PENDING

---

## Per-case: Query, Result, Logs (excerpt)

### Case 1: PASS

- **Query:** `Show accounting documents with their entries and coding, joined`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500)                                                             â”‚
â”‚     d.Id AS DocumentId,                                                      â”‚
â”‚     d.ReferenceNumber,                                                       â”‚
â”‚     d.Date,                                                                  â”‚
â”‚     d.Type,                                                                  â”‚
â”‚     d.ParentId,                                                              â”‚
â”‚     d.RelatedDocumentId,                                                     â”‚
â”‚     d.RelatedDocumentType,                                                   â”‚
â”‚     c.Title AS CategoryTitle,                                                â”‚
â”‚     c.DisplayOrder,                                                          â”‚
â”‚     c.Published,                                                             â”‚
â”‚     c.CreateDate AS CategoryCreateDate,                                      â”‚
â”‚     c.UpdateDate AS CategoryUpdateDate,                                      â”‚
â”‚     c.Description
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:30:05.031407+00:00", "level": "INFO", "message": "Query received", "request_id": "e3d4c93e", "user_input": "Show accounting documents with their entries and coding, joined"}
[92m00:00:05 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:30:05.038845+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:00:05"}
[92m00:01:03 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:31:03.146165+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:01:03"}
{"timestamp": "2026-02-15T20:31:03.225216+00:00", "level": "
```
</details>

### Case 2: TIMEOUT

- **Query:** `List proposals with their insured risks and insurance plan names`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'List proposals with their insured risks and insurance plan names']' timed out after 120 seconds
```
</details>

### Case 3: PASS

- **Query:** `Users and their roles with role name`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500)                                                             â”‚
â”‚     u.Id AS UserId,                                                          â”‚
â”‚     u.Username AS UserName,                                                  â”‚
â”‚     r.RoleName                                                               â”‚
â”‚ FROM                                                                         â”‚
â”‚     dbo.User u                                                               â”‚
â”‚ JOIN                                                                         â”‚
â”‚     UserRoles ur ON u.Id = ur.UserId                                         â”‚
â”‚ JOIN                                                                         â”‚
â”‚     Roles r ON ur.RoleId = r.Id;                                             â”‚
â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•¯
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:33:16.061624+00:00", "level": "INFO", "message": "Query received", "request_id": "5cba1095", "user_input": "Users and their roles with role name"}
[92m00:03:16 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:33:16.070220+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:03:16"}
[92m00:03:22 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:33:22.114091+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:03:22"}
{"timestamp": "2026-02-15T20:33:22.199318+00:00", "level": "INFO", "message": "Tables s
```
</details>

### Case 4: TIMEOUT

- **Query:** `Accounting document with parent and related document`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Accounting document with parent and related document']' timed out after 55 seconds
```
</details>

### Case 5: TIMEOUT

- **Query:** `Proposals joined to persons and proposal states`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Proposals joined to persons and proposal states']' timed out after 55 seconds
```
</details>

### Case 6: TIMEOUT

- **Query:** `Payments with payment file and user who created`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Payments with payment file and user who created']' timed out after 55 seconds
```
</details>

### Case 7: TIMEOUT

- **Query:** `Documents with amendment requests and confirm user`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Documents with amendment requests and confirm user']' timed out after 55 seconds
```
</details>

### Case 8: TIMEOUT

- **Query:** `Addendums with base addendum and linked proposal insured risk`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Addendums with base addendum and linked proposal insured risk']' timed out after 55 seconds
```
</details>

### Case 9: TIMEOUT

- **Query:** `Entries with document, coding and subcoding`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Entries with document, coding and subcoding']' timed out after 55 seconds
```
</details>

### Case 10: PASS

- **Query:** `Policy with beneficiary and insurer`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500)                                                             â”‚
â”‚     d.ReferenceNumber,                                                       â”‚
â”‚     d.Date,                                                                  â”‚
â”‚     d.Type,                                                                  â”‚
â”‚     p.BeneficiaryName,                                                       â”‚
â”‚     i.InsurerName                                                            â”‚
â”‚ FROM                                                                         â”‚
â”‚     Accounting.Document d                                                    â”‚
â”‚ LEFT JOIN                                                                    â”‚
â”‚     Accounting.Parent p ON d.ParentId = p.Id                                 â”‚
â”‚ LEFT JOIN                                                                    â”‚
â”‚     Accounting.Document relatedDoc ON d.RelatedDocumentId = relatedDoc.Id    â”‚
â”‚ LEFT JOIN                                                                    â”‚
â”‚     Accounting.Document insurerDoc ON relatedDoc.RelatedDocument
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:41:10.531569+00:00", "level": "INFO", "message": "Query received", "request_id": "4d591c20", "user_input": "Policy with beneficiary and insurer"}
[92m00:11:10 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:41:10.538670+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:11:10"}
[92m00:11:29 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:41:29.868959+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:11:29"}
{"timestamp": "2026-02-15T20:41:29.958146+00:00", "level": "WARNING", "message": "Too ma
```
</details>

### Case 11: TIMEOUT

- **Query:** `Documents created in last 7 days where type is 1 or 2`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Documents created in last 7 days where type is 1 or 2']' timed out after 55 seconds
```
</details>

### Case 12: TIMEOUT

- **Query:** `Proposals with status between 1 and 5 created after 2024`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Proposals with status between 1 and 5 created after 2024']' timed out after 55 seconds
```
</details>

### Case 13: TIMEOUT

- **Query:** `Users active and not deleted with email containing @company`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Users active and not deleted with email containing @company']' timed out after 55 seconds
```
</details>

### Case 14: TIMEOUT

- **Query:** `Accounting entries where amount greater than 1000 and date in last month`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Accounting entries where amount greater than 1000 and date in last month']' timed out after 55 seconds
```
</details>

### Case 15: PASS

- **Query:** `Policies that are active and have premium payment term annual`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500)                                                             â”‚
â”‚     d.*                                                                      â”‚
â”‚ FROM                                                                         â”‚
â”‚     Accounting.Document d                                                    â”‚
â”‚ INNER JOIN                                                                   â”‚
â”‚     Accounting.Document p ON d.ParentId = p.Id                               â”‚
â”‚ WHERE                                                                        â”‚
â”‚     d.Type = 'Premium' AND                                                   â”‚
â”‚     d.Date >= GETDATE() AND                                                  â”‚
â”‚     p.Type = 'Policy';                                                       â”‚
â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•¯
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:45:23.860051+00:00", "level": "INFO", "message": "Query received", "request_id": "0903f4dd", "user_input": "Policies that are active and have premium payment term annual"}
[92m00:15:23 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:45:23.868066+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:15:23"}
[92m00:15:43 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:45:43.687255+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:15:43"}
{"timestamp": "2026-02-15T20:45:43.774010+00:00", "level": "WA
```
</details>

### Case 16: PASS

- **Query:** `Proposals by status with count greater than 10`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500) d.Status, COUNT(*) AS ProposalCount                         â”‚
â”‚ FROM Accounting.Document d                                                   â”‚
â”‚ GROUP BY d.Status                                                            â”‚
â”‚ HAVING COUNT(*) > 10;                                                        â”‚
â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•¯
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:45:52.252135+00:00", "level": "INFO", "message": "Query received", "request_id": "b1065218", "user_input": "Proposals by status with count greater than 10"}
[92m00:15:52 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:45:52.259763+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:15:52"}
[92m00:16:24 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:46:24.789799+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:16:24"}
{"timestamp": "2026-02-15T20:46:24.870615+00:00", "level": "WARNING", "messag
```
</details>

### Case 17: PASS

- **Query:** `Documents where reference number is not null order by date desc`
- **Exit code:** 0  
- **Timeout:** False  

<details>
<summary>stdout (excerpt)</summary>

```
â•­â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ Generated SQL (dry run) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•®
â”‚ SELECT TOP (500) *                                                           â”‚
â”‚ FROM Accounting.Document                                                     â”‚
â”‚ WHERE ReferenceNumber IS NOT NULL                                            â”‚
â”‚ ORDER BY Date DESC;                                                          â”‚
â•°â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â•¯
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
{"timestamp": "2026-02-15T20:46:31.305859+00:00", "level": "INFO", "message": "Query received", "request_id": "9a6f4790", "user_input": "Documents where reference number is not null order by date desc"}
[92m00:16:31 - LiteLLM:INFO[0m: utils.py:3889 - 
LiteLLM completion() model= qwen2.5-coder:7b; provider = ollama
{"timestamp": "2026-02-15T20:46:31.313853+00:00", "level": "INFO", "message": "\nLiteLLM completion() model= qwen2.5-coder:7b; provider = ollama", "asctime": "00:16:31"}
[92m00:17:20 - LiteLLM:INFO[0m: utils.py:1629 - Wrapper: Completed Call, calling success_handler
{"timestamp": "2026-02-15T20:47:20.142937+00:00", "level": "INFO", "message": "Wrapper: Completed Call, calling success_handler", "asctime": "00:17:20"}
{"timestamp": "2026-02-15T20:47:20.228260+00:00", "level": "
```
</details>

### Case 18: TIMEOUT

- **Query:** `Users who have logged in in the last 30 days`
- **Exit code:** -1  
- **Timeout:** True  

<details>
<summary>stdout (excerpt)</summary>

```
(empty)
```
</details>

<details>
<summary>stderr (excerpt)</summary>

```
Command '['/home/mehdi/projects/personal/tadbir-query-generator/.venv/bin/python', '/home/mehdi/projects/personal/tadbir-query-generator/main.py', '--dry-run', 'Users who have logged in in the last 30 days']' timed out after 55 seconds
```
</details>

### Case 19: PENDING

- **Query:** `Entries grouped by coding with sum of amount`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 20: PENDING

- **Query:** `Addendums of type beneficiary change in last quarter`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 21: PENDING

- **Query:** `Count of proposals per status`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 22: PENDING

- **Query:** `Sum of amounts by document type in accounting`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 23: PENDING

- **Query:** `Average premium by insurance plan`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 24: PENDING

- **Query:** `Max and min date of documents per year`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 25: PENDING

- **Query:** `Count distinct users per role`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 26: PENDING

- **Query:** `Total entries per coding code`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 27: PENDING

- **Query:** `Number of addendums per base addendum type`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 28: PENDING

- **Query:** `Count policies grouped by status and plan`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 29: PENDING

- **Query:** `Sum of payment amounts by month`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 30: PENDING

- **Query:** `Count documents by parent and type`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 31: PENDING

- **Query:** `Ù„ÛŒØ³Øª Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯Ù‡Ø§ÛŒ ØªØ§ÛŒÛŒØ¯ Ø´Ø¯Ù‡`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 32: PENDING

- **Query:** `ØªØ¹Ø¯Ø§Ø¯ Ú©Ø§Ø±Ø¨Ø±Ø§Ù† Ù�Ø¹Ø§Ù„`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 33: PENDING

- **Query:** `Ø³Ù†Ø¯Ù‡Ø§ÛŒ Ø­Ø³Ø§Ø¨Ø¯Ø§Ø±ÛŒ Ù‡Ù�ØªÙ‡ Ú¯Ø°Ø´ØªÙ‡`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 34: PENDING

- **Query:** `Ø¨ÛŒÙ…Ù‡â€ŒÙ†Ø§Ù…Ù‡â€ŒÙ‡Ø§ÛŒ Ù…Ù†Ù‚Ø¶ÛŒ Ø´Ø¯Ù‡`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 35: PENDING

- **Query:** `Ù¾Ø±Ø¯Ø§Ø®Øªâ€ŒÙ‡Ø§ÛŒ Ù…ÙˆÙ�Ù‚ Ø¢Ø®Ø±ÛŒÙ† Ù…Ø§Ù‡`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 36: PENDING

- **Query:** `Ú¯Ø²Ø§Ø±Ø´ Ù¾ÛŒØ´Ù†Ù‡Ø§Ø¯ Ø¨Ù‡ ØªÙ�Ú©ÛŒÚ© ÙˆØ¶Ø¹ÛŒØª`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 37: PENDING

- **Query:** `Ø§Ù�Ø±Ø§Ø¯ Ø¨Ø§ Ú©Ø¯ Ù…Ù„ÛŒ Ø®Ø§Ù„ÛŒ`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 38: PENDING

- **Query:** `Ú†Ù†Ø¯ ØªØ§ Ø³Ù†Ø¯ Ø§ØµÙ„Ø§Ø­ÛŒÙ‡ Ø¯Ø§Ø±ÛŒÙ…`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 39: PENDING

- **Query:** `Ù„ÛŒØ³Øª Ù†Ù‚Ø´â€ŒÙ‡Ø§ÛŒ Ú©Ø§Ø±Ø¨Ø±ÛŒ`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 40: PENDING

- **Query:** `Ù…Ø¬Ù…ÙˆØ¹ Ù…Ø¨Ø§Ù„Øº Ø¨Ù‡ ØªÙ�Ú©ÛŒÚ© Ù†ÙˆØ¹ Ø³Ù†Ø¯`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 41: PENDING

- **Query:** `Show me everything from last week`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 42: PENDING

- **Query:** `Give me reports`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 43: PENDING

- **Query:** `What do we have`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 44: PENDING

- **Query:** `List data`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 45: PENDING

- **Query:** `Summary`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 46: PENDING

- **Query:** `All of them`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 47: PENDING

- **Query:** `Recent stuff`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 48: PENDING

- **Query:** `Important records`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 49: PENDING

- **Query:** `Things that need attention`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 50: PENDING

- **Query:** `Whatever is active`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 51: PENDING

- **Query:** `I need a list of all accounting documents that were created in the last week and have a document type of either 1 or 2, and I want to see the reference number and date and type, please`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 52: PENDING

- **Query:** `Show proposals that are in status approved or pending and were created by a user who is still active and the proposal has at least one insured risk linked to it`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 53: PENDING

- **Query:** `List every user with their username and email and the name of their role and whether they are active, but only if they have logged in at least once`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 54: PENDING

- **Query:** `Accounting entries joined to their document and to the coding table, where the entry amount is positive and the document date is in the current year, grouped by document type`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 55: PENDING

- **Query:** `I want to see addendums of type beneficiary change or premium change that are linked to a base addendum which was created last month`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 56: PENDING

- **Query:** `Documents where type = 1`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 57: PENDING

- **Query:** `Select * from Accounting.Document where Date > '2024-01-01'`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 58: PENDING

- **Query:** `User's list`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 59: PENDING

- **Query:** `Proposals (active only)`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 60: PENDING

- **Query:** `Count(*) from Document`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 61: PENDING

- **Query:** `List users where id is 1`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 62: PENDING

- **Query:** `Show documents; comment`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 63: PENDING

- **Query:** `Proposals where status in (1,2,3)`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 64: PENDING

- **Query:** `Users order by Id`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 65: PENDING

- **Query:** `Select Id from Accounting.Document`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 66: PENDING

- **Query:** `acounting documnts`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 67: PENDING

- **Query:** `proposlas by statu`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 68: PENDING

- **Query:** `usrs and roels`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 69: PENDING

- **Query:** `lisr of polocies`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 70: PENDING

- **Query:** `docuemnts form last weak`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 71: PENDING

- **Query:** `Documents from 2024-06-01 to 2024-06-30`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 72: PENDING

- **Query:** `Proposals created on 2025-01-15`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 73: PENDING

- **Query:** `Users with more than 5 logins`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 74: PENDING

- **Query:** `Entries with amount between 100 and 500`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 75: PENDING

- **Query:** `Policies expiring in next 30 days`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 76: PENDING

- **Query:** `Documents that are not type 0`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 77: PENDING

- **Query:** `Users who are not deleted`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 78: PENDING

- **Query:** `Proposals not in draft status`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 79: PENDING

- **Query:** `Entries without a linked subcoding`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 80: PENDING

- **Query:** `Policies that do not have addendums`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 81: PENDING

- **Query:** `Documents that have at least one entry with amount > 100`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 82: PENDING

- **Query:** `Proposals that have insured risks and are in approved status`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 83: PENDING

- **Query:** `Users who have a role and are active`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 84: PENDING

- **Query:** `Accounting documents with parent type 1 or no parent`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 85: PENDING

- **Query:** `Addendums linked to proposal insured risk where the risk is active`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 86: PENDING

- **Query:** `Top 10 documents by date with their entry count`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 87: PENDING

- **Query:** `Proposals with their person name and state name and count of insured risks`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 88: PENDING

- **Query:** `Users with role, last login date, and count of operations`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 89: PENDING

- **Query:** `Documents with parent reference and related document reference`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 90: PENDING

- **Query:** `Payments grouped by user and by month with total amount`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 91: PENDING

- **Query:** `Policies with plan name and beneficiary count`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 92: PENDING

- **Query:** `Entries with document reference and coding title and subcoding`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 93: PENDING

- **Query:** `Addendums with base addendum date and type description`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 94: PENDING

- **Query:** `Full join of document and entry and coding`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 95: PENDING

- **Query:** `Proposals with person and state and plan and insured risk count`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 96: PENDING

- **Query:** `Sum of debit and credit by document and coding`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 97: PENDING

- **Query:** `Users with no role assigned`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 98: PENDING

- **Query:** `Ø¢Ø®Ø±ÛŒÙ† Ù¾Ø±Ø¯Ø§Ø®Øª Ù‡Ø± Ú©Ø§Ø±Ø¨Ø±`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 99: PENDING

- **Query:** `Documents with more than 10 entries`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*

### Case 100: PENDING

- **Query:** `Proposals created yesterday with person name`
- **Exit code:** -  
- **Timeout:** False  

*Not run yet.*
