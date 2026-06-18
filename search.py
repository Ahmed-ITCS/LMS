"""
Group E - Search Module
Purpose: Enable search by title, author, or ISBN.
Responsibilities: Help users find available books.
"""


def search_by_title(library, title):
  """Return books whose title contains the query (case-insensitive)."""
  query = title.lower()
  return [book for book in library.list_books() if query in book.title.lower()]


def search_by_author(library, author):
  """Return books whose author contains the query (case-insensitive)."""
  query = author.lower()
  return [book for book in library.list_books() if query in book.author.lower()]


def search_by_isbn(library, isbn):
  """Return a book with an exact ISBN match."""
  book = library.get_book(isbn)
  return [book] if book else []


def search_books(library, query_string):
  """Search across title, author, and exact ISBN."""
  if not query_string:
    return []

  results = {}
  for book in (
    search_by_title(library, query_string)
    + search_by_author(library, query_string)
    + search_by_isbn(library, query_string)
  ):
    results[book.isbn] = book
  return list(results.values())
