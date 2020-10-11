from django.contrib.auth import authenticate, login, logout
from rest_framework import status, views, generics, permissions
from rest_framework.response import Response

from accounts.serializer import UserLoginLogoutSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginLogoutSerializer

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
