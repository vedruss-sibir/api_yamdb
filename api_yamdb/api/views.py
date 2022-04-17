from django.shortcuts import get_object_or_404

from rest_framework.pagination import LimitOffsetPagination
from rest_framework import viewsets, filters

from api.permissions import IsAuthorOrReadOnlyPermission
from reviews.models import Titles, User, Genre, Category, Review
from api.serializers import (
    GenreSerializer,
    CategorySerializer,
    TitlesSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs.get("slug"))
        return genre


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get("slug"))
        return category


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name", "genre", "category", "year")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Titles, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Titles, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)
