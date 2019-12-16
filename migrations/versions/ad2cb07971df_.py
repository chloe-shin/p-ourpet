"""empty message

Revision ID: ad2cb07971df
Revises: f0e418b2b58e
Create Date: 2019-12-16 11:36:17.423692

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'ad2cb07971df'
down_revision = 'f0e418b2b58e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('is_paid', sa.Boolean(), nullable=True))
    op.add_column('bookings', sa.Column('stripe_token', sa.String(), nullable=True))
    op.drop_constraint('bookings_token_key', 'bookings', type_='unique')
    op.create_unique_constraint(None, 'bookings', ['stripe_token'])
    op.drop_column('bookings', 'token')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('token', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'bookings', type_='unique')
    op.create_unique_constraint('bookings_token_key', 'bookings', ['token'])
    op.drop_column('bookings', 'stripe_token')
    op.drop_column('bookings', 'is_paid')
    # ### end Alembic commands ###