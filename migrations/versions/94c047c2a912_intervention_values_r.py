"""intervention_values R

Revision ID: 94c047c2a912
Revises: 1e4e279e020a
Create Date: 2024-01-02 15:03:04.067924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c047c2a912'
down_revision = '1e4e279e020a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.add_column(sa.Column('organization_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'organizations', ['organization_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('places', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('organization_id')

    # ### end Alembic commands ###
