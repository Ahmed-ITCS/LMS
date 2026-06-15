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
def member_list(request):
    members = Member.objects.all()

    return render(
        request,
        'library_app/member_list.html',
        {
            'members': members
        }
    )


def member_detail(request, member_id):
    member = get_object_or_404(
        Member,
        member_id=member_id
    )

    return render(
        request,
        'library_app/member_detail.html',
        {
            'member': member
        }
    )


