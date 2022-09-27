"""link address with user

Revision ID: c28658d7fc28
Revises: 1169a136906c
Create Date: 2022-09-27 01:38:23.327827

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c28658d7fc28'
down_revision = '1169a136906c'
branch_labels = None
depends_on = None


def upgrade() :
    op.add_column('users', sa.Column('address_id',sa.Integer(),nullable=True))
    op.create_foreign_key("address_user_fk",source_table="users",referent_table="address",
    local_cols=["address_id"],remote_cols=["id"],ondelete="CASCADE")


def downgrade() :
    op.drop_column("users","address_id")
    op.drop_constraint("address_user_fk",table_name="address")
    