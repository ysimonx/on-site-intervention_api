"""active user

Revision ID: 3097a7d38374
Revises: 9a5454753480
Create Date: 2024-01-04 19:56:54.995532

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3097a7d38374'
down_revision = '9a5454753480'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('active', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('active')

    # ### end Alembic commands ###
