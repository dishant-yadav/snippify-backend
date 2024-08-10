from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    SnippetViewSet,
    CodeViewSet,
    CommentViewSet,
    LikeSnippetViewSet,
    TestView,
    SnippetsByUserView,
    SaveSnippetViewSet,
    SaveSnippetsByUserView,
)

router = DefaultRouter()
router.register(r"users", UserProfileViewSet, basename="user")
router.register(r"snippets", SnippetViewSet, basename="snippet")
router.register(r"codes", CodeViewSet, basename="code")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"likes", LikeSnippetViewSet, basename="like")
router.register(r"saved-snippet", SaveSnippetViewSet, basename="save")

urlpatterns = [
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("test/", TestView.as_view()),
    path(
        "snippets/user/<uuid:user_id>/",
        SnippetsByUserView.as_view(),
        name="snippets-by-user",
    ),
    path(
        "save-snippets/user/<uuid:user_id>/",
        SaveSnippetsByUserView.as_view(),
        name="save-snippets-by-user",
    ),
    path("", include(router.urls)),
]

urlpatterns += router.urls
