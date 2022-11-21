import pytest


@pytest.fixture
@pytest.mark.django_db
def get_token(client, django_user_model):
    username = 'tim'
    password = 'Tim12234567'

    django_user_model.objects.create_user(
        username=username,
        password=password,
    )

    login_data = {
        'username': username,
        'password': password
    }

    response = client.post(
        '/core/login/',
        {'username': username, 'password': password},
        format='json'
    )

    token = response.data['token']
    return token
