from uuid import uuid4

from datetime import date

from rest_framework import serializers

from reviews.models import Category, Genre, Titles, Comment, Review
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Genre


class TitlesSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Titles

    def validate_year(self, value):
        year = date.today().year
        if year > value:
            raise serializers.ValidationError(
                "год произведения не может быть из будущего"
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = "__all__"
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, default='user')

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name'
        )
        role = serializers.CharField(read_only=True)

    def create(self, validated_data):
        confirmation_code = uuid4()
        user = User.objects.create(
            **validated_data,
            confirmation_code=confirmation_code
        )
        return user

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Не допустимое имя пользователя'
            )
        return value
