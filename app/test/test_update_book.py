# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_update_book():
#     response = client.put(
#         "/book/id?book_id=1",
#         json={"title": "Rich Dad Poor Dad", "pages": 200, "author_id": 1},
#     )

#     assert response.status_code == 200
#     assert response.json() == {
#         "id": 1,
#         "title": "Rich Dad Poor Dad",
#         "pages": 200,
#         "created_at": "2023-11-01",
#         "author_id": 1,
#     }


# def test_update_book_invalid_book_id():
#     response = client.put(
#         "/book/id?book_id=2",
#         json={"title": "Rich Dad Poor Dad", "pages": 250, "author_id": 1},
#     )

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Book id 2 not found"}


# def test_update_book_invalid_author_id():
#     response = client.put(
#         "/book/id?book_id=1",
#         json={"title": "Rich Dad Poor Dad", "pages": 250, "author_id": 2},
#     )

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Author id 2 not found"}
