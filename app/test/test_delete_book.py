# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)


# def test_delete_book():
#     response = client.post(
#         "/book", json={"title": "Rich Dad", "pages": 250, "author_id": 1}
#     )

#     assert response.status_code == 200
#     assert response.json() == {
#         "title": "Rich Dad",
#         "pages": 250,
#         "created_at": "2023-11-01",
#     }

#     # assert response.json().title == "Rich Dad"

#     response = client.delete(f"book/{response.json().id}")

#     assert response.status_code == 200
#     assert response.json == {"detail": "Book id 1 deleted successfully"}
