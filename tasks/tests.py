from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status
from .models import Task, SubTask
from accounts.models import User
from .serializers import TaskCreateSerializer, TaskUpdateSerializer
from .views import TaskView

from rest_framework.test import APIClient

class MyTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.user1 = User.objects.create(username="danbi", team='단비', password='password')
        self.user2 = User.objects.create(username="blabla", team='블라블라', password='password')

        self.task1 = Task.objects.create(
            create_user = self.user1,
            team = self.user1.team,
            title = "test title1",
            content = "test content1",
            is_complete = False,
        )
        self.task2 = Task.objects.create(
            create_user = self.user2,
            team = self.user2.team,
            title = "test title2",
            content = "test content2",
            is_complete = False,
        )

        self.subtask1 = SubTask.objects.create(
            team = "다래",
            task = self.task1,
        )
        self.subtask2 = SubTask.objects.create(
            team = "단비",
            task = self.task1
        )

    # 업무 생성 TEST
    """
    1. 한개 이상의 팀을 설정
    2. 업무를 생성하는 팀이 반드시 하위 업무에 포함되지 않아도 됨
    3. 정해진 팀 외에 다른 팀에 부여 못함
    """
    def test_create_task(self):
        url = '/task/'
        data = {
            "create_user": self.user1.pk,
            "team": self.user1.team,
            "title": "test title",
            "content": "test content",
            "is_complete": False,
            "subtasks": [
                {
                    "team" : "다래"
                },
                {
                    "team" : "블라블라"
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)


    # 업무 목록 조회 TEST
    """
    1. 하위업무에 본인 팀이 포함되어 있다면 업무 목록에서 함께 조회가 가능
    2. 하위 업무의 업무 처리 여부를 확인할 수 있어야 함
    3. 
    """
    def test_task_list(self):
        response = self.client.get('/task/')
        tasks = Task.objects.all()
        serializer = TaskCreateSerializer(tasks, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    def test_task_detail(self):
        response = self.client.get(f'/task/{self.task1.id}/')
        task = Task.objects.get(id=self.task1.id)
        serializer = TaskCreateSerializer(task)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


    # 업무 수정 TEST
    """
    1. 업무 수정 시 하위 업무 담당 팀도 수정 가능
    2. 하지만 완료된 하위 업무가 있다면 무시
    3. 작성자 외에 수정 불가능
    4. 모든 하위 업무가 완료가 되면 상위 업무는 자동으로 완료 처리
    5. 하위 업무 완료 처리는 소속된 팀만 처리 가능
    """
    def test_update_task(self):

        url = f'/task/{self.task1.id}/'
        data = {
            "create_user": self.task1.create_user.pk,
            "team": self.task1.team,
            "title": "put title",
            "content": "put content",
            "is_complete": False,
            "subtasks": [
                {
                    "id" : self.subtask1.pk,
                    "team" : self.subtask1.team,
                    "is_complete": False,
                    "completed_date": None
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)


    # # 업무 삭제 TEST
    # """
    # 1. 완료된 하위 업무에 대해서는 삭제 처리 불가능
    # """
    # def test_delete_task(self):
    #     pass
    
