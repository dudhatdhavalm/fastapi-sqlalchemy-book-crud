## content of test_db.py
#import pytest
#from sqlalchemy.orm import sessionmaker
#
#from app.api.dependencies import *
#
#
#import pytest
#from sqlalchemy import create_engine
#from sqlalchemy.exc import OperationalError
#
## Create a testing session local using the provided database URI
#TEST_DATABASE_URL = "postgresql://refactorybot:22r)pGKLcaeP@refactory.cluster-cw4q9y97boua.us-east-1.rds.amazonaws.com:5432/code_robotics_1703882508620"
#TestSessionLocal = sessionmaker(
#    autocommit=False, autoflush=False, bind=create_engine(TEST_DATABASE_URL)
#)
#
#
#@pytest.fixture(scope="function")
#def override_get_db():
#    """Override get_db dependency to use test database session"""
#
#    def _get_db_override():
#        try:
#            db = TestSessionLocal()
#            yield db
#        finally:
#            db.close()
#
#    return _get_db_override
#
#
#def test_get_db_no_errors(override_get_db):
#    db_gen = override_get_db()
#    db = next(db_gen)
#    try:
#        assert db is not None, "The get_db generator should not yield None"
#    finally:
#        # Clean up by closing the session and exhausting the generator
#        next(db_gen, None)
#
#
#def test_get_db_session_closed(override_get_db):
#    db_gen = override_get_db()
#    db = next(db_gen)
#    next(db_gen, None)  # Should close the generator and thus the session
#    with pytest.raises(OperationalError, match=r".*closed.*"):
#        db.execute("SELECT 1")  # This will fail because session is closed
#