from app import app


def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_students():
    client = app.test_client()
    response = client.get("/students")
    assert response.status_code == 200
    assert len(response.get_json()) == 3


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200