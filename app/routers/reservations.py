from fastapi import APIRouter, Depends, status
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
    reservation_in: ReservationCreate, session: Session = Depends(get_session)
):
    return create_reservation_db(reservation_in, session)


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: int, session: Session = Depends(get_session)):
    delete_reservation_db(reservation_id, session)
