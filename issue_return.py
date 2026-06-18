"""
Group D - Issue and Return Module
Purpose: Handle book issuance and return.
Responsibilities: Update availability when members borrow or return books.
"""


def issue_book(library, isbn, member):
  """
  Issue a book to a member if copies are available.
  Returns True on success, False otherwise.
  """
  book = library.get_book(isbn)
  if book and book.copies > 0:
    book.copies -= 1
    member.borrowed_books.append(isbn)
    return True
  return False


def return_book(library, isbn, member):
  """
  Return a borrowed book from a member.
  Returns True on success, False otherwise.
  """
  if isbn in member.borrowed_books:
    member.borrowed_books.remove(isbn)
    book = library.get_book(isbn)
    if book:
      book.copies += 1
    return True
  return False
