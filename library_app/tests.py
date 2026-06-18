from django.contrib.auth.models import User
from django.test import TestCase

from library_app.models import Book, BookTransaction, Member
from library_app.services.catalog import BookInUseError, add_book, remove_book
from library_app.services.search import search_books
from library_app.services.transactions import (
    InsufficientStockError,
    issue_book,
    return_book,
)


class LibrarySystemIntegrationTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            isbn='9780132350884',
            title='Clean Code',
            author='Robert Martin',
            copies=1,
        )
        self.user = User.objects.create_user(
            username='student1',
            password='securepassword',
        )
        self.member = Member.objects.create(user=self.user, member_id='MEM001')

    def test_successful_book_addition(self):
        self.assertEqual(Book.objects.count(), 1)

    def test_add_book_increments_existing_isbn(self):
        book, created = add_book(
            '9780132350884',
            'Clean Code',
            'Robert Martin',
            copies=2,
        )
        self.assertFalse(created)
        self.assertEqual(book.copies, 3)

    def test_duplicate_isbn_blocked_at_database_level(self):
        with self.assertRaises(Exception):
            Book.objects.create(
                isbn='9780132350884',
                title='Duplicate',
                author='Someone',
                copies=1,
            )

    def test_search_by_title(self):
        results = search_books('clean')
        self.assertEqual(results.count(), 1)

    def test_search_by_exact_isbn(self):
        results = search_books('9780132350884')
        self.assertEqual(results.count(), 1)

    def test_search_empty_query_returns_none(self):
        results = search_books('')
        self.assertEqual(results.count(), 0)

    def test_stock_depletion_on_issue(self):
        issue_book(self.book.isbn, self.member.member_id)
        updated_book = Book.objects.get(isbn='9780132350884')
        self.assertEqual(updated_book.copies, 0)
        self.assertEqual(BookTransaction.objects.filter(is_active=True).count(), 1)

    def test_issue_blocked_when_stock_zero(self):
        issue_book(self.book.isbn, self.member.member_id)
        with self.assertRaises(InsufficientStockError):
            issue_book(self.book.isbn, self.member.member_id)

    def test_return_restores_stock(self):
        txn = issue_book(self.book.isbn, self.member.member_id)
        return_book(txn.pk)
        updated_book = Book.objects.get(isbn='9780132350884')
        self.assertEqual(updated_book.copies, 1)
        txn.refresh_from_db()
        self.assertFalse(txn.is_active)
        self.assertIsNotNone(txn.return_date)

    def test_remove_book_blocked_when_on_loan(self):
        issue_book(self.book.isbn, self.member.member_id)
        with self.assertRaises(BookInUseError):
            remove_book(self.book.isbn)

    def test_remove_book_when_not_on_loan(self):
        remove_book(self.book.isbn)
        self.assertEqual(Book.objects.count(), 0)


class LibraryViewTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            isbn='9780132350884',
            title='Clean Code',
            author='Robert Martin',
            copies=2,
        )
        self.member_user = User.objects.create_user(
            username='member1',
            password='securepassword',
        )
        self.member = Member.objects.create(
            user=self.member_user,
            member_id='MEM001',
        )
        self.librarian = User.objects.create_user(
            username='librarian',
            password='securepassword',
            is_staff=True,
        )

    def test_dashboard_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_catalog_loads(self):
        response = self.client.get('/catalog/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clean Code')

    def test_search_finds_books(self):
        response = self.client.get('/search/', {'query': 'clean'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Clean Code')

    def test_add_book_requires_staff(self):
        self.client.login(username='member1', password='securepassword')
        response = self.client.get('/catalog/add/')
        self.assertEqual(response.status_code, 302)

    def test_librarian_can_access_add_book(self):
        self.client.login(username='librarian', password='securepassword')
        response = self.client.get('/catalog/add/')
        self.assertEqual(response.status_code, 200)

    def test_login_and_account_page(self):
        self.client.login(username='member1', password='securepassword')
        response = self.client.get('/account/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'MEM001')
