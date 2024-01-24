"""intervention_values

Revision ID: 7ec41b800d73
Revises: a90cc60ad18d
Create Date: 2024-01-02 13:50:58.184054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ec41b800d73'
down_revision = 'a90cc60ad18d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('interventions_values',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('owner_user_id', sa.String(length=36), nullable=True),
    sa.Column('tenant_id', sa.String(length=36), nullable=True),
    sa.Column('intervention_id', sa.String(length=36), nullable=True),
    sa.Column('place_id', sa.String(length=36), nullable=True),
    sa.Column('version', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['intervention_id'], ['interventions.id'], ),
    sa.ForeignKeyConstraint(['place_id'], ['places.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('interventions_values', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_interventions_values_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_interventions_values_owner_user_id'), ['owner_user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_interventions_values_tenant_id'), ['tenant_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('interventions_values', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_interventions_values_tenant_id'))
        batch_op.drop_index(batch_op.f('ix_interventions_values_owner_user_id'))
        batch_op.drop_index(batch_op.f('ix_interventions_values_name'))

    op.drop_table('interventions_values')
    # ### end Alembic commands ###