"""Group D - BookTransaction model."""

from django.db import models

from library_app.models.book import Book
from library_app.models.member import Member


class BookTransaction(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='transactions'
    )
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='borrowed_books'
    )
    issue_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        status = "Active" if self.is_active else "Returned"
        return f"{self.member} - {self.book.title} ({status})"
