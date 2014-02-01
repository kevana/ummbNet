"""Added separate calltime to Event

Revision ID: 22824bf1f98c
Revises: 3d37a3790b89
Create Date: 2014-01-31 19:37:34.963340

"""

# revision identifiers, used by Alembic.
revision = '22824bf1f98c'
down_revision = '3d37a3790b89'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('calltime', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('event', 'calltime')
