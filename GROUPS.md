# Group Assignments & Branch Guide

This project follows the **Library Management System GitHub Collaboration Plan**.
Each group works on an isolated branch and opens a PR to `main` when complete.

## Branch Naming

| Group | Branch | Module Files |
|-------|--------|--------------|
| **A** | `group-a-book` | `book.py`, `library_app/models/book.py` |
| **B** | `group-b-member` | `member.py`, `library_app/models/member.py` |
| **C** | `group-c-library` | `library.py`, `library_app/services/catalog.py` |
| **D** | `group-d-issue-return` | `issue_return.py`, `library_app/models/transaction.py`, `library_app/services/transactions.py` |
| **E** | `group-e-search` | `search.py`, `library_app/services/search.py` |
| **F** | `group-f-auth` | `auth_system.py`, `library_app/decorators.py`, `library_app/forms.py` |
| **G** | `group-g-interface` | `library_management_system.py`, `library_app/views.py`, `library_app/urls.py`, templates, static, settings |
| **H** | `group-h-testing` | `test_library.py`, `library_app/tests.py`, `seed_data` command |

## Merge Order

Branches must merge into `main` in dependency order:

```
group-a-book → group-b-member → group-c-library → group-d-issue-return
→ group-e-search → group-f-auth → group-g-interface → group-h-testing
```

## Workflow

1. **Branch** — `git checkout -b group-x-name` from latest `main`
2. **Develop** — only touch files assigned to your group
3. **Test** — run your module tests locally
4. **PR** — open a pull request using `.github/PULL_REQUEST_TEMPLATE.md`
5. **Review** — at least one other group reviews; Group H verifies tests
6. **Merge** — merge to `main` only after approval

## Standalone vs Django

| Layer | Purpose |
|-------|---------|
| Root `.py` files | Standalone OOP modules (CLI app) |
| `library_app/` | Django web integration |
| `library_management_system.py` | Group G CLI that wires standalone modules |

## Running Tests

```bash
# Standalone module tests (Group H)
python test_library.py

# Django integration tests (Group H)
python manage.py test

# Seed demo data
python manage.py seed_data --clear
```

## Demo Accounts

| Role | Username | Password |
|------|----------|----------|
| Librarian | `librarian` | `librarian123` |
| Member | `alice` | `password123` |

## Rules

- Do **not** push directly to `main`
- Report interface changes to **Group G** immediately
- Use consistent variable names across all groups
- Document every class and function with docstrings
