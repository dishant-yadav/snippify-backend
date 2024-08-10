import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
import pathlib


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
        if not user.is_admin:
            UserProfile.objects.create(user=user, id=user.id)

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
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class UserProfile(models.Model):

    def user_directory_path(instance, filename):
        file_name = instance.user.id
        file_extension = pathlib.Path(filename).suffix
        file_full_name = f"user_{file_name}{file_extension}"
        images_dir = "profiles"
        return f"{images_dir}/{file_full_name}"

    def tech_stack_default_value():
        return ["React", "Django"]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, upload_to=user_directory_path)
    bio = models.TextField(default="I am full stack developer!!!")
    tech_stack = models.JSONField(default=tech_stack_default_value)

    # social links

    def __str__(self):
        return self.user.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserProfile,
        related_name="commented_posts",
        on_delete=models.CASCADE,
        # editable=False,
    )
    snippet = models.ForeignKey(
        "snippify.Snippet",
        related_name="comments",
        on_delete=models.CASCADE,
        blank=True,
        # editable=False,
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
    owner = models.ForeignKey(
        UserProfile,
        related_name="snippets",
        on_delete=models.CASCADE,
        # editable=False,
    )
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES)

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
        Snippet,
        related_name="codes",
        on_delete=models.CASCADE,
        blank=True,
        # editable=False,
    )

    def __str__(self):
        return self.title


class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserProfile,
        related_name="liked_posts",
        on_delete=models.CASCADE,
        # editable=False,
    )
    snippet = models.ForeignKey(
        Snippet,
        related_name="liked_by",
        on_delete=models.CASCADE,
        # editable=False,
    )
    is_liked = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Likes {self.id}"

    class Meta:
        unique_together = ("user", "snippet")


class Save(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserProfile,
        related_name="saved_posts",
        on_delete=models.CASCADE,
        # editable=False,
    )
    snippet = models.ForeignKey(
        Snippet,
        related_name="saved_by",
        on_delete=models.CASCADE,
        # editable=False,
    )
    is_saved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Saved {self.id}"

    class Meta:
        unique_together = ("user", "snippet")
