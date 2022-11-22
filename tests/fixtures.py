import pytest


@pytest.fixture
def create_login_user(client):
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
        {'username': user_data['username'], 'password': user_data['password']},
        content_type='application/json')

    return create_user_response, login_user_response


@pytest.fixture
def create_board(client, create_login_user):
    create_board_response = client.post(
        '/goals/board/create',
        data={'title': 'test board'},
        content_type='application/json')
    return create_board_response


@pytest.fixture
def create_category(client, create_board):
    create_category = client.post('/goals/goal_category/create',
                                  {'title': 'test category',
                                   'board': create_board.data["id"]},
                                  format='json')

    return create_category


