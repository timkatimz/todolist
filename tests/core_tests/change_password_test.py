import pytest


@pytest.mark.django_db
def test_update_password(client):
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

    new_password = 'timtimtim'

    update_password_response = client.put(
        '/core/update_password',
        {'old_password': user_data['password'], 'new_password': new_password},
        content_type='application/json')

    login_response = client.post(
        '/core/login',
        {'username': 'tim', 'password': new_password},
        content_type='application/json')

    assert create_user_response.status_code == 201
    assert login_user_response.status_code == 201
    assert update_password_response.status_code == 200
    assert login_response.status_code == 201
