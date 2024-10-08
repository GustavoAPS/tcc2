"""Add StressRecord model

Revision ID: 42cb75f81581
Revises: eb63cbbfb2ab
Create Date: 2024-09-09 12:27:48.877937

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '42cb75f81581'
down_revision = 'eb63cbbfb2ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stress_record',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('stress_level', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('categorias',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=sa.Text(),
               existing_nullable=True)

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
        batch_op.alter_column('preferencias',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('preferencias',
               existing_type=sa.Text(),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)

    with op.batch_alter_table('game', schema=None) as batch_op:
        batch_op.alter_column('categorias',
               existing_type=sa.Text(),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=True)

    op.drop_table('stress_record')
    # ### end Alembic commands ###
