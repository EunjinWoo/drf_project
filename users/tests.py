# users/test.py

from django.urls import reverse # name 값을 이용해서 해당 path를 가져오는 코드. 그래서 url이 바뀌더라도 name만 같으면 그냥 사용할 수 있게.
from rest_framework.test import APITestCase
from rest_framework import status

# Create your tests here.
class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse("user_view")
        user_data = {
            "username": "testuser",
            "fullname": "테스터",
            "email": "test1@testuser.com",
            "password": "password",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)