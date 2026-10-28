from collections.abc import Generator
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app.db import get_session
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def test_session() -> Generator[Session, None, None]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = test_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    engine.dispose()


def test_create_list_edit_and_delete(client: TestClient) -> None:
    created = client.post(
        "/items",
        json={"name": "  Arroz  ", "quantity": "0.5", "unit": "kg", "unit_price": "12.50"},
    )
    assert created.status_code == 201
    item = created.json()
    assert item["name"] == "Arroz"
    assert item["total"] == "6.25"
    assert item["is_purchased"] is False

    duplicate = client.post("/items", json={"name": "Arroz"})
    assert duplicate.status_code == 201
    assert len(client.get("/items").json()) == 2

    updated = client.patch(
        f"/items/{item['id']}",
        json={"is_purchased": True, "unit_price": "13.00"},
    )
    assert updated.status_code == 200
    assert updated.json()["total"] == "6.50"
    assert updated.json()["is_purchased"] is True

    deleted = client.delete(f"/items/{item['id']}")
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert len(client.get("/items").json()) == 1
    assert client.delete(f"/items/{item['id']}").status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"name": "   "},
        {"name": "Leche", "quantity": "0"},
        {"name": "Leche", "unit_price": "-1"},
    ],
)
def test_create_rejects_invalid_values(client: TestClient, payload: dict) -> None:
    assert client.post("/items", json=payload).status_code == 422


def test_patch_rejects_null_required_field(client: TestClient) -> None:
    item_id = client.post("/items", json={"name": "Pan"}).json()["id"]
    assert client.patch(f"/items/{item_id}", json={"name": None}).status_code == 422
    assert client.patch(f"/items/{item_id}", json={"quantity": None}).status_code == 422
    assert client.patch(f"/items/{item_id}", json={"is_purchased": None}).status_code == 422
    assert client.get("/items").json()[0]["name"] == "Pan"


def test_missing_price_has_no_total(client: TestClient) -> None:
    item = client.post("/items", json={"name": "Pan"}).json()
    assert Decimal(item["quantity"]) == Decimal("1")
    assert item["unit_price"] is None
    assert item["total"] is None


def test_frontend_cors_preflight(client: TestClient) -> None:
    response = client.options(
        "/items",
        headers={
            "Origin": "http://127.0.0.1:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:5173"


