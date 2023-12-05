from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def create_author():
    response = client.post("/author", json={"name": "Robert"})
    return response.json()


def get_author_by_id(author_id: int):
    response = client.get(f"/author/{author_id}")
    return response.json()


# test_create_author


def test_create_author():
    response = client.post("/author", json={"name": "Xyz"})
    assert response.status_code == 200
    assert response.json()["name"] == "Xyz"


# test_get_author


def test_get_author():
    response = client.get(
        "/author",
    )
    assert response.status_code == 200
    assert len(response.json()) > 0


# test_get_by_author_id


def test_get_by_id_author():
    res = create_author()

    response = client.get(f"/author/{res['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "Robert"


def test_get_by_invalid_author_id():
    response = client.get("/author/300")

    assert response.status_code == 404
    assert response.json() == {"detail": "Author id 300 not found"}


# test_update_author


def test_update_author():
    res = create_author()

    response = client.put(f"/author/{res['id']}", json={"name": "new name"})

    assert response.status_code == 200
    assert response.json()["name"] == "new name"


def test_update_author_invalid_author_id():
    response = client.put("/author/309", json={"name": "new name"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Author id 309 not found"}


# test_delete_author


def test_delete_author():
    author = create_author()
    print(author)
    response = client.delete(f"/author/{author['id']}")
    assert response.status_code == 200
    assert response.json() == {"detail": f"Author id {author['id']} deleted successfully"}
