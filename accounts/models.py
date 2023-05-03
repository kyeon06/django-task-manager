from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    team = models.CharField(max_length=30, blank=True, null=True)
    first_name = None
    last_name =None