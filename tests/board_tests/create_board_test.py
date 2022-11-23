from datetime import datetime

import pytest

from goals.serializers import BoardSerializer


@pytest.mark.django_db
@pytest.mark.skip
def test_board_create(client, create_login_user):
    """Тест на создание доски"""
    board_create = client.post(
        '/goals/board/create',
        {'title': 'test board'},
        content_type='application/json'
    )

    expected_response = {
        "id": board_create.data['id'],
        "created": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        "updated": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
        "title": "test board",
        "is_deleted": False
    }

    assert board_create.status_code == 201
    assert board_create.data['title'] == expected_response['title']
    assert board_create.data['id'] == expected_response['id']
    assert board_create.data['created'][0:19] == expected_response['created']
    assert board_create.data['updated'][0:19] == expected_response['updated']
    assert board_create.data['is_deleted'] == expected_response['is_deleted']
