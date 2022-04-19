from uuid import uuid4

from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Titles, Genre, Category, Review
from users.models import User
from .permissions import IsAdmin
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    RegistrationSerializer,
    CreateTokenSerializer
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail = False,
        methods=['GET', 'PATCH'],
        url_path='me',
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer
    )
    def get_user(self, request, pk=None):
        user = get_object_or_404(User, pk=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role = user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    real_username = User.objects.filter(username=username)
    real_email = User.objects.filter(email=email)
    if real_username.exists() or real_email.exists():
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, email=email)
    user.confirmation_code = uuid4()
    user.save()
    send_mail(
            'Ваш код подтверждения:',
            f'{user.confirmation_code}',
            DEFAULT_FROM_EMAIL,
            [f'{email}'],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_token(request):
    serializer = CreateTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code == user.confirmation_code:
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )



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
