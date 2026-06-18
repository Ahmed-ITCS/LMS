from django.db import models

from library_app.models import Book


def search_books(query_string):
    """
    Search books by title, author, or exact ISBN match.
    """
    if not query_string:
        return Book.objects.none()

    return Book.objects.filter(
        models.Q(title__icontains=query_string)
        | models.Q(author__icontains=query_string)
        | models.Q(isbn__exact=query_string)
    )
