from rest_framework import serializers
from datetime import date

from reviews.models import Category, Genre, Titles, Comment, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Titles

    def validate_year(self, value):
        year = date.today().year
        if year > value:
            raise serializers.ValidationError("год произведения из будущего")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = 'id', 'text', 'author', 'score', 'pub_date'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = 'id', 'text', 'author', 'pub_date'
        model = Comment
