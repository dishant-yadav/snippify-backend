import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, is_admin=False, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email), name=name, is_admin=is_admin
        )
        user.set_password(password)
        user.save(using=self._db)
        UserProfile.objects.create(user=user)
        return user

    def create_superuser(self, email, name, is_admin=True, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email, password=password, name=name, is_admin=is_admin
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# Custom User Model.
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name="Email",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "is_admin"]

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True)
    bio = models.TextField(null=True)
    tech_stack = models.JSONField(null=True)

    @property
    def snippet_count(self):
        snippet_count = {
            "public": self.user.snippets.filter(visibility="public").count(),
            "private": self.user.snippets.filter(visibility="private").count(),
            "total": self.user.snippets.count(),
        }
        return snippet_count

    def __str__(self):
        return self.user.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, related_name="commented_posts", on_delete=models.CASCADE
    )
    snippet = models.ForeignKey(
        "snippify.Snippet",
        related_name="comments",
        on_delete=models.CASCADE,
        blank=True,
    )
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.name}"


class Snippet(models.Model):
    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    language = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, related_name="snippets", on_delete=models.CASCADE)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def like_count(self):
        return self.liked_by.count()

    def __str__(self):
        return self.title


class Code(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    description = models.TextField()
    language = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_content = models.TextField()
    # number_of_lines = models.IntegerField()
    snippet = models.ForeignKey(
        Snippet, related_name="codes", on_delete=models.CASCADE, blank=True
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name="liked_posts", on_delete=models.CASCADE)
    snippet = models.ForeignKey(
        Snippet, related_name="liked_by", on_delete=models.CASCADE
    )
    is_liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Likes {self.id}"
