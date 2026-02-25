from fastapi.testclient import TestClient

VALID_REGISTRATION = {
    'email': 'student@example.com',
    'password': 'StrongPass1',
    'name': 'Student Name',
    'course': 'Computer Science',
    'year_level': 'Junior',
    'career_goal': 'Software Engineer',
}


def register_user(client: TestClient, payload: dict | None = None) -> None:
    body = payload or VALID_REGISTRATION
    response = client.post('/api/auth/register', json=body)
    assert response.status_code == 201


def test_registration_valid_and_duplicate_email(client: TestClient) -> None:
    register_user(client)

    duplicate = client.post('/api/auth/register', json=VALID_REGISTRATION)
    assert duplicate.status_code == 400
    assert duplicate.json()['detail'] == 'Email already registered'


def test_registration_rejects_weak_password(client: TestClient) -> None:
    payload = VALID_REGISTRATION | {'password': 'weak'}
    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 422
    error_messages = [error['msg'] for error in response.json()['detail']]
    assert any('Password must be at least 8 characters with uppercase, lowercase, and numbers' in msg for msg in error_messages)


def test_registration_rejects_invalid_email(client: TestClient) -> None:
    payload = VALID_REGISTRATION | {'email': 'invalid-email'}
    response = client.post('/api/auth/register', json=payload)

    assert response.status_code == 422


def test_login_success_and_invalid_credentials(client: TestClient) -> None:
    register_user(client)

    invalid = client.post(
        '/api/auth/login',
        json={'email': VALID_REGISTRATION['email'], 'password': 'WrongPass1'},
    )
    assert invalid.status_code == 401
    assert invalid.json()['detail'] == 'Invalid email or password'

    valid = client.post(
        '/api/auth/login',
        json={'email': VALID_REGISTRATION['email'], 'password': VALID_REGISTRATION['password']},
    )
    assert valid.status_code == 200
    assert valid.json()['access_token']
    assert 'refresh_token=' in valid.headers.get('set-cookie', '')


def test_login_rate_limit_after_failed_attempts(client: TestClient) -> None:
    register_user(client)

    for _ in range(5):
        attempt = client.post(
            '/api/auth/login',
            json={'email': VALID_REGISTRATION['email'], 'password': 'WrongPass1'},
        )
        assert attempt.status_code == 401

    blocked = client.post(
        '/api/auth/login',
        json={'email': VALID_REGISTRATION['email'], 'password': 'WrongPass1'},
    )
    assert blocked.status_code == 429
    assert blocked.json()['detail'] == 'Too many login attempts. Try again later.'


def test_refresh_requires_cookie_and_issues_new_access_token(client: TestClient) -> None:
    register_user(client)

    unauthorized = client.post('/api/auth/refresh')
    assert unauthorized.status_code == 401

    client.cookies.set('refresh_token', 'invalid')
    invalid = client.post('/api/auth/refresh')
    assert invalid.status_code == 401

    client.cookies.clear()
    login = client.post(
        '/api/auth/login',
        json={'email': VALID_REGISTRATION['email'], 'password': VALID_REGISTRATION['password']},
    )
    assert login.status_code == 200

    refreshed = client.post('/api/auth/refresh')
    assert refreshed.status_code == 200
    assert refreshed.json()['access_token']
