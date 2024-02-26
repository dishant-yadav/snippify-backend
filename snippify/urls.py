from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    SnippetViewSet,
    CodeViewSet,
    CommentViewSet,
    LikeSnippetView,
    TestView,
)

router = DefaultRouter()
router.register(r"users/", UserProfileViewSet, basename="user")
router.register(r"snippets/", SnippetViewSet, basename="snippet")
router.register(r"codes/", CodeViewSet, basename="code")
router.register(r"snippets/comments/", CommentViewSet, basename="comment")
router.register(r"snippets/likes/", LikeSnippetView, basename="comment")

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
    path("test/", TestView.as_view()),
    # path("snippet/like", LikeSnippetView.as_view(), name="like"),
]

urlpatterns += router.urls
