from app.models import User
from app.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password


def _dummy_user() -> User:
    return User(
        id=1,
        email='alice@example.com',
        hashed_password='unused',
        name='Alice',
        course='Computer Science',
        year_level='Senior',
        career_goal='Backend Engineer',
    )


def test_password_hashing_and_verification() -> None:
    password = 'StrongPass1'
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password('WrongPass1', hashed)


def test_token_generation_and_validation() -> None:
    user = _dummy_user()
    access = create_access_token(user)
    refresh = create_refresh_token(user)

    access_payload = decode_token(access, token_type='access')
    refresh_payload = decode_token(refresh, token_type='refresh')

    assert access_payload['sub'] == '1'
    assert access_payload['email'] == user.email
    assert refresh_payload['sub'] == '1'
