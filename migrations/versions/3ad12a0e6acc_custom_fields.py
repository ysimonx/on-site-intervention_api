"""custom fields

Revision ID: 3ad12a0e6acc
Revises: 1b7a5b620611
Create Date: 2024-03-20 17:51:42.994783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ad12a0e6acc'
down_revision = '1b7a5b620611'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('types_interventions_sites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('dict_of_custom_fields', sa.Text(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('types_interventions_sites', schema=None) as batch_op:
        batch_op.drop_column('dict_of_custom_fields')

    # ### end Alembic commands ###
