from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Titles, Genre, Category, Review
from users.models import User
from .permissions import IsAdminOrReadOnly

from api_yamdb.settings import EMAIL_FROM
from .serializers import (
    GenreSerializer,
    CategorySerializer,
    RegistrationSerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    TokenSerializer,
)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=user
            )
            serializer.is_valid(raise_exception=True)
            if request.data.get('role') is not None and user.is_user:
                return Response(serializer.data)
            self.perform_update(serializer)

            if getattr(user, '_prefetched_objects_cache', None):
                user._prefetched_objects_cache = {}
            return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email'],
        password=serializer.validated_data['email']
    )
    user.save()
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Register code',
        f'{confirmation_code}',
        EMAIL_FROM,
        [serializer.data['email']],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )
    return Response(
        {'message': 'Пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    # permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        return genre


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return category


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    # permission_classes = (IsAuthorOrReadOnlyPermission,)
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
