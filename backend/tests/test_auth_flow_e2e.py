from fastapi.testclient import TestClient


def test_full_registration_login_profile_refresh_flow(client: TestClient) -> None:
    register_payload = {
        'email': 'e2e-user@example.com',
        'password': 'StrongPass1',
        'name': 'End To End',
        'course': 'Data Science',
        'year_level': 'Sophomore',
        'career_goal': 'Data Engineer',
    }

    register = client.post('/api/auth/register', json=register_payload)
    assert register.status_code == 201

    login = client.post(
        '/api/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login.status_code == 200
    token = login.json()['access_token']

    profile = client.get('/api/profile/me', headers={'Authorization': f'Bearer {token}'})
    assert profile.status_code == 200
    assert profile.json()['name'] == 'End To End'

    update = client.put(
        '/api/profile/me',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'End To End Updated',
            'course': 'Data Science',
            'year_level': 'Junior',
            'career_goal': 'Machine Learning Engineer',
        },
    )
    assert update.status_code == 200

    refresh = client.post('/api/auth/refresh')
    assert refresh.status_code == 200
    assert refresh.json()['access_token']


def test_protected_route_returns_unauthorized_without_token(client: TestClient) -> None:
    response = client.get('/api/profile/me')
    assert response.status_code == 401


def test_refresh_allows_recovery_after_access_token_failure(client: TestClient) -> None:
    register_payload = {
        'email': 'refresh-recovery@example.com',
        'password': 'StrongPass1',
        'name': 'Recovery User',
        'course': 'Computer Science',
        'year_level': 'Senior',
        'career_goal': 'Platform Engineer',
    }

    register = client.post('/api/auth/register', json=register_payload)
    assert register.status_code == 201

    login = client.post(
        '/api/auth/login',
        json={'email': register_payload['email'], 'password': register_payload['password']},
    )
    assert login.status_code == 200

    unauthorized_profile = client.get('/api/profile/me', headers={'Authorization': 'Bearer invalid-token'})
    assert unauthorized_profile.status_code == 401

    refreshed = client.post('/api/auth/refresh')
    assert refreshed.status_code == 200
    new_token = refreshed.json()['access_token']

    authorized_profile = client.get('/api/profile/me', headers={'Authorization': f'Bearer {new_token}'})
    assert authorized_profile.status_code == 200
