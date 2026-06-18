"""Group A - Book model."""

from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True, primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
