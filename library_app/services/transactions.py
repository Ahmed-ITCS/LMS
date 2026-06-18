from django.db import transaction
from django.utils import timezone

from library_app.models import Book, BookTransaction, Member


class InsufficientStockError(Exception):
    """Raised when no copies are available to issue."""


class TransactionNotActiveError(Exception):
    """Raised when attempting to return an inactive transaction."""


@transaction.atomic
def issue_book(isbn, member_id):
    """
    Issue a book to a member. Decrements stock and creates a transaction record.
    """
    book = Book.objects.select_for_update().get(isbn=isbn)
    member = Member.objects.get(member_id=member_id)

    if book.copies <= 0:
        raise InsufficientStockError(f"No copies of '{book.title}' are available.")

    book.copies -= 1
    book.save(update_fields=['copies'])

    return BookTransaction.objects.create(book=book, member=member, is_active=True)


@transaction.atomic
def return_book(transaction_id):
    """
    Return a borrowed book. Marks the transaction inactive and restores stock.
    """
    txn = BookTransaction.objects.select_for_update().get(pk=transaction_id)

    if not txn.is_active:
        raise TransactionNotActiveError("This loan has already been returned.")

    book = Book.objects.select_for_update().get(pk=txn.book_id)
    txn.is_active = False
    txn.return_date = timezone.now()
    txn.save(update_fields=['is_active', 'return_date'])

    book.copies += 1
    book.save(update_fields=['copies'])

    return txn
