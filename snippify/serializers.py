from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User, UserProfile, Comment, Code, Snippet, Like, Save


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ("id", "email", "name", "password")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "email",
        )


class UserViewSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "name", "email", "image")

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        name = User.objects.get(id=obj.id).name
        return name

    def get_email(self, obj):
        email = User.objects.get(id=obj.id).email
        return email

    def get_image(self, obj):
        image = UserProfile.objects.get(id=obj.id).image
        if image:
            return image
        else:
            return ""


class UserProfileSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

    user = UserViewSerializer()
    snippets_count = serializers.SerializerMethodField()
    liked_posts = serializers.SerializerMethodField()
    liked_posts_count = serializers.SerializerMethodField()
    commented_posts_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "bio",
            "tech_stack",
            "image",
            "snippets_count",
            "snippets",
            "liked_posts_count",
            "liked_posts",
            "commented_posts_count",
            "commented_posts",
        ]

    def get_snippets_count(self, obj):
        snippet_count = {
            "public": obj.snippets.filter(visibility="public").count(),
            "private": obj.snippets.filter(visibility="private").count(),
            "total": obj.snippets.count(),
        }
        return snippet_count

    def get_liked_posts(self, obj):
        return obj.liked_posts.filter(is_liked=True)

    def get_liked_posts_count(self, obj):
        return obj.liked_posts.filter(is_liked=True).count()

    def get_commented_posts_count(self, obj):
        return obj.commented_posts.count()


class CommentReadSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

    user = UserViewSerializer()

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


class CommentWriteSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

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


class LikeReadSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

    user = UserViewSerializer()

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


class LikeWriteSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

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


class SaveReadSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

    user = UserViewSerializer()

    class Meta:
        model = Save
        fields = (
            "id",
            "user",
            "snippet",
            "is_saved",
            "created_at",
            "updated_at",
        )


class SaveWriteSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

    class Meta:
        model = Save
        fields = (
            "id",
            "user",
            "snippet",
            "is_saved",
            "created_at",
            "updated_at",
        )


class CodeSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id
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
    # prevent changing of foreign key id

    comments = CommentReadSerializer(many=True)
    codes = CodeSerializer(many=True)
    owner = UserViewSerializer()

    codes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    liked_by = serializers.SerializerMethodField()
    liked_by_count = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = (
            "id",
            "owner",
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

    def get_liked_by(self, obj):
        return obj.liked_by.filter(is_liked=True)

    def get_liked_by_count(self, obj):
        return obj.liked_by.filter(is_liked=True).count()


class SnippetWriteSerializer(serializers.ModelSerializer):
    # prevent changing of foreign key id

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
