from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    TokenAPI, MeAPI, SignUpAPI, TitlesViewSet, CategoryViewSet, 
    GenreViewSet, CommentViewSet, ReviewViewSet
)

app_name = 'api'

router = DefaultRouter()
router.register("titles", TitlesViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="category")
router.register("genres", GenreViewSet, basename="genre")
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
                CommentViewSet, basename='reviews')

urlpatterns = [
    path('v1/auth/token/', TokenAPI.as_view()),
    path('v1/users/me/', MeAPI.as_view()),
    path('v1/auth/signup/', SignUpAPI.as_view()),
    path('v1/', include(router.urls)),
]
