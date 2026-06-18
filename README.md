# Athenaeum — Library Management System

A collaborative Django web application with standalone Python modules, built by **Groups A through H** using isolated Git branches and pull-request merges.

See **[GROUPS.md](GROUPS.md)** for branch names, file ownership, and merge order.

## Group Modules (Standalone)

| File | Group | Purpose |
|------|-------|---------|
| `book.py` | A | Book class |
| `member.py` | B | Member class |
| `library.py` | C | Library catalog |
| `issue_return.py` | D | Issue & return logic |
| `search.py` | E | Search functions |
| `auth_system.py` | F | CLI authentication |
| `library_management_system.py` | G | CLI main menu |
| `test_library.py` | H | Standalone unit tests |

## GitHub Workflow

```bash
# 1. Create your group branch from main
git checkout main && git pull
git checkout -b group-a-book   # use your group's branch name

# 2. Develop only your assigned files (see GROUPS.md)

# 3. Open a PR to main using .github/PULL_REQUEST_TEMPLATE.md

# 4. After review + Group H test pass → merge
```

### Rebuild group branch history (maintainers)

```bash
chmod +x scripts/setup_group_branches.sh
./scripts/setup_group_branches.sh
```

This creates `group-a-book` through `group-h-testing` branches and merges them into `main` in order.

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data --clear
python manage.py runserver
```

Visit http://127.0.0.1:8000/

### CLI Application (Group G)

```bash
python library_management_system.py
```

## Seed Data

```bash
python manage.py seed_data --clear
```

| Role | Username | Password |
|------|----------|----------|
| Librarian | `librarian` | `librarian123` |
| Member | `alice`, `bob`, `carol`, `david` | `password123` |

## Running Tests

```bash
python test_library.py          # Standalone modules (Group H)
python manage.py test           # Django integration (Group H)
```

## URL Map

| Path | Description | Access |
|------|-------------|--------|
| `/` | Dashboard | Public |
| `/catalog/` | Book catalog | Public |
| `/catalog/add/` | Add book | Librarian |
| `/search/` | Search books | Public |
| `/transaction/issue/` | Issue book | Librarian |
| `/transaction/return/` | Return book | Librarian |
| `/auth/login/` | Login | Public |
| `/auth/register/` | Member registration | Public |
| `/account/` | Member borrowing history | Member |
| `/admin/` | Django admin | Staff |

## Roles

- **Members** — search catalog, view dashboard, see personal loan history
- **Librarians** (`is_staff=True`) — add/remove books, issue and return loans
