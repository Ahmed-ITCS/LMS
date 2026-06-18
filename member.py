"""
Group B - Member Module
Purpose: Manage library members.
Responsibilities: Track member ID, name, and borrowed books.
"""


class Member:
  """Represents a library member who can borrow books."""

  def __init__(self, member_id, name):
    self.member_id = member_id
    self.name = name
    self.borrowed_books = []

  def __str__(self):
    return f"{self.name} ({self.member_id})"

  def __repr__(self):
    return f"Member(member_id={self.member_id!r}, name={self.name!r})"
