from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, UserProfile, Comment, Code, Snippet, Like


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    snippet_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        # put in proper order
        fields = "__all__"

    def get_snippet_count(self, obj):
        return {
            "public": obj.user.snippets.filter(visibility="public").count(),
            "private": obj.user.snippets.filter(visibility="private").count(),
            "total": obj.user.snippets.count(),
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "snippet",
            "comment_text",
            "created_at",
            "updated_at",
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            "id",
            "user",
            "snippet",
            "is_liked",
            "created_at",
            "updated_at",
        )


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = (
            "id",
            "title",
            "file_name",
            "description",
            "language",
            "code_content",
            "snippet",
            "created_at",
            "updated_at",
        )


class SnippetReadSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    liked_by = LikeSerializer(many=True)
    codes = CodeSerializer(many=True)

    codes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    liked_by_count = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = (
            "id",
            "owner",
            "visibility",
            "title",
            "description",
            "language",
            "codes_count",
            "codes",
            "comments_count",
            "comments",
            "liked_by_count",
            "liked_by",
            "created_at",
            "updated_at",
        )

    def get_codes_count(self, obj):
        return obj.codes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_liked_by_count(self, obj):
        return obj.liked_by.count()


class SnippetWriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    codes = CodeSerializer(many=True)

    class Meta:
        model = Snippet
        fields = "__all__"

    def create(self, validated_data):
        codes = validated_data.pop("codes")

        snippet = Snippet.objects.create(**validated_data)

        for code in codes:
            Code.objects.create(**code, snippet_id=snippet.id)

        return snippet
