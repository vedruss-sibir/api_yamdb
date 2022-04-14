from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES = (
        ('admin', 'администратор'),
        ('moderator', 'модератор'),
        ('user', 'пользователь'),
    )


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    role = models.CharField(
        'Пользовательская роль',
        choices=ROLES,
        max_length=15,
        default='user',
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=100,
        null=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    def __str__(self):
        return str(self.username)
