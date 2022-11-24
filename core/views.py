from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import CreateUserSerializer, LoginSerializer, ProfileSerializer, \
    UpdatePasswordSerializer


class SignupView(CreateAPIView):
    """Ручка для регистрации нового пользователя"""
    serializer_class = CreateUserSerializer


class LoginView(CreateAPIView):
    """Ручка для входа пользователя"""
    serializer_class = LoginSerializer

    def perform_create(self, serializer):
        """Метод производит вход(login) пользователя"""
        login(request=self.request, user=serializer.save())


class ProfileView(RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и выхода пользователя"""
    serializer_class = ProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user

    def destroy(self, request, *args, **kwargs):
        """Метод производит выход(logout) пользователя"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(UpdateAPIView):
    """Ручка для смены пароля пользователя"""
    permission_classes = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user
