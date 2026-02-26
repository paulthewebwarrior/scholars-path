"""Run habits correlation recomputation batch job."""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.database import SessionLocal
from app.habits_engine import run_correlation_batch


def main() -> None:
    session = SessionLocal()
    try:
        rows = run_correlation_batch(session, cadence='weekly')
        print(f'correlation rows updated: {rows}')
    finally:
        session.close()


if __name__ == '__main__':
    main()
