import sys
from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database import Base, get_db
from app.main import app
from app.rate_limiter import login_rate_limiter
from app.career_services import seed_career_metadata


@pytest.fixture(autouse=True)
def clear_rate_limiter() -> Generator[None, None, None]:
    login_rate_limiter._store.clear()  # noqa: SLF001
    yield
    login_rate_limiter._store.clear()  # noqa: SLF001


@pytest.fixture
def db_session(tmp_path: Path) -> Generator[Session, None, None]:
    db_file = tmp_path / 'test_auth.db'
    engine = create_engine(
        f'sqlite:///{db_file}',
        connect_args={'check_same_thread': False},
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = testing_session_local()
    seed_career_metadata(session)
    try:
        yield session
    finally:
        session.close()
        engine.dispose()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
