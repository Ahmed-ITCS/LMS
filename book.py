"""
Group A - Book Module
Purpose: Define the structure of a book.
Responsibilities: Store book data (ISBN, title, author, copies).
"""


class Book:
  """Represents a single book in the library catalog."""

  def __init__(self, isbn, title, author, copies):
    self.isbn = isbn
    self.title = title
    self.author = author
    self.copies = copies

  def __str__(self):
    return f"{self.title} by {self.author} (ISBN: {self.isbn})"

  def __repr__(self):
    return f"Book(isbn={self.isbn!r}, title={self.title!r}, copies={self.copies})"
