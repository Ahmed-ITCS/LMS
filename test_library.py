"""
Group H - Unit Testing Module
Purpose: Ensure standalone modules work correctly.
Responsibilities: Write tests for all major functions.
"""

import unittest

from auth_system import authenticate
from book import Book
from issue_return import issue_book, return_book
from library import Library
from member import Member
from search import search_by_isbn, search_by_title, search_books


class BookModuleTests(unittest.TestCase):
  def test_book_attributes(self):
    book = Book('9780132350884', 'Clean Code', 'Robert Martin', 2)
    self.assertEqual(book.isbn, '9780132350884')
    self.assertEqual(book.copies, 2)


class LibraryModuleTests(unittest.TestCase):
  def test_add_book(self):
    library = Library()
    book = Book('123', 'Test Book', 'Author', 2)
    library.add_book(book)
    self.assertIn('123', library.books)

  def test_add_book_increments_copies(self):
    library = Library()
    library.add_book(Book('123', 'Test Book', 'Author', 2))
    library.add_book(Book('123', 'Test Book', 'Author', 3))
    self.assertEqual(library.books['123'].copies, 5)


class IssueReturnTests(unittest.TestCase):
  def setUp(self):
    self.library = Library()
    self.library.add_book(Book('123', 'Test Book', 'Author', 1))
    self.member = Member('MEM001', 'Alice')

  def test_issue_reduces_stock(self):
    self.assertTrue(issue_book(self.library, '123', self.member))
    self.assertEqual(self.library.books['123'].copies, 0)

  def test_issue_blocked_when_no_stock(self):
    issue_book(self.library, '123', self.member)
    self.assertFalse(issue_book(self.library, '123', self.member))

  def test_return_restores_stock(self):
    issue_book(self.library, '123', self.member)
    self.assertTrue(return_book(self.library, '123', self.member))
    self.assertEqual(self.library.books['123'].copies, 1)


class SearchModuleTests(unittest.TestCase):
  def setUp(self):
    self.library = Library()
    self.library.add_book(Book('9780132350884', 'Clean Code', 'Robert Martin', 2))

  def test_search_by_title(self):
    results = search_by_title(self.library, 'clean')
    self.assertEqual(len(results), 1)

  def test_search_by_isbn(self):
    results = search_by_isbn(self.library, '9780132350884')
    self.assertEqual(len(results), 1)

  def test_combined_search(self):
    results = search_books(self.library, 'martin')
    self.assertEqual(len(results), 1)


class AuthModuleTests(unittest.TestCase):
  def test_authenticate_valid(self):
    self.assertTrue(authenticate('librarian', 'librarian123'))

  def test_authenticate_invalid(self):
    self.assertFalse(authenticate('librarian', 'wrong'))


if __name__ == '__main__':
  unittest.main()
