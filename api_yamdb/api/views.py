from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Titles, Genre, Category, Review
from users.models import User
from .permissions import IsAdminOrReadOnly
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    RegistrationSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer,
    TokenSerializer,
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request, *args, **kwargs):
    serializer = RegistrationSerializer(data=request.data, many=False)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    try:
        user, created = User.objects.get_or_create(
            username=username,
            email=email.lower()
        )
    except IntegrityError:
        return Response(
            {'message': 'Имя пользователя или почта уже используются.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = default_token_generator.make_token(user)
    send_mail(
        "API_YAMDB: Confirmation code",
        f"confirmation_code: {token}",
        DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    token = serializer.validated_data['confirmation_code']
    if not default_token_generator.check_token(user, token):
        return Response(
            'Ошибочный код подтверждения', status=status.HTTP_400_BAD_REQUEST
        )
    refresh = str(RefreshToken.for_user(user).access_token)
    return Response(
        {"token": refresh},
        status=status.HTTP_200_OK)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    # permission_classes = (AuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        return genre


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (AuthorOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return category


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = (AuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "genre", "category", "year")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        id = self.kwargs.get('id')
        title = get_object_or_404(Titles, pk=id)
        return title.reviews.all()

    def perform_create(self, serializer):
        id = self.kwargs.get('id')
        title = get_object_or_404(Titles, pk=id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        id = self.kwargs.get('id')
        review = get_object_or_404(Review, pk=id)
        return review.comments.all()

    def perform_create(self, serializer):
        id = self.kwargs.get('id')
        review = get_object_or_404(Review, pk=id)
        serializer.save(author=self.request.user, review=review)
