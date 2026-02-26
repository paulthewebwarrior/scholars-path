from fastapi.testclient import TestClient

REGISTRATION_PAYLOAD = {
    'email': 'career-reco@example.com',
    'password': 'StrongPass1',
    'name': 'Recommendation User',
    'course': 'Computer Science',
    'year_level': 'Junior',
}

ASSESSMENT_PAYLOAD = {
    'study_hours': 1,
    'sleep_hours': 5,
    'phone_usage_hours': 8,
    'social_media_hours': 6,
    'gaming_hours': 4,
    'breaks_per_day': 1,
    'coffee_intake': 4,
    'exercise_minutes': 5,
    'stress_level': 8,
    'focus_score': 30,
    'attendance_percentage': 65,
    'assignments_completed_per_week': 1,
    'final_grade': 62,
    'grade_opt_in': True,
}


def register_and_get_auth(client: TestClient, payload: dict[str, str]) -> tuple[dict[str, str], int]:
    register = client.post('/api/auth/register', json=payload)
    assert register.status_code == 201

    login = client.post(
        '/api/auth/login',
        json={'email': payload['email'], 'password': payload['password']},
    )
    assert login.status_code == 200
    token = login.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    profile = client.get('/api/profile/me', headers=headers)
    assert profile.status_code == 200
    return headers, profile.json()['id']


def select_software_developer_career(client: TestClient, headers: dict[str, str]) -> int:
    careers = client.get('/api/careers', headers=headers)
    assert careers.status_code == 200
    software_developer = next(item for item in careers.json() if item['name'] == 'Software Developer')

    selected = client.post('/api/profile/career', json={'career_id': software_developer['id']}, headers=headers)
    assert selected.status_code == 200
    return software_developer['id']


def test_career_aligned_recommendations_require_matching_user(client: TestClient) -> None:
    headers_one, user_one_id = register_and_get_auth(client, REGISTRATION_PAYLOAD)

    second_payload = {
        'email': 'career-reco-2@example.com',
        'password': 'StrongPass1',
        'name': 'Second User',
        'course': 'Computer Science',
        'year_level': 'Junior',
    }
    _, user_two_id = register_and_get_auth(client, second_payload)

    forbidden = client.get(
        f'/api/users/{user_two_id}/recommendations/career-aligned',
        headers=headers_one,
    )
    assert forbidden.status_code == 403

    # Control check to make sure own endpoint is accessible.
    allowed = client.get(
        f'/api/users/{user_one_id}/recommendations/career-aligned',
        headers=headers_one,
    )
    assert allowed.status_code == 200


def test_career_aligned_recommendations_include_resources_and_simulation_gap_closure(client: TestClient) -> None:
    headers, user_id = register_and_get_auth(client, REGISTRATION_PAYLOAD)
    select_software_developer_career(client, headers)

    submitted = client.post(f'/api/habits/{user_id}/assessment', json=ASSESSMENT_PAYLOAD, headers=headers)
    assert submitted.status_code == 201

    baseline = client.get(f'/api/users/{user_id}/recommendations/career-aligned', headers=headers)
    assert baseline.status_code == 200
    baseline_payload = baseline.json()

    assert baseline_payload['career'] is not None
    assert baseline_payload['career']['name'] == 'Software Developer'
    assert 1 <= len(baseline_payload['items']) <= 3

    first_item = baseline_payload['items'][0]
    assert first_item['subject_name']
    assert len(first_item['resources']) >= 1
    assert first_item['career_relevance_context'].endswith('for Software Developer')

    simulated = client.get(
        (
            f'/api/users/{user_id}/recommendations/career-aligned'
            '?study_hours=8&focus_score=92&phone_usage_hours=1&social_media_hours=1'
        ),
        headers=headers,
    )
    assert simulated.status_code == 200

    simulated_items = simulated.json()['items']
    assert simulated_items
    assert any(item['gap_closure_percent'] >= 0 for item in simulated_items)
