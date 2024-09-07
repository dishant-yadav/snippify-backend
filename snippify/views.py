# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK
from rest_framework.generics import ListAPIView
from .models import UserProfile, Comment, Code, Snippet, Like, Save
from .serializers import (
    UserProfileSerializer,
    CodeSerializer,
    SnippetReadSerializer,
    SnippetWriteSerializer,
    LikeReadSerializer,
    LikeWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    SaveReadSerializer,
    SaveWriteSerializer,
)


class TestView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return Response({"message": "This is a test endpoint"}, status=HTTP_200_OK)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    http_method_names = ["list", "get", "patch"]


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
    http_method_names = ["list", "get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return LikeReadSerializer
        return LikeWriteSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ["list", "get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return CommentReadSerializer
        return CommentWriteSerializer


class SaveSnippetViewSet(viewsets.ModelViewSet):
    queryset = Save.objects.all()
    http_method_names = ["list", "get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SaveReadSerializer
        return SaveWriteSerializer


class SnippetsByUserView(ListAPIView):
    serializer_class = SnippetReadSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Snippet.objects.filter(owner=user_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "snippets_count": queryset.count(),
            "snippets": serializer.data,
        }

        return Response(response_data)


class SaveSnippetsByUserView(ListAPIView):
    serializer_class = SaveReadSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return Save.objects.filter(user=user_id).filter(is_saved=True)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            "saved_snippets_count": queryset.count(),
            "saved_snippets": serializer.data,
        }

        return Response(response_data)
