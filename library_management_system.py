#!/usr/bin/env python3
"""
Group G - Main Application Interface (CLI)
Purpose: Combine all modules into a single menu-driven application.
Responsibilities: Provide user-friendly menu and actions.
"""

from auth_system import authenticate, is_librarian
from book import Book
from issue_return import issue_book, return_book
from library import Library
from member import Member
from search import search_books


def seed_demo_data(library, members):
  """Load sample books and members for the CLI demo."""
  library.add_book(Book('9780132350884', 'Clean Code', 'Robert C. Martin', 3))
  library.add_book(Book('9780201633610', 'Design Patterns', 'Gang of Four', 2))
  library.add_book(Book('9781491950358', 'Fluent Python', 'Luciano Ramalho', 4))
  members['MEM001'] = Member('MEM001', 'Alice Johnson')
  members['MEM002'] = Member('MEM002', 'Bob Smith')


def print_menu(user):
  print('\n--- Athenaeum Library (CLI) ---')
  print('1. List all books')
  print('2. Search books')
  if is_librarian(user):
    print('3. Add book')
    print('4. Issue book')
    print('5. Return book')
  print('0. Exit')


def main():
  library = Library()
  members = {}
  current_user = None

  seed_demo_data(library, members)

  while not current_user:
    username = input('\nUsername: ').strip()
    password = input('Password: ').strip()
    if authenticate(username, password):
      current_user = username
      print(f'Welcome, {current_user}!')
    else:
      print('Invalid credentials. Try librarian/librarian123 or alice/password123')

  while True:
    print_menu(current_user)
    choice = input('Choose an option: ').strip()

    if choice == '1':
      books = library.list_books()
      if not books:
        print('No books in catalog.')
      for book in books:
        print(f'  {book} — {book.copies} copies')

    elif choice == '2':
      query = input('Search: ').strip()
      results = search_books(library, query)
      if not results:
        print('No matches found.')
      for book in results:
        print(f'  {book} — {book.copies} copies')

    elif choice == '3' and is_librarian(current_user):
      isbn = input('ISBN: ').strip()
      title = input('Title: ').strip()
      author = input('Author: ').strip()
      copies = int(input('Copies: ').strip() or '1')
      library.add_book(Book(isbn, title, author, copies))
      print('Book added.')

    elif choice == '4' and is_librarian(current_user):
      isbn = input('Book ISBN: ').strip()
      member_id = input('Member ID: ').strip()
      member = members.get(member_id)
      if not member:
        print('Member not found.')
      elif issue_book(library, isbn, member):
        print('Book issued.')
      else:
        print('Issue failed — no copies available.')

    elif choice == '5' and is_librarian(current_user):
      isbn = input('Book ISBN: ').strip()
      member_id = input('Member ID: ').strip()
      member = members.get(member_id)
      if not member:
        print('Member not found.')
      elif return_book(library, isbn, member):
        print('Book returned.')
      else:
        print('Return failed — book not on loan.')

    elif choice == '0':
      print('Goodbye!')
      break

    else:
      print('Invalid option.')


if __name__ == '__main__':
  main()
