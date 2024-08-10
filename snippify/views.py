# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView
from .models import UserProfile, Comment, Code, Snippet, Like
from .serializers import (
    UserProfileSerializer,
    CommentSerializer,
    CodeSerializer,
    SnippetReadSerializer,
    SnippetWriteSerializer,
    LikeSerializer,
)


class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"message": "This is a test endpoint"}, status=HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ["list", "get", "patch"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ["list", "get", "post", "patch", "delete"]


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    http_method_names = ["list", "get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SnippetReadSerializer
        return SnippetWriteSerializer


class LikeSnippetViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ["list", "get", "post", "patch", "delete"]


class SnippetsByUserView(ListAPIView):
    serializer_class = SnippetReadSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Snippet.objects.filter(owner=user_id)
