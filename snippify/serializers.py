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
        fields = "__all__"

    # def get_snippet_count(self, obj):
    #     return {
    #         "public": obj.user.snippets.filter(visibility="public").count(),
    #         "private": obj.user.snippets.filter(visibility="private").count(),
    #         "total": obj.user.snippets.count(),
    #     }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = "__all__"
        read_only_fields = ("comments, liked_by",)


class SnippetReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    codes = CodeSerializer(many=True)

    class Meta:
        model = Snippet
        fields = "__all__"
        read_only_fields = ("comments, liked_by",)

    def create(self, validated_data):
        codes = validated_data.pop("codes")

        snippet = Snippet.objects.create(**validated_data)

        for code in codes:
            Code.objects.create(**code, snippet=snippet)

        return snippet


class SnippetWriteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    codes = CodeSerializer(many=True, read_only=True)

    class Meta:
        model = Snippet
        fields = "__all__"

    def create(self, validated_data):
        codes = validated_data.pop("books")

        snippet = Snippet.objects.create(**validated_data)

        for code in codes:
            Code.objects.create(**code, snippetId=snippet)

        return snippet


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
