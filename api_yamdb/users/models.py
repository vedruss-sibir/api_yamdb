from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_roles = (
        ('admin', 'администратор'),
        ('moderator', 'модератор'),
        ('user', 'пользователь'),
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Электронная почта',
        unique=True,
    )
    user_role = models.CharField(
        'Пользовательская роль',
        choices=user_roles,
        max_length=15,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
    )
    biography = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return str(self.username)
