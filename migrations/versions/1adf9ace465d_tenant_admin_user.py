"""tenant admin user

Revision ID: 1adf9ace465d
Revises: d0dd98c67b4e
Create Date: 2024-01-28 16:11:32.079432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1adf9ace465d'
down_revision = 'd0dd98c67b4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenants', schema=None) as batch_op:
        batch_op.add_column(sa.Column('admin_tenant_user_id', sa.String(length=36), nullable=True))
        batch_op.create_foreign_key(None, 'users', ['admin_tenant_user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tenants', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('admin_tenant_user_id')

    # ### end Alembic commands ###
