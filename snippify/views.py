# Create your views here.
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from .models import UserProfile, Comment, Code, Snippet, Like
from .serializers import (
    UserProfileSerializer,
    CommentSerializer,
    CodeSerializer,
    SnippetReadSerializer,
    SnippetWriteSerializer,
    LikeSerializer,
)


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
    serializer_class = SnippetReadSerializer

    """
    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SnippetReadSerializer
        return SnippetWriteSerializer
    """


class LikeSnippetView(APIView):
    def post(self, request, snippet_id):
        print(request)
        user = request.user
        try:
            snippet = Snippet.objects.get(id=snippet_id)
        except Snippet.DoesNotExist:
            return Response(
                {"error": "Snippet does not exist"}, status=HTTP_404_NOT_FOUND
            )
        try:
            like = Like.objects.get(user=user, snippet=snippet)
            like.is_liked = not like.is_liked
        except Like.DoesNotExist:
            like = Like.objects.create(user=user, snippet=snippet)

        like.save()

        serializer = LikeSerializer(like)

        return Response(serializer.data, status=HTTP_201_CREATED)
