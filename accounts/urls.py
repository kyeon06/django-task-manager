from django.urls import path, include
from .views import UserCreate

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='user-create'), # 회원가입
]