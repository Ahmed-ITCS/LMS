from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


class Member(models.Model):
    member_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=100)
    borrowed_books = models.ManyToManyField(Book, blank=True)

    def __str__(self):
        return self.name