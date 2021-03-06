"""empty message

Revision ID: 305d07707254
Revises: 878aab1c7105
Create Date: 2019-12-15 15:40:28.890976

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '305d07707254'
down_revision = '878aab1c7105'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('address', sa.String(), nullable=True))
    op.add_column('bookings', sa.Column('token', sa.String(), nullable=True))
    op.create_unique_constraint(None, 'bookings', ['token'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'bookings', type_='unique')
    op.drop_column('bookings', 'token')
    op.drop_column('bookings', 'address')
    # ### end Alembic commands ###
