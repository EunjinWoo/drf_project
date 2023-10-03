# articles/tests.py

from django.urls import reverse # name 값을 이용해서 해당 path를 가져오는 코드. 그래서 url이 바뀌더라도 name만 같으면 그냥 사용할 수 있게.
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

# 이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

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

    def test_create_article(self):
        response = self.client.post(
            path=reverse("article_view"),
            data=self.article_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        # self.assertEqual(response.data["meaasge"], "글 작성 완료!") # 메시지 response가 있을 때는 이렇게 확인도 가능.
        self.assertEqual(response.status_code, 200)

    def test_create_article_with_image(self):
        # 임시 이미지 파일 생성
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = "image.png"
        image_file = get_temporary_image(temp_file)
        image_file.seek(0) # image의 첫번째 frame을 받아옴.
        self.article_data["image"] = image_file

        #전송
        response = self.client.post(
            path=reverse("article_view"),
            data=encode_multipart(data = self.article_data, boundary=BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        self.assertEqual(response.status_code, 200)