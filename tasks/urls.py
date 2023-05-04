from django.urls import path
from .views import TaskView

urlpatterns = [
    path('', TaskView.as_view()), # 조회, 생성
    path('<int:pk>/', TaskView.as_view()), # 특정 task 조회, 삭제, 수정
]