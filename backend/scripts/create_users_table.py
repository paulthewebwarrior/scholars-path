"""Create the users table for new environments."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.database import Base, engine
from app.models import User  # noqa: F401


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print('users table created')


if __name__ == '__main__':
    main()
