# users/test.py

from django.urls import reverse # name 값을 이용해서 해당 path를 가져오는 코드. 그래서 url이 바뀌더라도 name만 같으면 그냥 사용할 수 있게.
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

# Create your tests here.
class UserRegistrationTest(APITestCase):
    def test_registration(self):
        url = reverse("user_view")
        user_data = {
            "username": "testuser",
            "fullname": "테스터",
            "email": "test@testuser.com",
            "password": "password",
        }
        response = self.client.post(url, user_data)
        self.assertEqual(response.status_code, 201)

class LoginUserTest(APITestCase):
    def setUp(self):

        self.data = {'email': 'john@test.com', 'password': 'johnpassword'}
        self.user = User.objects.create_user('john@test.com', 'johnpassword')

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        # print(response.data["access"]) # access token이 옴.
        self.assertEqual(response.status_code, 200)

    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(
            path=reverse("user_view"),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response.data['email'], self.data['email'])