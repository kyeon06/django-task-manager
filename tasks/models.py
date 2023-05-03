from django.db import models
from accounts.models import User
from task_manager.my_settings import TEAM_CHOICE

class Task(models.Model):
    id = models.AutoField(primary_key=True, db_column='task_id',verbose_name='업무번호')
    create_user = models.ForeignKey(User, verbose_name='생성자', db_column='create_user', on_delete=models.CASCADE)
    team = models.CharField(max_length=30, choices=TEAM_CHOICE ,verbose_name='담당팀')
    title = models.CharField(max_length=255, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    is_complete = models.BooleanField(default=False, verbose_name='완료여부')
    completed_date = models.DateTimeField(verbose_name='완료날짜')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정날짜')

class SubTask(models.Model):
    id = models.AutoField(primary_key=True, db_column='sub_id', verbose_name='하위업무번호')
    team = models.CharField(max_length=30, choices=TEAM_CHOICE , verbose_name='담당팀')
    is_complete = models.BooleanField(default=False, verbose_name='완료여부')
    completed_date = models.DateTimeField(verbose_name='완료날짜')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성날짜')
    modified_at = models.DateTimeField(auto_now=True, verbose_name='수정날짜')

    task_id = models.ForeignKey(Task, db_column='task_id', verbose_name='업무번호', on_delete=models.CASCADE) 