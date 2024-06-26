"""empty message

Revision ID: 90145b91fc5e
Revises: fd1ecdf985cb
Create Date: 2024-05-16 01:28:48.177931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90145b91fc5e'
down_revision = 'fd1ecdf985cb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cumulative_points', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('member', schema=None) as batch_op:
        batch_op.drop_column('cumulative_points')

    # ### end Alembic commands ###
