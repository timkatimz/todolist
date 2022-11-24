import pytest


@pytest.mark.django_db
# @pytest.mark.skip
def test_delete_user(client):
    """Тест на проверку удаления пользователя"""
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

    login_user_response = client.post(
        '/core/login',
        {'username': 'tim', 'password': 'tim12234567'},
        content_type='application/json')

    user_delete_response = client.delete(
        '/core/profile',
    )

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 201
    assert user_delete_response.status_code == 204
