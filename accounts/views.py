from rest_framework import generics
from .serializers import UserSerializer
from .models import User

# 회원가입
class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer