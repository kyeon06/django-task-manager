from django.urls import path
from .views import TaskView

urlpatterns = [
    path('', TaskView.as_view()), # 조회
    path('<int:pk>/', TaskView.as_view()), # 특정 task 조회
]