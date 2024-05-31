from logging.config import fileConfig
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context

import os

from app.database import Base

# Import all models to ensure they are registered with Base

# Load .env file
load_dotenv()

# Get the database configuration from environment variables
DB_HOST = os.getenv('DB_HOST').strip()
DB_USER = os.getenv('DB_USER').strip()
DB_PASSWORD = os.getenv('DB_PASSWORD').strip()
DB_NAME = os.getenv('DB_NAME').strip()
DB_PORT = os.getenv('DB_PORT').strip()

# Construct the database URL
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# This is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Set the sqlalchemy.url option dynamically
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,  # Use the DATABASE_URL directly
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
