"""add text column

Revision ID: 3233b8b94521
Revises: None
Create Date: 2013-04-11 15:24:15.921509

"""

# revision identifiers, used by Alembic.
revision = '3233b8b94521'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('questions', sa.Column('text', sa.String(256)))


def downgrade():
    op.drop_column('questions', 'text')
