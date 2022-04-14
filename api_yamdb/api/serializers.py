from rest_framework import serializers
from datetime import date

from reviews.models import Category, Genre, Titles


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
