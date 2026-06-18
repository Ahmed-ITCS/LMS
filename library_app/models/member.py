"""Group B - Member model."""

from django.contrib.auth.models import User
from django.db import models


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='library_profile'
    )
    member_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.member_id})"
