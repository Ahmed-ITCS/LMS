from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from library_app.decorators import librarian_required
from library_app.forms import (
    AddBookForm,
    IssueBookForm,
    LoginForm,
    MemberRegistrationForm,
    ReturnBookForm,
    SearchForm,
)
from library_app.models import Book, BookTransaction, Member
from library_app.services.catalog import BookInUseError, add_book, remove_book
from library_app.services.search import search_books
from library_app.services.transactions import (
    InsufficientStockError,
    TransactionNotActiveError,
    issue_book,
    return_book,
)


def dashboard_view(request):
    stats = {
        'total_books': Book.objects.count(),
        'total_copies': Book.objects.aggregate(total=Sum('copies'))['total'] or 0,
        'total_members': Member.objects.count(),
        'active_loans': BookTransaction.objects.filter(is_active=True).count(),
    }
    recent_transactions = BookTransaction.objects.select_related(
        'book', 'member', 'member__user'
    ).order_by('-issue_date')[:5]

    my_loans = []
    if request.user.is_authenticated and hasattr(request.user, 'library_profile'):
        my_loans = request.user.library_profile.borrowed_books.filter(
            is_active=True
        ).select_related('book')

    return render(request, 'library_app/dashboard.html', {
        'stats': stats,
        'recent_transactions': recent_transactions,
        'my_loans': my_loans,
    })


def catalog_view(request):
    books = Book.objects.annotate(
        active_loans=Count('transactions', filter=Q(transactions__is_active=True))
    ).order_by('title')
    return render(request, 'library_app/catalog.html', {'books': books})


@librarian_required
def add_book_view(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            book, created = add_book(
                data['isbn'],
                data['title'],
                data['author'],
                data['copies'],
            )
            if created:
                messages.success(request, f"Added '{book.title}' to the catalog.")
            else:
                messages.success(
                    request,
                    f"ISBN already exists. Increased copies of '{book.title}' to {book.copies}.",
                )
            return redirect('catalog')
    else:
        form = AddBookForm()

    return render(request, 'library_app/add_book.html', {'form': form})


@librarian_required
@require_http_methods(['POST'])
def remove_book_view(request, isbn):
    try:
        remove_book(isbn)
        messages.success(request, 'Book removed from the catalog.')
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
    except BookInUseError as exc:
        messages.error(request, str(exc))

    return redirect('catalog')


def search_view(request):
    form = SearchForm(request.GET or None)
    results = Book.objects.none()

    if form.is_valid() and form.cleaned_data.get('query'):
        results = search_books(form.cleaned_data['query'])

    return render(request, 'library_app/search.html', {
        'form': form,
        'results': results,
    })


@librarian_required
def issue_view(request):
    if request.method == 'POST':
        form = IssueBookForm(request.POST)
        if form.is_valid():
            try:
                txn = issue_book(
                    form.cleaned_data['isbn'].isbn,
                    form.cleaned_data['member'].member_id,
                )
                messages.success(
                    request,
                    f"Issued '{txn.book.title}' to {txn.member}.",
                )
                return redirect('dashboard')
            except InsufficientStockError as exc:
                messages.error(request, str(exc))
    else:
        form = IssueBookForm()

    return render(request, 'library_app/issue.html', {'form': form})


@librarian_required
def return_view(request):
    if request.method == 'POST':
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            try:
                txn = return_book(form.cleaned_data['transaction'].pk)
                messages.success(
                    request,
                    f"Returned '{txn.book.title}' from {txn.member}.",
                )
                return redirect('dashboard')
            except TransactionNotActiveError as exc:
                messages.error(request, str(exc))
    else:
        form = ReturnBookForm()

    return render(request, 'library_app/return.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        messages.success(request, 'Welcome back!')
        return redirect('dashboard')

    return render(request, 'library_app/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@require_http_methods(['GET', 'POST'])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = MemberRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Account created successfully.')
        return redirect('dashboard')

    return render(request, 'library_app/register.html', {'form': form})


@login_required
def my_account_view(request):
    member = get_object_or_404(Member, user=request.user)
    loans = member.borrowed_books.select_related('book').order_by('-issue_date')
    active_loan_count = loans.filter(is_active=True).count()
    return render(request, 'library_app/my_account.html', {
        'member': member,
        'loans': loans,
        'active_loan_count': active_loan_count,
    })
