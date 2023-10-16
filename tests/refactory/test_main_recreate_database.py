
from main import *
import pytest
from app.models.book import Base
from sqlalchemy import engine


@pytest.fixture(scope="module")
def setup_test_db() -> None:
    """
    Set up the test database for pytest.
    """
    # Ensure the engine is available from the DB
    assert isinstance(engine, engine.Engine)

    # Create a new database for testing
    Base.metadata.create_all(engine)


def test_recreate_database(setup_test_db: pytest.fixture) -> None:
    """
    Test the recreate_database function to ensure it does not raise any exceptions.
    """
    try:
        recreate_database()
        assert True
    except Exception as e:
        pytest.fail(f"recreate_database raised exception: {e}")
