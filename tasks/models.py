from django.db import models
from accounts.models import User
from task_manager.my_settings import TEAM_CHOICE

class Task(models.Model):

    create_user = models.ForeignKey(User, verbose_name='생성자', db_column='create_user', on_delete=models.CASCADE)
    team = models.CharField(max_length=30, choices=TEAM_CHOICE ,verbose_name='담당팀')
    title = models.CharField(max_length=255, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_complete = models.BooleanField(default=False, verbose_name='완료여부')
    completed_date = models.DateTimeField(verbose_name='완료날짜', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정날짜')

class SubTask(models.Model):

    team = models.CharField(max_length=30, choices=TEAM_CHOICE , verbose_name='담당팀')
    is_complete = models.BooleanField(default=False, verbose_name='완료여부')
    completed_date = models.DateTimeField(verbose_name='완료날짜', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정날짜')

    task = models.ForeignKey(Task,  related_name='subtasks', verbose_name='업무번호', on_delete=models.CASCADE) 