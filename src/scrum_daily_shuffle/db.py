from typing import Generator

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from scrum_daily_shuffle.config import CONFIG

ENGINE = create_engine(f"sqlite:///{CONFIG.sqlite3_filepath}")
"""
Engine for sqlite.
"""

SESSION_MAKER = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
"""
Default session maker, used in ``get_db_session`` function.
"""


def get_db_session() -> Generator:
    """
    Dependency for getting database sessions for FastAPI.

    Returns:
        Database session.
    """
    db = SESSION_MAKER()
    try:
        yield db
    finally:
        db.close()
