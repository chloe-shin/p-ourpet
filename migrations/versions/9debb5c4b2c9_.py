"""empty message

Revision ID: 9debb5c4b2c9
Revises: e835285fd840
Create Date: 2019-12-12 00:38:38.065772

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9debb5c4b2c9'
down_revision = 'e835285fd840'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('sitter_id', sa.Integer(), nullable=False),
    sa.Column('start', sa.DateTime(), nullable=True),
    sa.Column('finish', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('total_price', sa.Integer(), nullable=True),
    sa.Column('pet_type', sa.String(), nullable=True),
    sa.Column('pet_size', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['sitter_id'], ['sitters.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('booking')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('booking',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sitter_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('is_confirmed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('pet_type', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('pet_size', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('finish', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('start', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('total_price', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['sitter_id'], ['sitters.id'], name='booking_sitter_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='booking_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='booking_pkey')
    )
    op.drop_table('bookings')
    # ### end Alembic commands ###
