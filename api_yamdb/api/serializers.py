from datetime import date

from django.db.models import Avg

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Genre, Title, Comment, Review, GenreTitle
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # fields = "__all__"
        exclude = ("id",)
        model = Category


class GenreTitleSerializer(serializers.ModelSerializer):
    genre = serializers.ReadOnlyField(source="genre.id")
    title = serializers.ReadOnlyField(source="title.id")

    class Meta:
        model = GenreTitle
        fields = ("genre", "title")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = "__all__"
        exclude = ("id",)
        model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", many=False, queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
            "rating",
        )

    # def validate_year(self, value):
    #     year = date.today().year
    #     if year > value:
    #         raise serializers.ValidationError(
    #             "год произведения не может быть из будущего"
    #         )
    #     return value

    def get_rating(self, obj):
        reviews = Review.objects.filter(title=obj).all()
        rating = obj.reviews.aggregate(Avg("score")).get("score__avg")
        return rating


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = "__all__"
        model = Review
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(), fields=("author", "title")
            )
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = "__all__"
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, default="user")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "role",
            "bio",
        )
        role = serializers.CharField(read_only=True)


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Невозможно использовать имя "me" для регистрации.'
            )
        return value


class CreateTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r"^[\w.@+-]+$", max_length=150, required=True
    )
    confirmation_code = serializers.CharField(required=True)
