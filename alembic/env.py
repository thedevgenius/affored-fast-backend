# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
# Import the Base and DATABASE_URL from your app’s database configuration
from app.core.database import Base, DATABASE_URL, engine
from app.users.models import User
from app.location.models import Address
from app.business.models import Business


config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# This sets up logging configurations if necessary
if config.config_file_name is not None:
 fileConfig(config.config_file_name)

# Target metadata for Alembic migrations
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()