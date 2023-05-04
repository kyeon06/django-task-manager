from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User

class MyTestCase(APITestCase):
    def setUp(self):
        pass

    # 회원가입 test
    def test_create_user(self):
        url = '/user/signup/'
        data = {'username' : 'danbi', 'password' : 'testpass', 'team' : '단비'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)