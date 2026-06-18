from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from django.utils import timezone

from library_app.models import Book, BookTransaction, Member
from library_app.services.catalog import add_book
from library_app.services.transactions import issue_book, return_book


BOOKS = [
    ('9780132350884', 'Clean Code', 'Robert C. Martin', 4),
    ('9780201633610', 'Design Patterns', 'Gang of Four', 3),
    ('9780596517748', 'JavaScript: The Good Parts', 'Douglas Crockford', 5),
    ('9781449368781', 'Learning Python', 'Mark Lutz', 6),
    ('9781491950358', 'Fluent Python', 'Luciano Ramalho', 3),
    ('9780134685991', 'Effective Java', 'Joshua Bloch', 4),
    ('9780135166307', 'Clean Architecture', 'Robert C. Martin', 2),
    ('9781617294945', 'Spring in Action', 'Craig Walls', 3),
    ('9781492041137', 'Fundamentals of Software Architecture', 'Richards & Ford', 2),
    ('9781098111812', 'Learning Go', 'Jon Bodner', 4),
    ('9781492052584', 'Python for Data Analysis', 'Wes McKinney', 5),
    ('9780134193064', 'The Go Programming Language', 'Donovan & Kernighan', 2),
]

MEMBERS = [
    {
        'username': 'alice',
        'password': 'password123',
        'member_id': 'MEM001',
        'first_name': 'Alice',
        'last_name': 'Johnson',
        'email': 'alice@library.edu',
    },
    {
        'username': 'bob',
        'password': 'password123',
        'member_id': 'MEM002',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'email': 'bob@library.edu',
    },
    {
        'username': 'carol',
        'password': 'password123',
        'member_id': 'MEM003',
        'first_name': 'Carol',
        'last_name': 'Williams',
        'email': 'carol@library.edu',
    },
    {
        'username': 'david',
        'password': 'password123',
        'member_id': 'MEM004',
        'first_name': 'David',
        'last_name': 'Brown',
        'email': 'david@library.edu',
    },
]

ACTIVE_LOANS = [
    ('9780132350884', 'MEM001'),
    ('9780201633610', 'MEM002'),
    ('9780596517748', 'MEM001'),
    ('9781449368781', 'MEM003'),
]

RETURNED_LOANS = [
    ('9781491950358', 'MEM002'),
    ('9780134685991', 'MEM004'),
]


class Command(BaseCommand):
    help = 'Seed the database with demo books, members, and transactions.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Remove existing library data before seeding.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing library data...')
            BookTransaction.objects.all().delete()
            Member.objects.all().delete()
            Book.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        librarian, created = User.objects.get_or_create(
            username='librarian',
            defaults={
                'email': 'librarian@library.edu',
                'first_name': 'Margaret',
                'last_name': 'Hayes',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            librarian.set_password('librarian123')
            librarian.save()
            self.stdout.write(self.style.SUCCESS('Created librarian (librarian / librarian123)'))
        else:
            self.stdout.write('Librarian account already exists.')

        for data in MEMBERS:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data['email'],
                    'first_name': data['first_name'],
                    'last_name': data['last_name'],
                },
            )
            if created:
                user.set_password(data['password'])
                user.save()

            Member.objects.get_or_create(
                user=user,
                defaults={'member_id': data['member_id']},
            )
            if created:
                self.stdout.write(f"  Created member {data['username']} / password123")

        for isbn, title, author, copies in BOOKS:
            add_book(isbn, title, author, copies)

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(BOOKS)} books.'))

        for isbn, member_id in ACTIVE_LOANS:
            if not BookTransaction.objects.filter(
                book_id=isbn, member__member_id=member_id, is_active=True
            ).exists():
                issue_book(isbn, member_id)

        for isbn, member_id in RETURNED_LOANS:
            if not BookTransaction.objects.filter(
                book_id=isbn, member__member_id=member_id, is_active=False
            ).exists():
                txn = issue_book(isbn, member_id)
                txn.issue_date = timezone.now() - timezone.timedelta(days=14)
                txn.save(update_fields=['issue_date'])
                return_book(txn.pk)
                txn.refresh_from_db()
                txn.return_date = timezone.now() - timezone.timedelta(days=2)
                txn.save(update_fields=['return_date'])

        stats = {
            'books': Book.objects.count(),
            'members': Member.objects.count(),
            'active_loans': BookTransaction.objects.filter(is_active=True).count(),
            'returned_loans': BookTransaction.objects.filter(is_active=False).count(),
        }

        self.stdout.write(self.style.SUCCESS(
            f"Seed complete — {stats['books']} books, {stats['members']} members, "
            f"{stats['active_loans']} active loans, {stats['returned_loans']} returned."
        ))
        self.stdout.write('')
        self.stdout.write('Demo accounts:')
        self.stdout.write('  Librarian: librarian / librarian123')
        self.stdout.write('  Members:   alice, bob, carol, david / password123')
