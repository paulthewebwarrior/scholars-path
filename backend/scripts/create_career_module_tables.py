"""Create career-goal module tables and users.career_id column for SQLite environments."""

from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parents[1]
SQL_FILE = Path(__file__).resolve().with_name('create_career_module_tables.sql')
DB_FILE = ROOT_DIR.parent / 'auth.db'


def _ensure_users_career_column(connection: sqlite3.Connection) -> None:
    rows = connection.execute('PRAGMA table_info(users)').fetchall()
    user_columns = {row[1] for row in rows}
    if 'career_id' not in user_columns:
        connection.execute('ALTER TABLE users ADD COLUMN career_id INTEGER')
    connection.execute('CREATE INDEX IF NOT EXISTS ix_users_career_id ON users (career_id)')


def main() -> None:
    sql = SQL_FILE.read_text(encoding='utf-8')
    with sqlite3.connect(DB_FILE) as connection:
        connection.executescript(sql)
        _ensure_users_career_column(connection)
    print('career module tables created')


if __name__ == '__main__':
    main()
