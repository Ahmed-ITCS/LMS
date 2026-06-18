#!/usr/bin/env bash
# Rebuild group-wise branch history from the integration branch.
# Usage: ./scripts/setup_group_branches.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

BASE_COMMIT="28329d2"
INTEGRATION_BRANCH="full-integration"

echo "==> Saving current work to $INTEGRATION_BRANCH"
git add -A
if git diff --cached --quiet; then
  echo "    Nothing to commit on integration branch."
else
  git commit -m "Full LMS integration (all groups)" || true
fi
git branch -f "$INTEGRATION_BRANCH" HEAD

echo "==> Resetting main to scaffold ($BASE_COMMIT)"
git checkout main
git reset --hard "$BASE_COMMIT"

merge_group() {
  local branch="$1"
  local message="$2"
  shift 2
  local files=("$@")

  echo ""
  echo "==> Group branch: $branch"
  git checkout -B "$branch" main
  for f in "${files[@]}"; do
    git checkout "$INTEGRATION_BRANCH" -- "$f" 2>/dev/null || true
  done
  git add -A
  if ! git diff --cached --quiet; then
    git commit -m "$message"
  fi
  git checkout main
  git merge --no-ff "$branch" -m "Merge $branch into main"
}

merge_group "group-a-book" "Group A: Book module and Django Book model" \
  book.py library_app/models/book.py library_app/models/__init__.py \
  library_project/settings.py library_project/wsgi.py library_app/migrations/0001_initial.py

merge_group "group-b-member" "Group B: Member module and Django Member model" \
  member.py library_app/models/member.py library_app/models/__init__.py \
  library_app/migrations/0001_initial.py

merge_group "group-c-library" "Group C: Library module and catalog service" \
  library.py library_app/services/catalog.py library_app/services/__init__.py library_app/admin.py

merge_group "group-d-issue-return" "Group D: Issue/return module and transaction service" \
  issue_return.py library_app/models/transaction.py library_app/models/__init__.py \
  library_app/services/transactions.py library_app/migrations/0001_initial.py

merge_group "group-e-search" "Group E: Search module and search service" \
  search.py library_app/services/search.py library_app/templates/library_app/search.html

merge_group "group-f-auth" "Group F: Auth module, forms, and decorators" \
  auth_system.py library_app/decorators.py library_app/forms.py \
  library_app/templates/library_app/login.html library_app/templates/library_app/register.html

merge_group "group-g-interface" "Group G: Django UI, URLs, views, CLI, and static assets" \
  library_management_system.py library_app/views.py library_app/urls.py library_project/urls.py \
  library_project/settings.py library_app/templates/library_app/base.html \
  library_app/templates/library_app/dashboard.html library_app/templates/library_app/catalog.html \
  library_app/templates/library_app/add_book.html library_app/templates/library_app/issue.html \
  library_app/templates/library_app/return.html library_app/templates/library_app/my_account.html \
  library_app/static/library_app/css/style.css library_app/static/library_app/js/app.js

merge_group "group-h-testing" "Group H: Unit tests and seed data command" \
  test_library.py library_app/tests.py library_app/management/__init__.py \
  library_app/management/commands/__init__.py library_app/management/commands/seed_data.py \
  README.md GROUPS.md .github/PULL_REQUEST_TEMPLATE.md scripts/setup_group_branches.sh

echo ""
echo "==> Done! Branch graph:"
git log --oneline --graph -20
