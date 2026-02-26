from fastapi.testclient import TestClient

REGISTRATION_PAYLOAD = {
    'email': 'career-user@example.com',
    'password': 'StrongPass1',
    'name': 'Career User',
    'course': 'Computer Science',
    'year_level': 'Junior',
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


def test_careers_list_is_available_and_sorted(client: TestClient) -> None:
    headers = auth_headers(client)

    response = client.get('/api/careers', headers=headers)
    assert response.status_code == 200
    payload = response.json()

    assert len(payload) == 5
    names = [item['name'] for item in payload]
    assert names == sorted(names)
    assert names == [
        'Cybersecurity Specialist',
        'Data Analyst',
        'Doctor',
        'Engineer',
        'Software Developer',
    ]


def test_get_single_career_supports_slug(client: TestClient) -> None:
    headers = auth_headers(client)

    response = client.get('/api/careers/software-developer', headers=headers)
    assert response.status_code == 200
    assert response.json()['name'] == 'Software Developer'


def test_get_career_skills_and_subjects(client: TestClient) -> None:
    headers = auth_headers(client)

    skills_response = client.get('/api/careers/software-developer/skills', headers=headers)
    assert skills_response.status_code == 200
    skills = skills_response.json()
    assert any(item['name'] == 'Programming' for item in skills)

    programming_skill_id = next(item['id'] for item in skills if item['name'] == 'Programming')
    subjects_response = client.get(
        f'/api/careers/software-developer/skills/{programming_skill_id}/subjects',
        headers=headers,
    )
    assert subjects_response.status_code == 200

    subjects = subjects_response.json()
    subject_names = {subject['name'] for subject in subjects}
    assert 'Introduction to Programming' in subject_names
    assert 'Software Development' in subject_names
    assert 'Human Anatomy' not in subject_names


def test_invalid_career_or_skill_returns_not_found(client: TestClient) -> None:
    headers = auth_headers(client)

    invalid_career = client.get('/api/careers/not-a-real-career', headers=headers)
    assert invalid_career.status_code == 404

    invalid_skill = client.get('/api/careers/software-developer/skills/99999/subjects', headers=headers)
    assert invalid_skill.status_code == 404
