from django.urls import path
from .views import TaskView, SubTaskView

urlpatterns = [
    path('', TaskView.as_view(), name='task_list'), # 조회, 생성
    path('<int:pk>/', TaskView.as_view(), name='task_detail'), # 특정 task 조회, 삭제, 수정

    path('subtask/<int:pk>/', SubTaskView.as_view()),
]