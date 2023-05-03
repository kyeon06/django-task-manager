from django.db import models
from django.contrib.auth.models import AbstractUser
from task_manager.my_settings import TEAM_CHOICE

class User(AbstractUser):
    team = models.CharField(max_length=30, choices=TEAM_CHOICE, blank=True, null=True)
    first_name = None
    last_name =None