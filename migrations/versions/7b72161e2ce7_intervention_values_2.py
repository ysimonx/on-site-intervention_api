"""intervention_values 2

Revision ID: 7b72161e2ce7
Revises: 7ec41b800d73
Create Date: 2024-01-02 14:43:42.052936

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b72161e2ce7'
down_revision = '7ec41b800d73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interventions_values', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organization_id', sa.String(length=36), nullable=True))
        batch_op.add_column(sa.Column('type_intervention_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'organizations', ['organization_id'], ['id'])
        batch_op.create_foreign_key(None, 'types_interventions', ['type_intervention_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interventions_values', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('type_intervention_id')
        batch_op.drop_column('organization_id')

    # ### end Alembic commands ###
