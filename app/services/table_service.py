from fastapi import HTTPException
from httpx import get
from sqlmodel import select
from app.core.exceptions import model_not_found_404
from app.models.table import Table
from app.core.logger import logger


def create_table_db(table_in, session):
    table = Table.model_validate(table_in)
    session.add(table)
    session.commit()
    session.refresh(table)
    logger.info(f"Table {table.name} created")
    return table


def get_tables_db(session):
    return session.exec(select(Table)).all()


def delete_table_db(table_id, session):
    table = get_table_db(table_id, session)
    session.delete(table)
    session.commit()


def get_table_db(table_id, session):
    table = session.get(Table, table_id)
    if not table:
        raise model_not_found_404(Table, table_id)
    return table
