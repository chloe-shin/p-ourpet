"""empty message

Revision ID: 878aab1c7105
Revises: 1636e56777fa
Create Date: 2019-12-12 15:18:27.921247

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '878aab1c7105'
down_revision = '1636e56777fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('is_photo', sa.Boolean(), nullable=True))
    op.add_column('bookings', sa.Column('pet_age', sa.String(), nullable=True))
    op.add_column('bookings', sa.Column('pet_breed', sa.String(), nullable=True))
    op.add_column('bookings', sa.Column('pet_name', sa.String(), nullable=True))
    op.add_column('bookings', sa.Column('pet_sex', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'pet_sex')
    op.drop_column('bookings', 'pet_name')
    op.drop_column('bookings', 'pet_breed')
    op.drop_column('bookings', 'pet_age')
    op.drop_column('bookings', 'is_photo')
    # ### end Alembic commands ###
