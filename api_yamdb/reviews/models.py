from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, blank=True, unique=True)

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.TextField(verbose_name="Название произведения")
    year = models.DateTimeField(verbose_name="год произведения")
    description = models.TextField(max_length=400)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="genre",
        verbose_name="Жанр",
    )
    category = models.OneToOneField(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="category",
    )
