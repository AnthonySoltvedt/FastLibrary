from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}


def test_add_book():
    response = client.post("/books", json={
        "title": "Book A",
        "author": "Author A",
        "isbn": "12345",
        "available": True
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Book A"
    assert data["author"] == "Author A"
    assert data["isbn"] == "12345"
    assert data["available"] is True


def test_get_books():
    client.post("/books", json={
        "title": "Book B",
        "author": "Author B",
        "isbn": "67890",
        "available": False
    })
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_book_by_id():
    response = client.post("/books", json={
        "title": "Book A",
        "author": "Author A",
        "isbn": "12345",
        "available": True
    })
    book = response.json()
    book_id = book["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Book A"


def test_update_book():
    response = client.post("/books", json={
        "title": "Book A",
        "author": "Author A",
        "isbn": "12345",
        "available": True
    })
    book = response.json()
    book_id = book["id"]

    response = client.put(f"/books/{book_id}", json={
        "title": "Book Updated",
        "author": "Author B",
        "isbn": "67890",
        "available": False
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Book Updated"


def test_delete_book():
    response = client.post("/books", json={
        "title": "Book A",
        "author": "Author A",
        "isbn": "12345",
        "available": True
    })
    book = response.json()
    book_id = book["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 204

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 404


def test_add_member():
    response = client.post("/members", json={
        "id": 0,  # will be overridden
        "name": "John Doe",
        "email": "john@example.com"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert "id" in data


def test_list_members():
    response = client.get("/members")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1
