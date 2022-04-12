from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken


class UsersViewSet(viewsets.ModelViewSet):
    pass


class SignUpAPI(APIView):
    pass


class TokenAPI(APIView):
    pass


class MeAPI(APIView):
    pass
