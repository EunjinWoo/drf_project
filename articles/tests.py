# articles/tests.py

from django.urls import reverse # name 값을 이용해서 해당 path를 가져오는 코드. 그래서 url이 바뀌더라도 name만 같으면 그냥 사용할 수 있게.
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

# Create your tests here.
class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'email': 'john@test.com', 'password': 'johnpassword'}
        cls.article_data = {'title':'some title', 'content':'some content'}
        cls.user = User.objects.create_user('john@test.com', 'johnpassword')

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    # def setUp(self): # 이 부분을 위처럼 바꿈.
    #     self.user_data = {'email': 'john@test.com', 'password': 'johnpassword'}
    #     self.article_data= {'title':'some title', 'content':'some content'}
    #     self.user = User.objects.create_user('john@test.com', 'johnpassword')
    #     self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']

    def test_fail_if_not_logged_in(self): # 앞에 test 붙어있어야 manage.py test 그 돌렸을 때 돌아감.
        url = reverse("article_view")
        response = self.client.post(url, self.article_data)
        self.assertEqual(response.status_code, 401)
