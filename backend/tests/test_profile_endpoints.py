from fastapi.testclient import TestClient

REGISTRATION_PAYLOAD = {
    'email': 'profile-user@example.com',
    'password': 'StrongPass1',
    'name': 'Profile User',
    'course': 'Information Technology',
    'year_level': 'Senior',
}


def auth_headers(client: TestClient) -> dict[str, str]:
    register = client.post('/api/auth/register', json=REGISTRATION_PAYLOAD)
    assert register.status_code == 201

    login = client.post(
        '/api/auth/login',
        json={'email': REGISTRATION_PAYLOAD['email'], 'password': REGISTRATION_PAYLOAD['password']},
    )
    assert login.status_code == 200
    token = login.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def get_first_career_id(client: TestClient, headers: dict[str, str]) -> int:
    careers = client.get('/api/careers', headers=headers)
    assert careers.status_code == 200
    return careers.json()[0]['id']


def test_profile_endpoints_require_authentication(client: TestClient) -> None:
    response = client.get('/api/profile/me')
    assert response.status_code == 401


def test_get_and_update_profile(client: TestClient) -> None:
    headers = auth_headers(client)

    current = client.get('/api/profile/me', headers=headers)
    assert current.status_code == 200
    assert current.json()['name'] == REGISTRATION_PAYLOAD['name']
    assert current.json()['career_id'] is None

    update_payload = {
        'name': 'Updated Name',
        'course': 'Computer Science',
        'year_level': 'Junior',
    }
    updated = client.put('/api/profile/me', json=update_payload, headers=headers)
    assert updated.status_code == 200
    assert updated.json()['name'] == 'Updated Name'
    assert updated.json()['course'] == 'Computer Science'

    persisted = client.get('/api/profile/me', headers=headers)
    assert persisted.status_code == 200
    assert persisted.json()['name'] == 'Updated Name'


def test_set_and_update_career(client: TestClient) -> None:
    headers = auth_headers(client)

    first_career_id = get_first_career_id(client, headers)
    selected = client.post('/api/profile/career', json={'career_id': first_career_id}, headers=headers)
    assert selected.status_code == 200
    assert selected.json()['career_id'] == first_career_id
    assert selected.json()['career'] is not None

    careers = client.get('/api/careers', headers=headers).json()
    second_career_id = careers[1]['id']
    updated = client.put('/api/profile/career', json={'career_id': second_career_id}, headers=headers)
    assert updated.status_code == 200
    assert updated.json()['career_id'] == second_career_id
    assert updated.json()['career']['id'] == second_career_id


def test_set_career_rejects_unknown_career_id(client: TestClient) -> None:
    headers = auth_headers(client)
    invalid = client.post('/api/profile/career', json={'career_id': 99999}, headers=headers)
    assert invalid.status_code == 404
    assert invalid.json()['detail'] == 'Career not found'
