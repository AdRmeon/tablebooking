from fastapi.testclient import TestClient
from sqlmodel import Session
from app.core.exceptions import model_not_found_404
from app.models.table import Table


def test_create_table(client: TestClient):
    table_data = {"name": "Table 1", "seats": 4, "location": "Зал у окна"}
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == table_data["name"]
    assert data["seats"] == table_data["seats"]
    assert data["location"] == table_data["location"]
    assert "id" in data


def test_get_tables(client: TestClient, session: Session):
    table1 = Table(name="Table 1", seats=4, location="Зал у окна")
    table2 = Table(name="Table 2", seats=3, location="Зал на терассе")
    session.add_all([table1, table2])
    session.commit()

    response = client.get("/tables/")
    assert response.status_code == 200
    data = response.json()
    assert data[0]["name"] == table1.name
    assert data[0]["seats"] == table1.seats
    assert data[0]["location"] == table1.location


def test_delete_table(client: TestClient, session: Session):
    table1 = Table(name="Table 1", seats=4, location="Зал у окна")
    session.add(table1)
    session.commit()

    response = client.delete(f"/tables/{table1.id}")
    assert response.status_code == 204


def test_delete_table_not_found(client: TestClient, session: Session, clean_db):
    table_id = 1
    response = client.delete(f"/tables/{table_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": model_not_found_404(Table, table_id).detail}
