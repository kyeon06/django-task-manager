from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Task, SubTask
from .serializers import TaskCreateSerializer, TaskUpdateSerializer
from rest_framework.views import APIView

class TaskView(APIView):

    # 조회
    """
    1. /task/ : 로그인한 유저가 있다면 해당 유저가 작성한 task와 하위업무로 포함된 task 조회
    2. /task/{pk} : 해당 pk에 해당하는 task의 정보 조회
    
    """
    def get(self, request, **kwargs):
        result_set = []
        if kwargs.get('pk') is None:
            if self.request.user:
                result_set = Task.objects.filter(create_user=self.request.user)

                if SubTask.objects.filter(team=self.request.user.team).exists():
                    add_queryset = list(SubTask.objects.filter(team=self.request.user.team))
                    for addset in add_queryset:
                        result_set = result_set | Task.objects.filter(id=addset.task_id)
            else:
                result_set = Task.objects.all()

            task_queryset_serializer = TaskCreateSerializer(result_set, many=True)
            return Response(task_queryset_serializer.data, status=status.HTTP_200_OK)
        else:
            task_id = kwargs.get('pk')
            task_data = Task.objects.get(id=task_id)
            task_serializer = TaskCreateSerializer(task_data)
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        

    # 생성
    """
    /task/{pk} : task를 생성한다.
    """
    def post(self, request):
        task_serializer = TaskCreateSerializer(data=request.data)

        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 수정
    """
    /task/{pk} : task를 수정한다.
    """
    def put(self, request, **kwargs):
        if kwargs.get('pk') is None:
            return Response("잘못된 접근입니다.", status=status.HTTP_400_BAD_REQUEST)
        else:
            task_id = kwargs.get('pk')
            task_object = Task.objects.get(id=task_id)

            # 작성자가 아닐 경우 수정하지 못하게 설정
            if self.request.user != task_object.create_user :
                return Response("수정권한이 없습니다.", status=status.HTTP_400_BAD_REQUEST)
            else:
                update_task_serializer = TaskUpdateSerializer(task_object, data=request.data)
                if update_task_serializer.is_valid(raise_exception=True):
                    update_task_serializer.save()
                    return Response(update_task_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("잘못된 요청입니다.", status=status.HTTP_400_BAD_REQUEST)

    # 삭제
    """
    /task/{pk} : 해당 task 삭제한다.
    """
    def delete(self, request, **kwargs):
        if kwargs.get('pk') is None:
            return Response("잘못된 요청입니다.", status=status.HTTP_400_BAD_REQUEST)
        else:
            task_id = kwargs.get('pk')
            task_object = Task.objects.get(id=task_id)
            
            # 하위 업무가 있는지 확인
            if task_object.subtasks.filter(is_complete=True).exists():
                # 완료된 작업이 있으면 삭제하지 않고 에러 메시지 반환
                return Response({'error': '하위 업무 중 완료된 작업이 있어 삭제할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # 완료된 작업이 없으면 삭제
                task_object.delete()
                return Response("삭제가 완료되었습니다.", status=status.HTTP_200_OK)