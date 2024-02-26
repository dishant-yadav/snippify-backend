from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    SnippetViewSet,
    CodeViewSet,
    CommentViewSet,
    LikeSnippetView,
)

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"snippets", SnippetViewSet, basename="snippet")
router.register(r"codes", CodeViewSet, basename="code")
router.register(r"snippets/comment", CommentViewSet, basename="comment")

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("", include(router.urls)),
    # path("snippet/like", LikeSnippetView.as_view(), name="like"),
]

urlpatterns += router.urls
