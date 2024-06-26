"""empty message

Revision ID: a445a232ed6d
Revises: 1b96be2caf59
Create Date: 2024-03-24 17:52:25.137972

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a445a232ed6d'
down_revision = '1b96be2caf59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nickname', sa.String(length=200), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('admin', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=200), nullable=True))
        batch_op.drop_column('nickname')

    # ### end Alembic commands ###
