from fastapi import HTTPException
from sqlmodel import select
from app.models.table import Table


def create_table_db(table_in, session):
    table = Table.model_validate(table_in)
    session.add(table)
    session.commit()
    session.refresh(table)
    return table


def get_tables_db(session):
    return session.exec(select(Table)).all()


def delete_table_db(table_id, session):
    table = session.get(Table, table_id)
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")
    session.delete(table)
    session.commit()
