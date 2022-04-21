from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .utils import year_of_creation_validator
from users.models import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Название категории"
    )
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, verbose_name="Жанр")
    slug = models.SlugField(max_length=100, blank=True, unique=True)

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
        through="GenreTitle",
        related_name="genre",
        verbose_name="Жанр",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="category",
        null=True,
    )
    # score = models.PositiveSmallIntegerField(
    #     verbose_name="Оценка от 1 до 10", blank=True, null=True
    # )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre} {self.title}"


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Название произведения"
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
            MinValueValidator(1, 'Минимальная оценка - 1'),
            MaxValueValidator(10, 'Максимальная оценка - 10'),
        ]
    )
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор"
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв о произведении"
    )
    text = models.TextField(verbose_name="Ваш комментарий")
    pub_date = models.DateTimeField(
        "Дата добавления",
        auto_now_add=True,
        db_index=True
    )
