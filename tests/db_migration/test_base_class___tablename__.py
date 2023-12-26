## Imports necessary for the test script
#import pytest
#from sqlalchemy.orm import declarative_base
#from app.db.base_class import Base
#
## Using the Base class that was already defined in the scope
#from app.db.base_class import *
#
#
#def test_base_class_has_tablename_attr():
#    """
#    Test that the Base class has a __tablename__ attribute generated.
#    """
#    assert hasattr(
#        Base, "__tablename__"
#    ), "The Base class should have a '__tablename__' attribute."
#
#
#def test_auto_tablename_generation_for_subclass():
#    """
#    Test that a subclass of Base automatically generates the __tablename__ attribute.
#    """
#
#    class MockSubclass(Base):
#        pass
#
#    assert hasattr(
#        MockSubclass, "__tablename__"
#    ), "The MockSubclass should have a '__tablename__' attribute."
#    assert (
#        MockSubclass.__tablename__ == "mocksubclass".lower()
#    ), f"The __tablename__ should be '{'mocksubclass'.lower()}', got: {MockSubclass.__tablename__}"
#