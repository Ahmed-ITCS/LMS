from library_app.models import Book


class BookInUseError(Exception):
    """Raised when a book cannot be removed because it is on loan."""


def add_book(isbn, title, author, copies=1):
    """
    Add a book to the catalog. If the ISBN already exists, increment copies.
    """
    book, created = Book.objects.get_or_create(
        isbn=isbn,
        defaults={'title': title, 'author': author, 'copies': copies},
    )
    if not created:
        book.copies += copies
        book.save(update_fields=['copies'])
    return book, created


def remove_book(isbn):
    """
    Remove a book from the catalog. Blocks removal if active loans exist.
    """
    book = Book.objects.get(isbn=isbn)
    if book.transactions.filter(is_active=True).exists():
        raise BookInUseError(
            f"Cannot remove '{book.title}' while copies are on loan."
        )
    book.delete()
