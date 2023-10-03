# users/views.py

from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from users.models import User
from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer

# Create your views here.

class UserView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입 완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followers.all(): # model의 related name이 followers
            you.followers.remove(me)
            return Response("unfollow했습니다", status=status.HTTP_200_OK)
        else:
            you.followers.add(me)
            return Response("follow했습니다", status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request.user)
        # user.is_admin = True
        # user.save() -> 뭐 이런 식으로 user 내부의 DB 조작 가능. 하지만 DB 조작하는 것은 get 보다는 post로 하는 것이 좋기에 주석처리함. 
        return Response("get 요청")

class ProfileView(APIView):
    # permission_classes = [permissions.IsAuthenticated] # login 해야 들어갈 수 있도록 하는 것.
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)