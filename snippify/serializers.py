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


class SnippetReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Snippet
        fields = "__all__"


class SnippetWriteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)
    codes = CodeSerializer(many=True)

    class Meta:
        model = Snippet
        fields = "__all__"

    def create(self, validated_data):
        codes = validated_data.pop("codes")
        comments = validated_data.pop("comments")

        snippet = Snippet.objects.create(**validated_data)

        for code in codes:
            Code.objects.create(**code, snippet_id=snippet.id)

        for comment in comments:
            Comment.objects.create(**comment, snippet_id=snippet.id)

        return snippet

    # def update(self, instance, validated_data):
    #     comments_data = validated_data.pop("comments", None)
    #     codes_data = validated_data.pop("codes", None)

    #     if comments_data is not None:
    #         instance.comments.set(comments_data)

    #     if codes_data is not None:
    #         instance.comments.set(codes_data)

    #     return super().update(instance, validated_data)

    # def partial_update(self, instance, validated_data):
    #     comments_data = validated_data.pop("comments", None)
    #     codes_data = validated_data.pop("codes", None)

    #     if comments_data is not None:
    #         instance.comments.set(comments_data)

    #     if codes_data is not None:
    #         instance.comments.set(codes_data)
    #     return super().partial_update(instance, validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"
