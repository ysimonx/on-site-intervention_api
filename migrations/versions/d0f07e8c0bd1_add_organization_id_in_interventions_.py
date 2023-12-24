"""add organization_id in interventions table

Revision ID: d0f07e8c0bd1
Revises: 
Create Date: 2023-12-24 09:35:15.969899

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0f07e8c0bd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interventions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organization_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'organizations', ['organization_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interventions', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('organization_id')

    # ### end Alembic commands ###
