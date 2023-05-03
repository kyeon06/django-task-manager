from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Task, SubTask
from accounts.models import User

class MyTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="danbi", team='단비')

    # 업무 생성 TEST
    """
    1. 한개 이상의 팀을 설정
    2. 업무를 생성하는 팀이 반드시 하위 업무에 포함되지 않아도 됨
    3. 정해진 팀 외에 다른 팀에 부여 못함
    """
    def test_create_task(self):
        url = '/task/'
        data = {
            "create_user": self.user.pk,
            "team": self.user.team,
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

    # # 업무 수정 TEST
    # """
    # 1. 업무 수정 시 하위 업무 담당 팀도 수정 가능
    # 2. 하지만 완료된 하위 업무가 있다면 무시
    # 3. 작성자 외에 수정 불가능
    # 4. 모든 하위 업무가 완료가 되면 상위 업무는 자동으로 완료 처리
    # 5. 하위 업무 완료 처리는 소속된 팀만 처리 가능
    # """
    # def test_update_task(self):
    #     pass

    # # 업무 삭제 TEST
    # """
    # 1. 완료된 하위 업무에 대해서는 삭제 처리 불가능
    # """
    # def test_delete_task(self):
    #     pass
    

    # # 업무 목록 조회 TEST
    # """
    # 1. 하위업무에 본인 팀이 포함되어 있다면 업무 목록에서 함께 조회가 가능
    # 2. 하위 업무의 업무 처리 여부를 확인할 수 있어야 함
    # 3. 
    # """
    # def test_list_task(self):
    #     pass