def test_category_create(client):
    create_category = client.post(
        '/goals/goal_category/create'

    )
