"""Add level and xp to User model

Revision ID: a239a9a2e8d6
Revises: 42cb75f81581
Create Date: 2024-09-15 17:16:25.758732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a239a9a2e8d6'
down_revision = '42cb75f81581'
branch_labels = None
depends_on = None


def upgrade():
    # Add columns with a default value for existing rows
    op.add_column('user', sa.Column('level', sa.Integer(), server_default='1'))
    op.add_column('user', sa.Column('xp', sa.Integer(), server_default='0'))

    # Remove the server default after existing rows have been updated
    op.alter_column('user', 'level', server_default=None)
    op.alter_column('user', 'xp', server_default=None)

def downgrade():
    op.drop_column('user', 'level')
    op.drop_column('user', 'xp')
