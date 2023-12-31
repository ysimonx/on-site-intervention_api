"""section

Revision ID: b994476983fe
Revises: 5fa59fdc36f5
Create Date: 2023-12-30 10:51:41.532208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b994476983fe'
down_revision = '5fa59fdc36f5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sections',
    sa.Column('id', sa.String(length=36), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.Column('owner_user_id', sa.String(length=36), nullable=True),
    sa.Column('tenant_id', sa.String(length=36), nullable=True),
    sa.Column('section_on_site_uuid', sa.String(length=36), nullable=True),
    sa.Column('section_type', sa.String(length=100), nullable=True),
    sa.Column('section_name', sa.String(length=100), nullable=True),
    sa.Column('form_on_site_uuid', sa.String(length=36), nullable=True),
    sa.Column('form_id', sa.String(length=36), nullable=True),
    sa.Column('section_order_in_form', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['form_id'], ['forms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('sections', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_sections_form_on_site_uuid'), ['form_on_site_uuid'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_owner_user_id'), ['owner_user_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_section_name'), ['section_name'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_section_on_site_uuid'), ['section_on_site_uuid'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_section_type'), ['section_type'], unique=False)
        batch_op.create_index(batch_op.f('ix_sections_tenant_id'), ['tenant_id'], unique=False)

    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.add_column(sa.Column('field_order_in_section', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('section_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'sections', ['section_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('fields', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('section_id')
        batch_op.drop_column('field_order_in_section')

    with op.batch_alter_table('sections', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_sections_tenant_id'))
        batch_op.drop_index(batch_op.f('ix_sections_section_type'))
        batch_op.drop_index(batch_op.f('ix_sections_section_on_site_uuid'))
        batch_op.drop_index(batch_op.f('ix_sections_section_name'))
        batch_op.drop_index(batch_op.f('ix_sections_owner_user_id'))
        batch_op.drop_index(batch_op.f('ix_sections_name'))
        batch_op.drop_index(batch_op.f('ix_sections_form_on_site_uuid'))

    op.drop_table('sections')
    # ### end Alembic commands ###
