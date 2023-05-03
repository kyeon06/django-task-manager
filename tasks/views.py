from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, SubTask
from .serializers import TaskSerializer, SubTaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    # task 생성
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid()
        serializer.save()
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        # 로그인한 유저의 업무 목록 조회
        user = self.request.user
        queryset = Task.objects.filter(create_user=user)

        addsets = list(SubTask.objects.filter(team=user.team))

        for addset in addsets:
            result_set = queryset | Task.objects.filter(id=addset.task_id)
        return result_set
    
