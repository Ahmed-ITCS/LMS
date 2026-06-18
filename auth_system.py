"""
Group F - Authentication Module
Purpose: Authenticate users (librarians/members).
Responsibilities: Basic login system for the CLI application.
"""

# Demo credentials for the standalone CLI (not used by Django auth).
USER_DB = {
  'librarian': 'librarian123',
  'alice': 'password123',
  'bob': 'password123',
}


def authenticate(username, password, user_db=None):
  """
  Verify username/password against the user database.
  Returns True if credentials match, False otherwise.
  """
  db = user_db if user_db is not None else USER_DB
  return db.get(username) == password


def is_librarian(username):
  """Librarians are identified by the 'librarian' username in the CLI."""
  return username == 'librarian'
