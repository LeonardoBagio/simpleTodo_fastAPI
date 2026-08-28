from http import HTTPStatus


def test_list_statuses(client, token):
    response = client.get(
        '/catalog/statuses',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    statuses = response.json()['statuses']
    expected = 8
    assert len(statuses) == expected
    # Ordenado por sort_order; primeiro é o default.
    assert statuses[0]['code'] == 'nao_iniciada'
    assert statuses[0]['group'] == 'a_fazer'
    assert {s['group'] for s in statuses} == {
        'a_fazer',
        'em_andamento',
        'concluidos',
    }


def test_list_categories(client, token):
    response = client.get(
        '/catalog/categories',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    categories = response.json()['categories']
    expected = 8
    assert len(categories) == expected
    assert categories[0]['code'] == 'hotfix'


def test_list_statuses_without_token(client):
    response = client.get('/catalog/statuses')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
