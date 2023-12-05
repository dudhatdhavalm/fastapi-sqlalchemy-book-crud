import datetime
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sample books API is online"}


def create_author():
    response = client.post("/author", json={"name": "Robert"})
    return response.json()


def create_book(author_id: int):
    response = client.post(
        "/book", json={"title": "Rich Dad", "pages": 250, "author_id": author_id}
    )
    return response.json()


def delete_author(id):
    response = client.delete(f"/author/{id}")
    return response.json()


def delete_book(id):
    response = client.delete(f"/book/{id}")
    return response.json()


# test_create_book


def test_create_book():
    author = create_author()
    response = client.post(
        "/book", json={"title": "Rich Dad", "pages": 250, "author_id": author["id"]}
    )
    assert response.status_code == 200
    created_at = datetime.date.today().isoformat()

    assert response.json()["title"] == "Rich Dad"
    assert response.json()["pages"] == 250
    assert response.json()["created_at"] == created_at

    delete_book(response.json()["id"])


def test_create_book_invalid_author_id():
    response = client.post(
        "/book", json={"title": "Rich Dad Poor Dad", "pages": 250, "author_id": 200}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Author id 200 not found"}


# test_get_book


def test_get_book():
    response = client.get(
        "/book",
    )
    assert response.status_code == 200
    assert len(response.json()) >= 0


def test_get_by_id():
    author = create_author()
    book = create_book(author["id"])

    response = client.get(f"/book/{book['id']}")

    assert response.status_code == 200
    created_at = datetime.date.today().isoformat()

    assert response.json()["title"] == "Rich Dad"
    assert response.json()["pages"] == 250
    assert response.json()["created_at"] == created_at


def test_get_by_invalid_book_id():
    response = client.get("/book/200")

    assert response.status_code == 404
    assert response.json() == {"detail": "Book id 200 not found"}


def test_delete_book():
    author = create_author()
    book = create_book(author["id"])
    response = delete_book(book["id"])
    print(response)
    assert response == {"detail": f"Book id {book['id']} deleted successfully"}
