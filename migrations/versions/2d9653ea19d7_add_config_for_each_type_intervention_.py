"""add config for each type_intervention for each organization

Revision ID: 2d9653ea19d7
Revises: d8a4a60e8710
Create Date: 2023-12-29 08:29:37.862311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d9653ea19d7'
down_revision = 'd8a4a60e8710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('types_interventions_organizations_config',
    sa.Column('type_intervention_id', sa.String(length=36), nullable=False),
    sa.Column('organization_id', sa.String(length=36), nullable=False),
    sa.Column('config', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['type_intervention_id'], ['types_interventions.id'], ),
    sa.PrimaryKeyConstraint('type_intervention_id', 'organization_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('types_interventions_organizations_config')
    # ### end Alembic commands ###