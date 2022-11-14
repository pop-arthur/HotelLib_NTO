"""Initial

Revision ID: 1e7d81f16735
Revises: cb2e16dd4ca6
Create Date: 2022-11-14 21:46:40.096887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e7d81f16735'
down_revision = 'cb2e16dd4ca6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('hotels', sa.Column('name', sa.String(length=200), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('hotels', 'name')
    # ### end Alembic commands ###
