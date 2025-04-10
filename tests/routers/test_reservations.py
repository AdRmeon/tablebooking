from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.exceptions import TABLE_ALREADY_BOOKED_400
from app.models import reservation
from app.models.reservation import Reservation, ReservationCreate
from app.models.table import TableCreate
from app.services.table_service import create_table_db


def test_create_reservation(client: TestClient, session: Session) -> None:
    table = TableCreate(name="Table 1", seats=4, location="Зал у окна")
    created_table = create_table_db(table, session)
    now = datetime.now()
    reservation_in = Reservation(
        customer_name="John Doe",
        table_id=created_table.id,
        reservation_time=now,
        duration_minutes=60,
    )
    json_compatible_reservation = jsonable_encoder(reservation_in)

    response = client.post("/reservations/", json=json_compatible_reservation)

    assert response.status_code == 201
    assert response.json()["table_id"] == created_table.id
    assert response.json()["customer_name"] == reservation_in.customer_name


def test_create_reservation_wrong_table(
    client: TestClient, session: Session, clean_db
) -> None:
    reservation_in = ReservationCreate(
        customer_name="John Doe",
        table_id=2,
        reservation_time=datetime.now(),
        duration_minutes=60,
    )
    json_compatible_reservation = jsonable_encoder(reservation_in)

    response = client.post("/reservations/", json=json_compatible_reservation)
    assert response.status_code == 404
    assert response.json() == {"detail": "Table not found"}


def test_reservation_conflict(client: TestClient, session: Session) -> None:
    table = TableCreate(name="Table 1", seats=4, location="Зал у окна")
    created_table = create_table_db(table, session)
    now = datetime.now()
    reservation_in = ReservationCreate(
        customer_name="John Doe",
        table_id=created_table.id,
        reservation_time=now,
        duration_minutes=60,
    )
    json_compatible_reservation = jsonable_encoder(reservation_in)

    response = client.post("/reservations/", json=json_compatible_reservation)
    assert response.status_code == 201

    reservation_before_reservation = ReservationCreate(
        customer_name="Jane Doe",
        table_id=created_table.id,
        reservation_time=now - timedelta(minutes=30),
        duration_minutes=60,
    )
    json_compatible_before_reservation = jsonable_encoder(
        reservation_before_reservation
    )

    response = client.post("/reservations/", json=json_compatible_before_reservation)
    assert response.status_code == TABLE_ALREADY_BOOKED_400.status_code
    assert response.json()["detail"] == TABLE_ALREADY_BOOKED_400.detail

    reservation_after_reservation = ReservationCreate(
        customer_name="Jane Doe",
        table_id=created_table.id,
        reservation_time=now + timedelta(minutes=30),
        duration_minutes=60,
    )
    json_compatible_after_reservation = jsonable_encoder(reservation_after_reservation)

    response = client.post("/reservations/", json=json_compatible_after_reservation)
    assert response.status_code == TABLE_ALREADY_BOOKED_400.status_code
    assert response.json()["detail"] == TABLE_ALREADY_BOOKED_400.detail


def test_get_reservations(client: TestClient, session: Session, clean_db):
    table = TableCreate(name="Table 1", seats=4, location="Зал у окна")
    created_table = create_table_db(table, session)

    now = datetime.now()
    reservation1 = Reservation(
        customer_name="John Doe",
        table_id=created_table.id,
        reservation_time=now,
        duration_minutes=60,
    )
    reservation2 = Reservation(
        customer_name="Jane Doe",
        table_id=created_table.id,
        reservation_time=now + timedelta(minutes=120),
        duration_minutes=60,
    )
    session.add_all([reservation1, reservation2])
    session.commit()

    response = client.get("/reservations/")
    assert response.status_code == 200

    reservations = response.json()
    assert len(reservations) == 2
    assert reservations[0]["customer_name"] == reservation1.customer_name
    assert reservations[1]["customer_name"] == reservation2.customer_name
    assert reservations[0]["table_id"] == created_table.id
    assert reservations[1]["table_id"] == created_table.id


def test_delete_reservation(client: TestClient, session: Session, clean_db):
    table = TableCreate(name="Table 1", seats=4, location="Зал у окна")
    created_table = create_table_db(table, session)

    now = datetime.now()
    reservation = Reservation(
        customer_name="John Doe",
        table_id=created_table.id,
        reservation_time=now,
        duration_minutes=60,
    )
    session.add(reservation)
    session.commit()

    response = client.delete(f"/reservations/{reservation.id}")
    assert response.status_code == 204

    response = client.get("/reservations/")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_delete_reservation_not_found(client: TestClient, session: Session, clean_db):
    response = client.delete("/reservations/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Reservation not found"}
