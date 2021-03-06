from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, views, generics, permissions, viewsets
from rest_framework.response import Response

from accounts.serializer import UserSerializer


class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        data = request.data
        username = data.get("username", None)
        password = data.get("password", None)

        if username and password:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            return Response({"message": "User created"}, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, format=None):
        """
        Login
        :param request: Username, Password
        :param format: {"username": "x", "password": "y"}
        :return: Message and status
        """

        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return Response({"message": "Login Success"}, status=status.HTTP_200_OK)

        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        if request.user:
            logout(request)
            return Response({"message": "Logout Success"}, status=status.HTTP_200_OK)
        return Response({"message": "You need to login first"}, status=status.HTTP_404_NOT_FOUND)
