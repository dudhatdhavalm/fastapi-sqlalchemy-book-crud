# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_create_book():
#     response = client.post(
#         "/book", json={"title": "Rich Dad", "pages": 250, "author_id": 1}
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#         "title": "Rich Dad",
#         "pages": 250,
#         "created_at": "2023-11-01",
#         "id": 1,
#     }

#     client.delete(f"/book/{response.json().id}")


# def test_create_book_invalid_author_id():
#     response = client.post(
#         "/book", json={"title": "Rich Dad Poor Dad", "pages": 250, "author_id": 2}
#     )

#     assert response.status_code == 404
#     assert response.json() == {"detail": "Author id 2 not found"}
