"""Seed development users for manual testing."""

import sys
from pathlib import Path

from sqlalchemy import select

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.database import SessionLocal
from app.models import User
from app.security import hash_password

TEST_USERS = [
    {
        'email': 'student1@example.com',
        'password': 'StrongPass1',
        'name': 'Alex Johnson',
        'course': 'Computer Science',
        'year_level': 'Junior',
        'career_goal': 'Software Engineer',
    },
    {
        'email': 'student2@example.com',
        'password': 'StrongPass2',
        'name': 'Sam Rivera',
        'course': 'Information Systems',
        'year_level': 'Sophomore',
        'career_goal': 'Data Analyst',
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        created = 0
        for payload in TEST_USERS:
            existing = db.scalar(select(User).where(User.email == payload['email']))
            if existing is not None:
                continue

            user = User(
                email=payload['email'],
                hashed_password=hash_password(payload['password']),
                name=payload['name'],
                course=payload['course'],
                year_level=payload['year_level'],
                career_goal=payload['career_goal'],
            )
            db.add(user)
            created += 1

        db.commit()
        print(f'created {created} test users')
    finally:
        db.close()


if __name__ == '__main__':
    main()
