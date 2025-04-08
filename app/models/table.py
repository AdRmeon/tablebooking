from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class TableBase(SQLModel):
    name: str
    seats: int
    location: str


class Table(TableBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    reservations: List["Reservation"] = Relationship(back_populates="table")  # type: ignore # noqa: F821


class TableCreate(TableBase):
    pass


class TableRead(TableBase):
    id: int


class TableUpdate(SQLModel):
    name: Optional[str] = None
    seats: Optional[int] = None
    location: Optional[str] = None
