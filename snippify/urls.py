from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    SnippetViewSet,
    CodeViewSet,
    CommentViewSet,
    LikeSnippetViewSet,
    TestView,
)

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"snippets", SnippetViewSet, basename="snippet")
router.register(r"codes", CodeViewSet, basename="code")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"likes", LikeSnippetViewSet, basename="comment")

urlpatterns = [ 
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("test/", TestView.as_view()),
    path("", include(router.urls)),
]

urlpatterns += router.urls
