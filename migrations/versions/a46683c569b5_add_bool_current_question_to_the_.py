"""add bool current question to the question table

Revision ID: a46683c569b5
Revises: 09c69492e00f
Create Date: 2017-03-23 12:12:31.975762

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a46683c569b5'
down_revision = '09c69492e00f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('questions', sa.Column('current', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('questions', 'current')
    # ### end Alembic commands ###
