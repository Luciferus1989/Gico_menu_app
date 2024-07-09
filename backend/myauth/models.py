from django.db import models
from django.contrib.auth.models import AbstractUser


def avatar_directory_path(instance: "CustomUser", filename: str) -> str:
    return "user/user_{pk}/avatars/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions',
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_directory_path, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    def get_fullName(self):
        return f"{self.first_name} {self.last_name}"

    def update_name(self, full_name):
        full_name_parts = full_name.split()
        self.first_name = full_name_parts[0] if full_name_parts else ''
        self.last_name = ' '.join(full_name_parts[1:]) if len(full_name_parts) > 1 else ''
