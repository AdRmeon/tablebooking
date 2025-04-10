from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session
from app.models.reservation import ReservationCreate, ReservationRead
from app.core.database import get_session
from app.services.reservation_service import get_reservations_db
from app.services.reservation_service import create_reservation_db
from app.services.reservation_service import delete_reservation_db

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=list[ReservationRead])
def get_reservations(session: Session = Depends(get_session)):
    return get_reservations_db(session)


@router.post("/", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    reservation_in: Annotated[
        ReservationCreate,
        Body(
            examples=[
                {
                    "customer_name": "John Doe",
                    "reservation_time": "2025-04-09 12:00:00.000",
                    "duration_minutes": 60,
                    "table_id": 1,
                }
            ],
        ),
    ],
    session: Session = Depends(get_session),
):
    return create_reservation_db(reservation_in, session)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    delete_reservation_db(reservation_id, session)
