"""Added event.opponent and request.info

Revision ID: 4675799c91d0
Revises: 22824bf1f98c
Create Date: 2014-02-06 00:20:07.880068

"""

# revision identifiers, used by Alembic.
revision = '4675799c91d0'
down_revision = '22824bf1f98c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('event', sa.Column('opponent', sa.Text(), nullable=True))
    op.add_column('request', sa.Column('info', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('request', 'info')
    op.drop_column('event', 'opponent')
