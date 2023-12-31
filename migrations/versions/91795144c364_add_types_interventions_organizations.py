"""add types_interventions_organizations

Revision ID: 91795144c364
Revises: 027dd9567134
Create Date: 2023-12-29 08:44:08.080299

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91795144c364'
down_revision = '027dd9567134'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('types_interventions_organizations',
    sa.Column('type_intervention_id', sa.String(length=36), nullable=False),
    sa.Column('organization_id', sa.String(length=36), nullable=False),
    sa.Column('config_text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ),
    sa.ForeignKeyConstraint(['type_intervention_id'], ['types_interventions.id'], ),
    sa.PrimaryKeyConstraint('type_intervention_id', 'organization_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('types_interventions_organizations')
    # ### end Alembic commands ###
