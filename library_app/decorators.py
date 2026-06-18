from functools import wraps

from django.contrib.auth.decorators import login_required, user_passes_test


def is_librarian(user):
    return user.is_authenticated and user.is_staff


def librarian_required(view_func):
    """Restrict a view to authenticated staff (librarians)."""
    @wraps(view_func)
    @login_required
    @user_passes_test(is_librarian)
    def wrapper(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)

    return wrapper
