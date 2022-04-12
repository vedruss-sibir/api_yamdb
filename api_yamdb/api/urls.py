from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TokenAPI, MeAPI, SignUpAPI


app_name = "api"

router = DefaultRouter()


urlpatterns = [
    path('v1/auth/token/', TokenAPI.as_view()),
    path('v1/users/me/', MeAPI.as_view()),
    path('v1/auth/signup/', SignUpAPI.as_view()),
    path('v1/', include(router.urls)),
]
