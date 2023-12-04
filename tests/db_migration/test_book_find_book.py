#from app.api.endpoints.book import *
#import pytest
#
#
#def test_get_by_id(monkeypatch):
#    """
#    Tests the get_by_id function does not return any error and value is not none.
#    """
#
#    # Mocking necessary components needed for the function to run
#    def mock_get_db():
#        class MockSession:
#            def query(self, model):
#                class QueryResult:
#                    def filter(self, condition):
#                        class FilterResult:
#                            def first(self):
#                                class MockBook:
#                                    id = 1
#                                    title = "Test Book"
#                                    pages = 100
#
#                                return MockBook()
#
#                        return FilterResult()
#
#                return QueryResult()
#
#            def close(self):
#                pass
#
#        return MockSession()
#
#    monkeypatch.setattr("app.api.dependencies.get_db", mock_get_db)
#
#    # Checking function does not return any error and its return value is not None
#    result = get_by_id(book_id=1)
#    assert result is not None
#