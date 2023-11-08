# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_get_by_id():
#     response = client.get("/book/id?book_id=1")

#     assert response.status_code == 200
#     assert response.json() == {
#         "id": 1,
#         "title": "Rich Dad",
#         "pages": 250,
#         "created_at": "2023-11-01",
#         "author_id": 1,
#         "author_name": "Robert",
#     }

# def test_get_by_invalid_book_id():
#     response = client.get("/book/id?book_id=2")

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Book id 2 not found"}

