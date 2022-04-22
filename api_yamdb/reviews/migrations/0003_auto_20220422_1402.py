# Generated by Django 2.2.16 on 2022-04-22 08:02

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220422_0528'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Название категории'},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'verbose_name': 'Название жанра'},
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальная оценка - 1'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка - 10')]),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, null=True, related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
        migrations.DeleteModel(
            name='GenreTitle',
        ),
    ]
