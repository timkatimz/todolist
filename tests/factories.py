import factory.django
from factory import Faker

from core.models import User
from goals.models import Board, GoalCategory

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'tim'
    first_name = 'Tim'
    last_name = 'Semeneev'
    email = 'tim@semeneev.ru'
    password = 'tim12234567'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('sentence')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = Faker('sentence')
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

