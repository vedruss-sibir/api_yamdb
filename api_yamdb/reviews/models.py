from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

from .utils import year_of_creation_validator


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name="Категория")
    slug = models.SlugField(
        max_length=50, blank=True, unique=True, verbose_name="slug категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Название категорий"

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Жанр")
    slug = models.SlugField(
        max_length=100, blank=True, unique=True, verbose_name="slug жанра"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Название жанров"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название произведения"
    )
    year = models.SmallIntegerField(
        validators=[year_of_creation_validator],
        verbose_name="Год произведения"
    )
    description = models.TextField(blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
    )

    class Meta:
        verbose_name = "Название произведения"
        verbose_name_plural = "Название произведений"

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения",
    )
    text = models.TextField(verbose_name="Я думаю это ...")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор"
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Минимальная оценка - 1"),
            MaxValueValidator(10, message="Максимальная оценка - 10"),
        ]
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(fields=["author", "title"],
                                    name="author_review")
        ]
        verbose_name = 'Отзыв о произведении'
        verbose_name_plural = 'Отзывы о произведении'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв о произведении",
    )
    text = models.TextField(verbose_name="Ваш комментарий")
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'
