"""Add Comment model

Revision ID: eb63cbbfb2ab
Revises: 
Create Date: 2024-08-31 18:43:22.901765

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'eb63cbbfb2ab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
                               type_=sa.String(length=256),
                               existing_type=sa.String(length=128))

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
                               type_=sa.String(length=128),
                               existing_type=sa.String(length=256))

    # ### end Alembic commands ###
