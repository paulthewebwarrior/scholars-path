from fastapi.testclient import TestClient

REGISTRATION_PAYLOAD = {
    'email': 'profile-user@example.com',
    'password': 'StrongPass1',
    'name': 'Profile User',
    'course': 'Information Technology',
    'year_level': 'Senior',
    'career_goal': 'Product Manager',
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


def test_profile_endpoints_require_authentication(client: TestClient) -> None:
    response = client.get('/api/profile/me')
    assert response.status_code == 401


def test_get_and_update_profile(client: TestClient) -> None:
    headers = auth_headers(client)

    current = client.get('/api/profile/me', headers=headers)
    assert current.status_code == 200
    assert current.json()['name'] == REGISTRATION_PAYLOAD['name']

    update_payload = {
        'name': 'Updated Name',
        'course': 'Computer Science',
        'year_level': 'Junior',
        'career_goal': 'Engineering Manager',
    }
    updated = client.put('/api/profile/me', json=update_payload, headers=headers)
    assert updated.status_code == 200
    assert updated.json()['name'] == 'Updated Name'
    assert updated.json()['course'] == 'Computer Science'

    persisted = client.get('/api/profile/me', headers=headers)
    assert persisted.status_code == 200
    assert persisted.json()['career_goal'] == 'Engineering Manager'
