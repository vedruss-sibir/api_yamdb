from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

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
        blank=True,
    )
    category = models.OneToOneField(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        related_name="category",
        blank=True,
    )


class Review(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
