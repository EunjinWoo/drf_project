# articles/views.py

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db.models.query_utils import Q
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, ArticleListSerializer, ArticleCreateSerializer, CommentSerializer, CommentCreateSerializer

# Create your views here.

class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated] # login 해야 들어갈 수 있도록 하는 것. 위에 permissions import 되어 있어야 함.

    def get(self, request):
        q = Q()
        # request.user # login한 사람의 데이터가 옴.
        # request.user.followings.all() # 로그인한 사용자가 팔로우하고 있는 모든 사용자의 query set이 돌아옴.
        for user in request.user.followings.all():
            q.add(Q(user=user),q.OR)
        feeds = Article.objects.filter(q)
        serializer = ArticleListSerializer(feeds, many=True)
        return Response(serializer.data)  

class ArticleView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인 해주세요."}, 401)

        serializer = ArticleCreateSerializer(data=request.data)
        # print(request.user)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    def get(self, request, article_id):
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, article_id):
        # article = Article.objects.get(id=article_id)
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            serializer = ArticleCreateSerializer(article, data=request.data)
            if serializer.is_valid():
                serializer.save() # 여기는 이미 기존 article에 user가 저장되어있어서 따라고 request.user를 안 해줘도 됨.
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user == article.user:
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

class CommentView(APIView):
    def get(self, request, article_id):
        article = Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, article_id):
        serializer = CommentCreateSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            serializer.save(user=request.user, article_id=article_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetailView(APIView):
    def put(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            serializer = CommentCreateSerializer(comment, data=request.data) # update
            if serializer.is_valid():
                serializer.save() # 여기는 이미 기존 article에 user가 저장되어있어서 따라고 request.user를 안 해줘도 됨.
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, article_id, comment_id):
        comment = get_object_or_404(Comment, id=article_id)
        if request.user == comment.user:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

class LikeView(APIView):
    def post(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        if request.user in article.likes.all():
            article.likes.remove(request.user)
            return Response("unlike했습니다", status=status.HTTP_200_OK)
        else:
            article.likes.add(request.user)
            return Response("like했습니다", status=status.HTTP_200_OK)