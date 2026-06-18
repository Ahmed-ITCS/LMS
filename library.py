"""
Group C - Library Module
Purpose: Manage the library's book collection.
Responsibilities: Add, remove, and list books.
"""


class Library:
  """In-memory catalog that stores books keyed by ISBN."""

  def __init__(self):
    self.books = {}

  def add_book(self, book):
    """Add a book or increment copies if the ISBN already exists."""
    if book.isbn in self.books:
      self.books[book.isbn].copies += book.copies
    else:
      self.books[book.isbn] = book
    return True

  def remove_book(self, isbn):
    """Remove a book from the collection by ISBN."""
    if isbn in self.books:
      del self.books[isbn]
      return True
    return False

  def get_book(self, isbn):
    """Return a book by ISBN, or None if not found."""
    return self.books.get(isbn)

  def list_books(self):
    """Return all books in the catalog."""
    return list(self.books.values())

  def get_available_books(self):
    """Return books that have at least one copy available."""
    return [book for book in self.books.values() if book.copies > 0]
