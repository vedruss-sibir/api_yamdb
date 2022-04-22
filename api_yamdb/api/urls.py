from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api"

router = DefaultRouter()
router.register(r"titles", views.TitlesViewSet, basename="titles")
router.register(r"categories", views.CategoryViewSet, basename="category")
router.register(r"genres", views.GenreViewSet, basename="genre")
router.register(r"users", views.UsersViewSet, basename="users")
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    views.ReviewViewSet,
    basename="reviews",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    views.CommentViewSet,
    basename="reviews",
)

urlpatterns = [
    path("v1/auth/signup/", views.create_user, name="register"),
    path("v1/auth/token/", views.create_token, name="token"),
    path("v1/", include(router.urls)),
]
