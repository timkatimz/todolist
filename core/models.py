from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Класс модели пользователя"""
    list_display = ('last_name', 'first_name', 'username', 'email')
    list_filter = ('last_name', 'first_name', 'username', 'email')

    class Meta:
        """Мета-класс для корректного отображения полей пользователя в админ панели"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
