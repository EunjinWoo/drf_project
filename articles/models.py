# articles/models.py

from django.db import models
from users.models import User

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 1대다 관계 (User는 여러개 article 작성 가능)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name="like_articles")

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 1대다 관계 (User는 여러개 article 작성 가능)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comment_set") # CASCADE -> 게시글이 지워지면 댓글도 다 지워지도록. / related_name은 default로 comment_set로 지정되어있어서 안써도 됨.
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content) # admin page에서 그 타이틀처럼 내용 딱 보이게 하는 기능.
