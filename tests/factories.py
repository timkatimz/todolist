import factory.django
from factory import Faker

from goals.models import Board


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = Faker('name')

