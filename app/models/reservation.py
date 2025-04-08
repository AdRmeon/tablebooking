from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime


class ReservationBase(SQLModel):
    customer_name: str
    reservation_time: datetime
    duration_minutes: int


class Reservation(ReservationBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    table_id: int = Field(foreign_key="table.id")

    table: Optional["Table"] = Relationship(back_populates="reservations")  # type: ignore # noqa: F821


class ReservationCreate(ReservationBase):
    pass


class ReservationRead(ReservationBase):
    id: int
    table_id: int


class ReservationUpdate(SQLModel):
    customer_name: Optional[str] = None
    reservation_time: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    table_id: Optional[int] = None
