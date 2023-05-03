from django.urls import path
from .views import TaskViewSet

task_list = TaskViewSet.as_view({
    'get' : 'list',
    'post' : 'create'
})

task_detail = TaskViewSet.as_view({
    'get' : 'retrieve',
    'put' : 'update',
    'delete' : 'destroy'
})

urlpatterns = [
    path('task/', task_list),
    path('task/<int:pk>/', task_detail),
]