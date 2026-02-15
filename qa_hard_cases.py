#!/usr/bin/env python3
"""100 hard/edge-case queries for QA. Run with: python run_qa_hard.py"""

HARD_CASES = [
    # --- Joins (multi-table) ---
    "Show accounting documents with their entries and coding, joined",
    "List proposals with their insured risks and insurance plan names",
    "Users and their roles with role name",
    "Accounting document with parent and related document",
    "Proposals joined to persons and proposal states",
    "Payments with payment file and user who created",
    "Documents with amendment requests and confirm user",
    "Addendums with base addendum and linked proposal insured risk",
    "Entries with document, coding and subcoding",
    "Policy with beneficiary and insurer",
    # --- Complex filters ---
    "Documents created in last 7 days where type is 1 or 2",
    "Proposals with status between 1 and 5 created after 2024",
    "Users active and not deleted with email containing @company",
    "Accounting entries where amount greater than 1000 and date in last month",
    "Policies that are active and have premium payment term annual",
    "Proposals by status with count greater than 10",
    "Documents where reference number is not null order by date desc",
    "Users who have logged in in the last 30 days",
    "Entries grouped by coding with sum of amount",
    "Addendums of type beneficiary change in last quarter",
    # --- Aggregations ---
    "Count of proposals per status",
    "Sum of amounts by document type in accounting",
    "Average premium by insurance plan",
    "Max and min date of documents per year",
    "Count distinct users per role",
    "Total entries per coding code",
    "Number of addendums per base addendum type",
    "Count policies grouped by status and plan",
    "Sum of payment amounts by month",
    "Count documents by parent and type",
    # --- Persian / mixed ---
    "لیست پیشنهادهای تایید شده",
    "تعداد کاربران فعال",
    "سندهای حسابداری هفته گذشته",
    "بیمه‌نامه‌های منقضی شده",
    "پرداخت‌های موفق آخرین ماه",
    "گزارش پیشنهاد به تفکیک وضعیت",
    "افراد با کد ملی خالی",
    "چند تا سند اصلاحیه داریم",
    "لیست نقش‌های کاربری",
    "مجموع مبالغ به تفکیک نوع سند",
    # --- Ambiguous / vague ---
    "Show me everything from last week",
    "Give me reports",
    "What do we have",
    "List data",
    "Summary",
    "All of them",
    "Recent stuff",
    "Important records",
    "Things that need attention",
    "Whatever is active",
    # --- Edge: long / verbose ---
    "I need a list of all accounting documents that were created in the last week and have a document type of either 1 or 2, and I want to see the reference number and date and type, please",
    "Show proposals that are in status approved or pending and were created by a user who is still active and the proposal has at least one insured risk linked to it",
    "List every user with their username and email and the name of their role and whether they are active, but only if they have logged in at least once",
    "Accounting entries joined to their document and to the coding table, where the entry amount is positive and the document date is in the current year, grouped by document type",
    "I want to see addendums of type beneficiary change or premium change that are linked to a base addendum which was created last month",
    # --- Edge: special chars / symbols ---
    "Documents where type = 1",
    "Select * from Accounting.Document where Date > '2024-01-01'",
    "User's list",
    "Proposals (active only)",
    "Count(*) from Document",
    # --- Edge: injection-like (must still be safe) ---
    "List users where id is 1",
    "Show documents; comment",
    "Proposals where status in (1,2,3)",
    "Users order by Id",
    "Select Id from Accounting.Document",
    # --- Edge: typos / noisy ---
    "acounting documnts",
    "proposlas by statu",
    "usrs and roels",
    "lisr of polocies",
    "docuemnts form last weak",
    # --- Edge: numbers and dates ---
    "Documents from 2024-06-01 to 2024-06-30",
    "Proposals created on 2025-01-15",
    "Users with more than 5 logins",
    "Entries with amount between 100 and 500",
    "Policies expiring in next 30 days",
    # --- Edge: negations ---
    "Documents that are not type 0",
    "Users who are not deleted",
    "Proposals not in draft status",
    "Entries without a linked subcoding",
    "Policies that do not have addendums",
    # --- Edge: nested / complex logic ---
    "Documents that have at least one entry with amount > 100",
    "Proposals that have insured risks and are in approved status",
    "Users who have a role and are active",
    "Accounting documents with parent type 1 or no parent",
    "Addendums linked to proposal insured risk where the risk is active",
    # --- Super hard ---
    "Top 10 documents by date with their entry count",
    "Proposals with their person name and state name and count of insured risks",
    "Users with role, last login date, and count of operations",
    "Documents with parent reference and related document reference",
    "Payments grouped by user and by month with total amount",
    "Policies with plan name and beneficiary count",
    "Entries with document reference and coding title and subcoding",
    "Addendums with base addendum date and type description",
    "Full join of document and entry and coding",
    "Proposals with person and state and plan and insured risk count",
    # --- 5 more to reach 100 ---
    "Sum of debit and credit by document and coding",
    "Users with no role assigned",
    "آخرین پرداخت هر کاربر",
    "Documents with more than 10 entries",
    "Proposals created yesterday with person name",
]

if __name__ == "__main__":
    print(len(HARD_CASES))
    for i, q in enumerate(HARD_CASES):
        print(f"{i+1}. {q[:60]}{'...' if len(q) > 60 else ''}")
