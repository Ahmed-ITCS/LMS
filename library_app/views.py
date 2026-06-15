from django.shortcuts import render, get_object_or_404
from .models import Book, Member


def book_list(request):
    books = Book.objects.all()

    return render(
        request,
        'books/list.html',
        {
            'books': books
        }
    )


