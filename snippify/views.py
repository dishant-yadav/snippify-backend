# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
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
    def get(self, request):
        return Response({"message": "This is a test endpoint"}, status=HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CodeViewSet(viewsets.ModelViewSet):
    queryset = Code.objects.all()
    serializer_class = CodeSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SnippetReadSerializer
        return SnippetWriteSerializer


class LikeSnippetViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    http_method_names = ("get", "list", "post")
