"""Added Reservation index

Revision ID: 0650dc2e10bc
Revises: 0d2463a7ef77
Create Date: 2025-04-08 21:50:25.427690

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '0650dc2e10bc'
down_revision: Union[str, None] = '0d2463a7ef77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_reservation_reservation_time'), 'reservation', ['reservation_time'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_reservation_reservation_time'), table_name='reservation')
    # ### end Alembic commands ###
