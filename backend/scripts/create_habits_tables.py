"""Create habits assessment related tables."""

from pathlib import Path
import sqlite3

ROOT_DIR = Path(__file__).resolve().parents[1]
SQL_FILE = Path(__file__).resolve().with_name('create_habits_tables.sql')
DB_FILE = ROOT_DIR.parent / 'auth.db'


def main() -> None:
    sql = SQL_FILE.read_text(encoding='utf-8')
    with sqlite3.connect(DB_FILE) as connection:
        connection.executescript(sql)
    print('habits tables created')


if __name__ == '__main__':
    main()
