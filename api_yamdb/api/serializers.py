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
        fields = "__all__"
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = "__all__"
        model = Comment


class RegistrationSerializer(serializers.ModelSerializer):
    queryset=User.objects.all()
    email = serializers.EmailField(
        required=True)
    username = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError("Нельзя подписаться на себя!")
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
