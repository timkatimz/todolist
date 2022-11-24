import pytest


@pytest.fixture
def create_login_user(client):
    """Фикстура создания и логин пользователя"""
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
def create_another_user(client):
    """Фикстура создания и логин второго пользователя"""
    user_data = {
        'username': 'tim2',
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

    return create_user_response


@pytest.fixture
def create_board(client, create_login_user):
    """Фикстура создания доски"""
    create_board_response = client.post(
        '/goals/board/create',
        data={'title': 'test board'},
        content_type='application/json')
    return create_board_response


@pytest.fixture
def create_category(client, create_board):
    """Фикстура создания категории"""
    create_category = client.post('/goals/goal_category/create',
                                  {'title': 'test category',
                                   'board': create_board.data["id"]},
                                  format='json')

    return create_category


@pytest.fixture
def create_goal(client, create_category):
    """Фикстура создания цели"""
    create_goal = client.post('/goals/goal/create',
                              {'title': 'new goal', 'category': create_category.data['id']},
                              content_type='application/json')
    return create_goal
