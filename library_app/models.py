from django.db import models


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


