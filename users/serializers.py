# users/serializers.py

from dataclasses import field
from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.serializers import ArticleListSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True) # 이렇게 하면 다 user의 email로 뜸.
    # followers = serializers.PrimaryKeyRelatedField(many=True, read_only=True) # 이렇게 하면 다 user_id로 뜸 팔로워가.
    followings = serializers.StringRelatedField(many=True)
    article_set = ArticleListSerializer(many=True)
    like_articles = ArticleListSerializer(many=True) # models.py에서 related_name이 like_articles로 되어있음.

    class Meta:
        model = User
        fields = ("id", "email", "followings", "followers", "article_set", "like_articles")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data) # DB에 전달
        print(validated_data)
        password = user.password
        user.set_password(password) # password hashing
        print(user.password)
        user.save() # DB에 전달
        return user
    
    def update(self, validated_data):
        user = super().create(validated_data) # DB에 전달
        password = user.password
        user.set_password(password) # password hashing
        user.save() # DB에 전달
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token