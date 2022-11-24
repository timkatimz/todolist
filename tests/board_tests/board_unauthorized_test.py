import pytest


@pytest.mark.django_db
@pytest.mark.skip
def test_unauthorized_user_board(client, create_board):
    """Тест просмотр, редактирование и удаления доски неавторизованным пользователем"""
    client.logout()

    board_list_result = client.get(f'/goals/board/list')
    board_detail_response = client.get(f'/goals/board/{int(create_board.data["id"])}')
    board_delete_response = client.delete(f'/goals/board/{int(create_board.data["id"])}')
    update_board_response = client.put(f'/goals/board/{int(create_board.data["id"])}',
                                       data={'participants': [],
                                             'title': "updated board",
                                             "is_deleted": False},
                                       content_type='application/json')

    assert create_board.status_code == 201
    assert board_delete_response.status_code == 403
    assert board_detail_response.status_code == 403
    assert update_board_response.status_code == 403
    assert board_list_result.status_code == 403
