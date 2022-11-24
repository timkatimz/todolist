from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, AuthenticationFailed, NotAuthenticated


from core.models import User


class PasswordField(serializers.CharField):
    """Django-форма для пароля"""
    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора для создания пользователя"""
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True)

    class Meta:
        """Мета-класс для указания модели для сериализатора и полей модели сериализатора"""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate(self, attrs: dict):
        """Метод проверяет, совпадают ли введенные пароли"""
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data):
        """Метод удаляет значение поля [password_repeat], хэширует пароль и создает пользователя"""
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора для проверки данных пользователя на входе"""
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        """Мета-класс для указания модели для сериализатора и полей модели сериализатора"""
        model = User
        fields = '__all__'

    def create(self, validated_data: dict):
        """Метод проводит аутентификацию пользователя"""
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password']
        )):
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора пользователя"""
    class Meta:
        """Мета-класс для указания модели для сериализатора и полей модели сериализатора"""
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class UpdatePasswordSerializer(serializers.Serializer):
    """Класс модели сериализатора для смены пароля пользователя"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    old_password = PasswordField(required=True)
    new_password = PasswordField(required=True)

    def validate(self, attrs: dict):
        """Метод проверяет, совпадает ли значение поля ['old_password'] с действующим
        паролем"""
        if not (user := attrs['user']):
            raise NotAuthenticated
        if not user.check_password(attrs['old_password']):
            raise ValidationError({'old_password': 'field is incorrect'})
        return attrs

    def update(self, instance: User, validated_data: dict) -> User:
        """Метод хэширует значение поля ['new_password'] и обновляет
        пароль пользователя в БД"""
        instance.password = make_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance
