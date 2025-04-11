from fastapi import HTTPException
from sqlmodel import SQLModel
from app.core.logger import logger
from app.models.reservation import ReservationCreate


def reservation_conflict_400(reservation_in: ReservationCreate):
    logger.warning(
        f"Reservation conflict: table_id: {reservation_in.table_id} - {reservation_in.reservation_time}"
    )
    return HTTPException(
        status_code=400,
        detail=f"This time slot {reservation_in.reservation_time} is already booked for table_id:{reservation_in.table_id}",
    )


def model_not_found_404(model: SQLModel, id: int):
    logger.error(f"{model.__name__} with id:{id} not found")
    return HTTPException(
        status_code=404, detail=f"{model.__name__} with id:{id} not found"
    )
