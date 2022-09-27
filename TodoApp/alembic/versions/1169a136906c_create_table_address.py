"""create table address

Revision ID: 1169a136906c
Revises: b3ac06482c17
Create Date: 2022-09-27 01:28:29.349788

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1169a136906c'
down_revision = 'b3ac06482c17'
branch_labels = None
depends_on = None


def upgrade() :
    op.create_table("address",
    sa.Column("id",sa.Integer(),nullable=False,primary_key=True),
    sa.Column("address1",sa.String(),nullable=False),
    sa.Column("address2",sa.String(),nullable=False),
    sa.Column("city",sa.String(),nullable=False),
    sa.Column("state",sa.String(),nullable=False),
    sa.Column("country",sa.String(),nullable=False),
    sa.Column("postalcode",sa.Integer(),nullable=False),
    )


def downgrade():
    op.drop_table("address")
