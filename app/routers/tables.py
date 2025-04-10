from typing import Annotated
from fastapi import APIRouter, Body, Depends, status
from sqlmodel import Session
from app.models.table import TableCreate, TableRead
from app.core.database import get_session
from app.services.table_service import create_table_db
from app.services.table_service import get_tables_db
from app.services.table_service import delete_table_db

router = APIRouter(prefix="/tables", tags=["Tables"])


@router.get("/", response_model=list[TableRead])
def get_tables(session: Session = Depends(get_session)):
    return get_tables_db(session)


@router.post("/", response_model=TableRead, status_code=status.HTTP_201_CREATED)
def create_table(
    table_in: Annotated[
        TableCreate,
        Body(
            examples=[
                {
                    "name": "Table 1",
                    "seats": 4,
                    "location": "Зал у окна",
                }
            ],
        ),
    ],
    session: Session = Depends(get_session),
):
    table = create_table_db(table_in, session)
    return table


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(table_id: int, session: Session = Depends(get_session)):
    delete_table_db(table_id, session)
