import pytest

from core.models import User


@pytest.mark.django_db
@pytest.mark.skip
def test_sign_up(client):
    user_data = {
        'username': 'tim',
        'first_name': 'Tim',
        'last_name': 'Semeneev',
        'email': 'tim@semeneev.ru',
        'password': 'tim12234567',
        'password_repeat': 'tim12234567'
    }

    create_user_response = client.post(
        '/core/signup',
        data=user_data,
        content_type='application/json')

    user = User.objects.filter(username=user_data['username']).first()

    assert create_user_response.status_code == 201
    assert user.username == user_data['username']

