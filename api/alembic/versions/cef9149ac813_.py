"""empty message

Revision ID: cef9149ac813
Revises: 535c8cc3c6a8
Create Date: 2023-09-10 20:47:32.741799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cef9149ac813'
down_revision: Union[str, None] = '535c8cc3c6a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'dirfiles', ['id'])
    op.create_unique_constraint(None, 'projects', ['id'])
    op.create_unique_constraint(None, 'syncdirs', ['id'])
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'syncdirs', type_='unique')
    op.drop_constraint(None, 'projects', type_='unique')
    op.drop_constraint(None, 'dirfiles', type_='unique')
    # ### end Alembic commands ###