from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_career_schema(engine: Engine) -> None:
    inspector = inspect(engine)
    if not inspector.has_table('users'):
        return

    user_columns = {column['name'] for column in inspector.get_columns('users')}
    with engine.begin() as connection:
        if 'career_id' not in user_columns:
            connection.execute(text('ALTER TABLE users ADD COLUMN career_id INTEGER'))

        connection.execute(
            text(
                'CREATE INDEX IF NOT EXISTS ix_users_career_id ON users (career_id)'
            )
        )

        if 'career_goal' in user_columns:
            connection.execute(text('ALTER TABLE users DROP COLUMN career_goal'))
