from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField
from django.db.models.fields import BooleanField


class User(AbstractUser):
    accepted_tos = IntegerField(blank=False, default=0)
    is_banned = BooleanField(default=False)