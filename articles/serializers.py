# articles/serializers.py

from rest_framework import serializers

from articles.models import Article, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        # obj -> article 객체?임. 
        return obj.user.email

    class Meta:
        model = Comment
        # fields = '__all__'
        exclude = ("article", )

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",) # 하나만 있으면 반드시 마지막에 comma 넣어줘야함.

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comment_set = CommentSerializer(many=True) # 무조건 comment_set 여야함. s 더 붙이고 이런거 안됨. related_name이 기본적으로 comment_set으로 설정되어있기 때문.
    likes = serializers.StringRelatedField(many=True) # users/models.py 가면 user의 str field는 self.email로 설정해뒀기 때문. 이렇게 하면 누가 like 했는지가 user_id가 아니라 이메일 주소로 나옴.

    def get_user(self, obj):
        # obj -> article 객체?임. 
        return obj.user.email

    class Meta:
        model = Article
        fields = '__all__'


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("title", "image", "content")


class ArticleListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        # obj -> article 객체?임. 
        return obj.user.email

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comment_set.count()

    class Meta:
        model = Article
        fields = ("pk", "title", "image", "updated_at", "user", "likes_count", "comments_count")