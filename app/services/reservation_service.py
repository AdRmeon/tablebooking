from sqlmodel import Session, select, text
from datetime import timedelta
from app.models.reservation import Reservation, ReservationCreate
from app.core.exceptions import model_not_found_404, reservation_conflict_400
from app.core.logger import logger
from app.services.table_service import get_table_db


def check_reservation_conflict(
    reservation_in: ReservationCreate, session: Session
) -> bool:
    new_start = reservation_in.reservation_time
    new_end = new_start + timedelta(minutes=reservation_in.duration_minutes)

    query = text(
        """
        SELECT * FROM reservation
        WHERE table_id = :table_id
          AND reservation_time < :new_end
          AND (reservation_time + (duration_minutes * interval '1 minute')) > :new_start
        LIMIT 1
    """
    )

    result = session.exec(
        query,
        params={
            "table_id": reservation_in.table_id,
            "new_start": new_start,
            "new_end": new_end,
        },
    ).first()
    return result is not None


def get_reservations_db(session):
    return session.exec(select(Reservation)).all()


def create_reservation_db(reservation_in, session):
    reservation = Reservation.model_validate(reservation_in)

    get_table_db(reservation.table_id, session)
    if check_reservation_conflict(reservation_in, session):
        raise reservation_conflict_400(reservation_in)

    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


def delete_reservation_db(reservation_id, session):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise model_not_found_404(Reservation, reservation_id)
    session.delete(reservation)
    session.commit()
